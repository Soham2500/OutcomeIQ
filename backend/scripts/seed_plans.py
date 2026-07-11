"""Seed idempotent subscription plans for local/test billing."""

from decimal import Decimal
from pathlib import Path
import sys

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402
from app.models.plan import Plan  # noqa: E402
from app.services.billing_service import get_plan_by_slug  # noqa: E402


PLANS = (
    {
        "name": "Free",
        "slug": "free",
        "description": "Free MVP plan for safe simulated OutcomeIQ demos.",
        "price_inr_monthly": Decimal("0.00"),
        "currency": "INR",
        "max_projects": 1,
        "max_workflow_runs_per_month": 50,
        "max_team_members": 1,
        "export_enabled": False,
        "analytics_enabled": True,
        "recommendations_enabled": True,
        "openai_provider_enabled": False,
        "is_active": True,
    },
    {
        "name": "Starter",
        "slug": "starter",
        "description": "Starter test-mode plan for small teams.",
        "price_inr_monthly": Decimal("499.00"),
        "currency": "INR",
        "max_projects": 5,
        "max_workflow_runs_per_month": 1000,
        "max_team_members": 3,
        "export_enabled": True,
        "analytics_enabled": True,
        "recommendations_enabled": True,
        "openai_provider_enabled": False,
        "is_active": True,
    },
    {
        "name": "Pro",
        "slug": "pro",
        "description": "Pro test-mode plan for larger evaluation projects.",
        "price_inr_monthly": Decimal("1499.00"),
        "currency": "INR",
        "max_projects": 20,
        "max_workflow_runs_per_month": 10000,
        "max_team_members": 10,
        "export_enabled": True,
        "analytics_enabled": True,
        "recommendations_enabled": True,
        "openai_provider_enabled": False,
        "is_active": True,
    },
)


def main() -> int:
    if db_session.SessionLocal is None:
        print("DATABASE NOT CONFIGURED")
        return 1

    database_session = db_session.SessionLocal()
    try:
        inspector = inspect(database_session.get_bind())
        if not inspector.has_table("plans"):
            print("PLANS TABLE MISSING")
            print("Run scripts/db_migrate.ps1 from the project root first.")
            return 1

        created_count = 0
        existing_count = 0
        for plan_data in PLANS:
            existing = get_plan_by_slug(database_session, plan_data["slug"])
            if existing is not None:
                for key, value in plan_data.items():
                    setattr(existing, key, value)
                database_session.add(existing)
                existing_count += 1
                continue
            database_session.add(Plan(**plan_data))
            created_count += 1

        database_session.commit()
        print("SUBSCRIPTION PLAN SEED COMPLETE")
        print(f"created: {created_count}")
        print(f"updated_or_existing: {existing_count}")
        print("Plans are for local/test billing only. No real payment keys are used.")
        return 0
    except SQLAlchemyError:
        database_session.rollback()
        print("SUBSCRIPTION PLAN SEED ERROR")
        print("Verify migrations and database access, then retry.")
        return 1
    finally:
        database_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
