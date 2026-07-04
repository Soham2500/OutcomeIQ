"""Read-only checks for the OutcomeIQ development seed records."""

from pathlib import Path
import sys

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402
from app.models.audit_event import AuditEvent  # noqa: E402
from app.models.organization import Organization  # noqa: E402
from app.models.project import Project  # noqa: E402
from app.models.project_member import ProjectMember  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.dev_seed_service import (  # noqa: E402
    DEMO_EMAIL,
    DEMO_ORGANIZATION_SLUG,
    DEMO_PROJECT_SLUG,
)


COUNT_MODELS = (
    ("users", User),
    ("organizations", Organization),
    ("projects", Project),
    ("project_members", ProjectMember),
    ("audit_events", AuditEvent),
)


def main() -> int:
    if db_session.SessionLocal is None:
        print("CORE DEVELOPMENT DATA MISSING")
        print("Database is not configured.")
        return 1

    database_session = db_session.SessionLocal()
    try:
        for table_name, model in COUNT_MODELS:
            count = database_session.scalar(select(func.count()).select_from(model))
            print(f"{table_name}: {count}")

        user = database_session.scalar(
            select(User).where(User.email == DEMO_EMAIL)
        )
        organization = database_session.scalar(
            select(Organization).where(
                Organization.slug == DEMO_ORGANIZATION_SLUG
            )
        )
        project = None
        if organization is not None:
            project = database_session.scalar(
                select(Project).where(
                    Project.organization_id == organization.id,
                    Project.slug == DEMO_PROJECT_SLUG,
                )
            )

        if user is not None and organization is not None and project is not None:
            print("CORE DEVELOPMENT DATA FOUND")
        else:
            print("CORE DEVELOPMENT DATA MISSING")
        return 0
    except SQLAlchemyError:
        print("CORE DEVELOPMENT DATA MISSING")
        print("Core data check failed. Run migrations before checking seed data.")
        return 1
    finally:
        database_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
