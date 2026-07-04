"""Validate Alembic files and database revision state without migrating."""

from pathlib import Path
import sys

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402


ALEMBIC_CONFIG_PATH = BACKEND_ROOT / "alembic.ini"
MIGRATIONS_PATH = BACKEND_ROOT / "alembic"
VERSIONS_PATH = MIGRATIONS_PATH / "versions"


def validate_alembic_state() -> bool:
    """Return True when migration files exist and the database is at head."""

    if db_session.engine is None:
        return False
    if not MIGRATIONS_PATH.is_dir() or not VERSIONS_PATH.is_dir():
        return False

    migration_files = list(VERSIONS_PATH.glob("*.py"))
    if not migration_files or not ALEMBIC_CONFIG_PATH.is_file():
        return False

    try:
        alembic_config = Config(str(ALEMBIC_CONFIG_PATH))
        alembic_config.set_main_option("script_location", str(MIGRATIONS_PATH))
        script_directory = ScriptDirectory.from_config(alembic_config)
        migration_heads = set(script_directory.get_heads())

        with db_session.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            migration_context = MigrationContext.configure(connection)
            current_heads = set(migration_context.get_current_heads())

        return bool(migration_heads) and current_heads == migration_heads
    except (CommandError, SQLAlchemyError, OSError, ValueError):
        return False


def main() -> int:
    """Print a stable validation result without exposing connection details."""

    if validate_alembic_state():
        print("ALEMBIC STATE VALID")
        return 0

    print("ALEMBIC STATE NEEDS ATTENTION")
    print("Check database connectivity, migration files, and the current revision.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
