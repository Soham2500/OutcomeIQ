"""Seed a deterministic, idempotent OutcomeIQ customer-support demo dataset."""

from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import sys

import bcrypt
from sqlalchemy import inspect, select
from sqlalchemy.exc import SQLAlchemyError


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db import session as db_session  # noqa: E402
from app.models.enums import (  # noqa: E402
    ProjectMemberRole,
    UserStatus,
    WorkflowOutcomeStatus,
    WorkflowRunStatus,
)
from app.models.recommendation import Recommendation  # noqa: E402
from app.models.workflow_run import WorkflowRun  # noqa: E402
from app.repositories.model_call_repository import (  # noqa: E402
    create_model_call,
    list_model_calls,
)
from app.repositories.organization_repository import (  # noqa: E402
    create_organization,
    get_organization_by_slug,
)
from app.repositories.outcome_contract_repository import (  # noqa: E402
    get_outcome_contract_by_name,
)
from app.repositories.project_member_repository import (  # noqa: E402
    add_project_member,
    get_project_member,
)
from app.repositories.project_repository import (  # noqa: E402
    create_project,
    get_project_by_slug,
)
from app.repositories.tool_call_repository import (  # noqa: E402
    create_tool_call,
    list_tool_calls,
)
from app.repositories.user_repository import (  # noqa: E402
    create_user,
    get_user_by_email,
)
from app.repositories.workflow_configuration_repository import (  # noqa: E402
    create_workflow_configuration,
    get_configuration_by_version,
)
from app.repositories.workflow_repository import (  # noqa: E402
    create_workflow,
    get_workflow_by_slug,
)
from app.repositories.workflow_run_repository import (  # noqa: E402
    complete_workflow_run,
    create_workflow_run,
    mark_workflow_run_running,
)
from app.schemas.outcome_contract import OutcomeContractCreate  # noqa: E402
from app.schemas.workflow_run_outcome import WorkflowRunOutcomeCreate  # noqa: E402
from app.services.cost_calculation_service import (  # noqa: E402
    calculate_workflow_run_cost,
)
from app.services.outcome_service import (  # noqa: E402
    create_contract,
    record_workflow_run_outcome,
)
from app.services.recommendation_service import (  # noqa: E402
    generate_project_recommendations,
)


DEMO_EMAIL = "demo@outcomeiq.local"
DEMO_PASSWORD = "Demo@12345"  # Local placeholder; never printed.
DEMO_ORGANIZATION_NAME = "OutcomeIQ Demo Org"
DEMO_ORGANIZATION_SLUG = "outcomeiq-live-demo-org"
DEMO_PROJECT_NAME = "AI Support Cost Optimization Demo"
DEMO_PROJECT_SLUG = "ai-support-live-quality-demo"

REQUIRED_TABLES = {
    "users",
    "organizations",
    "projects",
    "project_members",
    "workflows",
    "workflow_configurations",
    "workflow_runs",
    "model_calls",
    "tool_calls",
    "model_pricing_rates",
    "workflow_run_costs",
    "outcome_contracts",
    "workflow_run_outcomes",
    "recommendations",
}

WORKFLOW_SPECS = (
    {
        "name": "Support Ticket Classifier",
        "slug": "support-ticket-classifier",
        "description": "Classifies customer-support intent and urgency.",
        "tool_name": "customer_profile_lookup",
    },
    {
        "name": "Refund Request Assistant",
        "slug": "refund-request-assistant",
        "description": "Assesses refund eligibility and drafts a resolution.",
        "tool_name": "refund_policy_lookup",
    },
    {
        "name": "Escalation Risk Detector",
        "slug": "escalation-risk-detector",
        "description": "Identifies tickets likely to require human escalation.",
        "tool_name": "ticket_history_lookup",
    },
)

RUN_SPECS = {
    "support-ticket-classifier": (
        ("01", "succeeded", 700, 180, Decimal("0.0008")),
        ("02", "succeeded", 850, 220, Decimal("0.0010")),
        ("03", "failed", 1700, 560, Decimal("0.0035")),
        ("04", "pending", 1000, 300, Decimal("0.0015")),
    ),
    "refund-request-assistant": (
        ("01", "succeeded", 1100, 340, Decimal("0.0018")),
        ("02", "failed", 3200, 1100, Decimal("0.0070")),
        ("03", "escalated", 2800, 900, Decimal("0.0060")),
        ("04", "succeeded", 1450, 430, Decimal("0.0022")),
    ),
    "escalation-risk-detector": (
        ("01", "succeeded", 650, 160, Decimal("0.0007")),
        ("02", "failed", 2100, 680, Decimal("0.0045")),
        ("03", "escalated", 3600, 1250, Decimal("0.0080")),
        ("04", "pending", 900, 240, Decimal("0.0012")),
    ),
}


def _increment(
    counts: defaultdict[str, dict[str, int]],
    entity: str,
    state: str,
    amount: int = 1,
) -> None:
    counts[entity][state] += amount


def _ensure_demo_user(db, counts):
    user = get_user_by_email(db, DEMO_EMAIL)
    if user is None:
        user = create_user(
            db,
            email=DEMO_EMAIL,
            full_name="OutcomeIQ Demo User",
            hashed_password=_hash_demo_password(),
        )
        _increment(counts, "users", "created")
        return user

    changed = False
    if not _demo_password_matches(user.hashed_password):
        user.hashed_password = _hash_demo_password()
        changed = True
    if user.status != UserStatus.ACTIVE.value:
        user.status = UserStatus.ACTIVE.value
        changed = True
    if changed:
        db.add(user)
        db.commit()
        db.refresh(user)
        _increment(counts, "users", "updated")
    else:
        _increment(counts, "users", "reused")
    return user


def _hash_demo_password() -> str:
    return bcrypt.hashpw(
        DEMO_PASSWORD.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def _demo_password_matches(hashed_password: str | None) -> bool:
    if not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            DEMO_PASSWORD.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (TypeError, ValueError):
        return False


def _ensure_organization_and_project(db, user, counts):
    organization = get_organization_by_slug(db, DEMO_ORGANIZATION_SLUG)
    if organization is None:
        organization = create_organization(
            db,
            DEMO_ORGANIZATION_NAME,
            DEMO_ORGANIZATION_SLUG,
        )
        _increment(counts, "organizations", "created")
    else:
        _increment(counts, "organizations", "reused")

    project = get_project_by_slug(
        db,
        organization.id,
        DEMO_PROJECT_SLUG,
    )
    if project is None:
        project = create_project(
            db,
            organization_id=organization.id,
            name=DEMO_PROJECT_NAME,
            slug=DEMO_PROJECT_SLUG,
            description=(
                "Deterministic AI customer-support evidence for OutcomeIQ demos."
            ),
        )
        _increment(counts, "projects", "created")
    else:
        _increment(counts, "projects", "reused")

    membership = get_project_member(db, project.id, user.id)
    if membership is None:
        add_project_member(
            db,
            project_id=project.id,
            user_id=user.id,
            role=ProjectMemberRole.OWNER.value,
        )
        _increment(counts, "memberships", "created")
    else:
        _increment(counts, "memberships", "reused")
    return organization, project


def _ensure_workflow(db, user, project, spec, counts):
    workflow = get_workflow_by_slug(db, project.id, spec["slug"])
    if workflow is None:
        workflow = create_workflow(
            db,
            project_id=project.id,
            name=spec["name"],
            slug=spec["slug"],
            description=spec["description"],
            created_by_user_id=user.id,
        )
        _increment(counts, "workflows", "created")
    else:
        _increment(counts, "workflows", "reused")

    configuration = get_configuration_by_version(db, workflow.id, "demo-v1")
    if configuration is None:
        configuration = create_workflow_configuration(
            db,
            workflow_id=workflow.id,
            name="Deterministic demo configuration",
            version_label="demo-v1",
            description="Simulated local evidence configuration.",
            strategy_name="balanced-demo",
            config_json={"provider_mode": "simulated", "dataset": "live-v1"},
            created_by_user_id=user.id,
        )
        _increment(counts, "configurations", "created")
    else:
        _increment(counts, "configurations", "reused")

    contract_name = f"{spec['name']} verified outcome"
    contract = get_outcome_contract_by_name(db, project.id, contract_name)
    if contract is None:
        contract = create_contract(
            db,
            user.id,
            OutcomeContractCreate(
                project_id=project.id,
                workflow_id=workflow.id,
                name=contract_name,
                description=(
                    "A support attempt is successful when the expected business "
                    "resolution is verified."
                ),
                success_criteria_json={
                    "resolution_verified": True,
                    "demo_only": True,
                },
                success_window_hours=48,
            ),
        )
        _increment(counts, "outcome_contracts", "created")
    else:
        _increment(counts, "outcome_contracts", "reused")
    return workflow, configuration, contract


def _ensure_model_calls(db, run, prompt_tokens, completion_tokens, counts):
    existing_by_sequence = {
        call.sequence_number: call for call in list_model_calls(db, run.id)
    }
    call_specs = (
        {
            "sequence_number": 1,
            "model_name": "support-classifier-small",
            "call_type": "classification",
            "prompt_tokens": max(1, prompt_tokens // 3),
            "completion_tokens": max(1, completion_tokens // 4),
            "latency_ms": 140,
        },
        {
            "sequence_number": 2,
            "model_name": "support-generator-standard",
            "call_type": "generation",
            "prompt_tokens": prompt_tokens - max(1, prompt_tokens // 3),
            "completion_tokens": completion_tokens - max(1, completion_tokens // 4),
            "latency_ms": 420,
        },
    )
    for spec in call_specs:
        if spec["sequence_number"] in existing_by_sequence:
            _increment(counts, "model_calls", "reused")
            continue
        create_model_call(
            db,
            workflow_run_id=run.id,
            provider="simulated",
            model_name=spec["model_name"],
            call_type=spec["call_type"],
            status="succeeded",
            prompt_tokens=spec["prompt_tokens"],
            completion_tokens=spec["completion_tokens"],
            total_tokens=(
                spec["prompt_tokens"] + spec["completion_tokens"]
            ),
            latency_ms=spec["latency_ms"],
            request_summary="Redacted deterministic support input.",
            response_summary="Simulated deterministic support output.",
            metadata_json={"demo_only": True},
            sequence_number=spec["sequence_number"],
        )
        _increment(counts, "model_calls", "created")


def _ensure_tool_call(db, run, tool_name, tool_cost, counts):
    calls = list_tool_calls(db, run.id)
    if any(call.sequence_number == 3 for call in calls):
        _increment(counts, "tool_calls", "reused")
        return
    create_tool_call(
        db,
        workflow_run_id=run.id,
        sequence_number=3,
        tool_name=tool_name,
        status="succeeded",
        latency_ms=90,
        estimated_cost_usd=tool_cost,
        input_summary="Synthetic support record reference.",
        output_summary="Synthetic support record result.",
        metadata_json={"demo_only": True},
    )
    _increment(counts, "tool_calls", "created")


def _ensure_run(
    db,
    user,
    project,
    workflow,
    configuration,
    contract,
    workflow_spec,
    run_spec,
    counts,
):
    label, outcome_status, prompt_tokens, completion_tokens, tool_cost = run_spec
    external_reference = f"live-demo-{workflow.slug}-{label}"
    run = db.scalar(
        select(WorkflowRun).where(
            WorkflowRun.external_reference == external_reference
        )
    )
    if run is None:
        run = create_workflow_run(
            db,
            project_id=project.id,
            workflow_id=workflow.id,
            configuration_id=configuration.id,
            triggered_by_user_id=user.id,
            trigger_type="simulated",
            external_reference=external_reference,
            input_summary=f"Synthetic {workflow.name} support case {label}.",
            metadata_json={"demo_only": True, "dataset_version": "live-v1"},
        )
        run = mark_workflow_run_running(db, run)
        _increment(counts, "workflow_runs", "created")
    else:
        _increment(counts, "workflow_runs", "reused")
        if run.status == WorkflowRunStatus.PENDING.value:
            run = mark_workflow_run_running(db, run)

    _ensure_model_calls(db, run, prompt_tokens, completion_tokens, counts)
    _ensure_tool_call(db, run, workflow_spec["tool_name"], tool_cost, counts)

    if run.status == WorkflowRunStatus.RUNNING.value:
        run = complete_workflow_run(
            db,
            run,
            output_summary=f"Synthetic {workflow.name} result recorded.",
            latency_ms=650 + (prompt_tokens // 5),
            metadata_json={"demo_only": True, "dataset_version": "live-v1"},
        )

    calculate_workflow_run_cost(db, run.id)
    _increment(counts, "run_costs", "upserted")

    score_by_status = {
        "succeeded": Decimal("1.0"),
        "failed": Decimal("0.0"),
        "escalated": Decimal("0.25"),
        "pending": None,
    }
    record_workflow_run_outcome(
        db,
        run.id,
        WorkflowRunOutcomeCreate(
            outcome_contract_id=contract.id,
            status=WorkflowOutcomeStatus(outcome_status),
            verification_source="simulated",
            outcome_score=score_by_status[outcome_status],
            notes="Deterministic local demo outcome.",
            metadata_json={
                "demo_only": True,
                "dataset_version": "live-v1",
            },
        ),
    )
    _increment(counts, "run_outcomes", "upserted")


def _ensure_recommendations(db, project, workflows, counts):
    scopes = [None, *(workflow.id for workflow in workflows)]
    for workflow_id in scopes:
        statement = select(Recommendation).where(
            Recommendation.project_id == project.id,
            Recommendation.status == "open",
        )
        statement = (
            statement.where(Recommendation.workflow_id.is_(None))
            if workflow_id is None
            else statement.where(Recommendation.workflow_id == workflow_id)
        )
        existing = list(db.scalars(statement))
        if existing:
            _increment(counts, "recommendations", "reused", len(existing))
            continue
        response = generate_project_recommendations(
            db,
            project_id=project.id,
            workflow_id=workflow_id,
        )
        _increment(
            counts,
            "recommendations",
            "created",
            response.generated_count,
        )


def seed_demo_data(db) -> defaultdict[str, dict[str, int]]:
    counts: defaultdict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    user = _ensure_demo_user(db, counts)
    organization, project = _ensure_organization_and_project(
        db,
        user,
        counts,
    )

    workflows = []
    for workflow_spec in WORKFLOW_SPECS:
        workflow, configuration, contract = _ensure_workflow(
            db,
            user,
            project,
            workflow_spec,
            counts,
        )
        workflows.append(workflow)
        for run_spec in RUN_SPECS[workflow_spec["slug"]]:
            _ensure_run(
                db,
                user,
                project,
                workflow,
                configuration,
                contract,
                workflow_spec,
                run_spec,
                counts,
            )

    _ensure_recommendations(db, project, workflows, counts)
    return counts


def main() -> int:
    if db_session.SessionLocal is None:
        print("DATABASE NOT CONFIGURED")
        return 1

    database_session = db_session.SessionLocal()
    try:
        existing_tables = set(inspect(database_session.get_bind()).get_table_names())
        missing_tables = sorted(REQUIRED_TABLES - existing_tables)
        if missing_tables:
            print("DEMO DATA TABLES MISSING")
            print("Run database migrations before seeding demo data.")
            return 1

        counts = seed_demo_data(database_session)
        print("DEMO DATA SEED COMPLETE")
        print(f"demo user email: {DEMO_EMAIL}")
        print(f"organization: {DEMO_ORGANIZATION_NAME}")
        print(f"project: {DEMO_PROJECT_NAME}")
        for entity in sorted(counts):
            summary = ", ".join(
                f"{state}={value}"
                for state, value in sorted(counts[entity].items())
            )
            print(f"{entity}: {summary}")
        return 0
    except (SQLAlchemyError, LookupError, ValueError, TypeError) as exc:
        database_session.rollback()
        print("DEMO DATA SEED FAILED")
        print(f"error type: {type(exc).__name__}")
        return 1
    finally:
        database_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
