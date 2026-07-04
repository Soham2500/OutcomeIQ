"""Seed safe, idempotent local development data."""

from pathlib import Path
import sys

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402
from app.services.dev_seed_service import seed_development_data  # noqa: E402
from scripts.check_db_tables import CORE_TABLES  # noqa: E402


def main() -> int:
    if db_session.SessionLocal is None:
        print("DATABASE NOT CONFIGURED")
        print("Configure backend/.env before running the development seed.")
        return 1

    database_session = db_session.SessionLocal()
    try:
        inspector = inspect(database_session.get_bind())
        missing_tables = [
            table_name
            for table_name in CORE_TABLES
            if not inspector.has_table(table_name)
        ]
        if missing_tables:
            print("CORE TABLES MISSING")
            print("Run scripts/db_migrate.ps1 from the project root first.")
            return 1

        result = seed_development_data(database_session)
        print("DEVELOPMENT SEED COMPLETE")
        for record_type, state in result.items():
            print(f"{record_type}: {state}")
        return 0
    except SQLAlchemyError:
        database_session.rollback()
        print("DEVELOPMENT SEED ERROR")
        print("The seed could not complete. Verify migrations and database access.")
        return 1
    finally:
        database_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
