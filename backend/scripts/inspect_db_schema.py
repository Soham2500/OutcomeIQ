"""Print a safe, read-only summary of the OutcomeIQ database schema."""

from pathlib import Path
import sys

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402


KNOWN_CORE_TABLES = (
    "system_metadata",
    "users",
    "organizations",
    "projects",
    "project_members",
    "audit_events",
)


def main() -> int:
    """Inspect table and column metadata without changing database state."""

    if db_session.engine is None:
        print("DATABASE SCHEMA INSPECTION UNAVAILABLE")
        print("Database is not configured.")
        return 1

    try:
        inspector = inspect(db_session.engine)
        table_names = sorted(inspector.get_table_names())

        print("DATABASE TABLES")
        for table_name in table_names:
            print(f"- {table_name}")

        print("CORE TABLE COLUMNS")
        for table_name in KNOWN_CORE_TABLES:
            if table_name not in table_names:
                print(f"{table_name}: MISSING")
                continue

            print(f"{table_name}:")
            for column in inspector.get_columns(table_name):
                nullable = "nullable" if column["nullable"] else "not null"
                print(f"- {column['name']} | {column['type']} | {nullable}")

        return 0
    except SQLAlchemyError:
        print("DATABASE SCHEMA INSPECTION UNAVAILABLE")
        print("Schema inspection failed. Verify database connectivity.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
