"""Seed idempotent, explicitly non-production model pricing rates."""

from decimal import Decimal
from pathlib import Path
import sys

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402
from app.repositories.model_pricing_rate_repository import (  # noqa: E402
    create_pricing_rate,
    get_active_rate,
)


DEMO_RATES = (
    {
        "provider": "simulated",
        "model_name": "support-classifier-small",
        "input_token_price_per_1k": Decimal("0.0001"),
        "output_token_price_per_1k": Decimal("0.0002"),
    },
    {
        "provider": "simulated",
        "model_name": "support-generator-standard",
        "input_token_price_per_1k": Decimal("0.0005"),
        "output_token_price_per_1k": Decimal("0.0015"),
    },
    {
        "provider": "openai",
        "model_name": "gpt-demo-placeholder",
        "input_token_price_per_1k": Decimal("0.0010"),
        "output_token_price_per_1k": Decimal("0.0030"),
    },
)


def main() -> int:
    if db_session.SessionLocal is None:
        print("DATABASE NOT CONFIGURED")
        return 1

    database_session = db_session.SessionLocal()
    try:
        inspector = inspect(database_session.get_bind())
        if not inspector.has_table("model_pricing_rates"):
            print("MODEL_PRICING_RATES TABLE MISSING")
            print("Run scripts/db_migrate.ps1 from the project root first.")
            return 1

        created_count = 0
        existing_count = 0
        for rate in DEMO_RATES:
            existing = get_active_rate(
                database_session,
                provider=rate["provider"],
                model_name=rate["model_name"],
            )
            if existing is not None:
                existing_count += 1
                continue
            create_pricing_rate(
                database_session,
                **rate,
                metadata_json={
                    "source": "OutcomeIQ local demo seed",
                    "demo_only": True,
                },
            )
            created_count += 1

        print("DEMO PRICING SEED COMPLETE")
        print(f"created: {created_count}")
        print(f"existing: {existing_count}")
        print("Rates are local demonstrations, not current provider prices.")
        return 0
    except SQLAlchemyError:
        database_session.rollback()
        print("DEMO PRICING SEED ERROR")
        print("Verify migrations and database access, then retry.")
        return 1
    finally:
        database_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
