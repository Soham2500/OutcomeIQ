"""String enums shared by the core OutcomeIQ database models."""

from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class ProjectMemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    SYSTEM = "system"


class WorkflowStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class WorkflowRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ModelCallStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RETRIED = "retried"
    FALLBACK_USED = "fallback_used"


class ToolCallStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class WorkflowRunTrigger(str, Enum):
    MANUAL = "manual"
    API = "api"
    SIMULATED = "simulated"
    SCHEDULED = "scheduled"


class CostCalculationStatus(str, Enum):
    CALCULATED = "calculated"
    PARTIAL = "partial"
    FAILED = "failed"


class OutcomeContractStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class WorkflowOutcomeStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ESCALATED = "escalated"
    REOPENED = "reopened"
    ABANDONED = "abandoned"
    REVERSED = "reversed"


class OutcomeVerificationSource(str, Enum):
    MANUAL = "manual"
    SIMULATED = "simulated"
    API = "api"
    SYSTEM = "system"


class RecommendationType(str, Enum):
    MISSING_COSTS = "missing_costs"
    MISSING_OUTCOMES = "missing_outcomes"
    HIGH_COST_LOW_SUCCESS = "high_cost_low_success"
    HIGH_FAILURE_RATE = "high_failure_rate"
    COST_PER_SUCCESS_OPPORTUNITY = "cost_per_success_opportunity"
    DATA_QUALITY = "data_quality"


class RecommendationSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecommendationStatus(str, Enum):
    OPEN = "open"
    ACCEPTED = "accepted"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"


class SubscriptionStatus(str, Enum):
    FREE = "free"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PaymentProvider(str, Enum):
    MANUAL = "manual"
    RAZORPAY_TEST = "razorpay_test"
    RAZORPAY_LIVE = "razorpay_live"
    STRIPE_TEST = "stripe_test"
