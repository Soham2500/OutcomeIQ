"""Database access functions for workflow configurations."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workflow_configuration import WorkflowConfiguration


UPDATABLE_FIELDS = {
    "name",
    "description",
    "strategy_name",
    "config_json",
    "is_active",
}


def create_workflow_configuration(
    db: Session,
    workflow_id: uuid.UUID,
    name: str,
    version_label: str,
    description: str | None = None,
    strategy_name: str | None = None,
    config_json: dict[str, object] | None = None,
    created_by_user_id: uuid.UUID | None = None,
) -> WorkflowConfiguration:
    configuration = WorkflowConfiguration(
        workflow_id=workflow_id,
        name=name,
        version_label=version_label,
        description=description,
        strategy_name=strategy_name,
        config_json=config_json,
        created_by_user_id=created_by_user_id,
    )
    db.add(configuration)
    db.commit()
    db.refresh(configuration)
    return configuration


def get_configuration_by_id(
    db: Session,
    configuration_id: uuid.UUID,
) -> WorkflowConfiguration | None:
    return db.get(WorkflowConfiguration, configuration_id)


def get_configuration_by_version(
    db: Session,
    workflow_id: uuid.UUID,
    version_label: str,
) -> WorkflowConfiguration | None:
    return db.scalar(
        select(WorkflowConfiguration).where(
            WorkflowConfiguration.workflow_id == workflow_id,
            WorkflowConfiguration.version_label == version_label,
        )
    )


def list_configurations(
    db: Session,
    workflow_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowConfiguration]:
    statement = (
        select(WorkflowConfiguration)
        .where(WorkflowConfiguration.workflow_id == workflow_id)
        .order_by(WorkflowConfiguration.created_at, WorkflowConfiguration.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def update_configuration(
    db: Session,
    configuration: WorkflowConfiguration,
    **fields: object,
) -> WorkflowConfiguration:
    if set(fields) - UPDATABLE_FIELDS:
        raise ValueError("Unsupported workflow configuration update field.")
    for field_name, value in fields.items():
        setattr(configuration, field_name, value)
    db.add(configuration)
    db.commit()
    db.refresh(configuration)
    return configuration
