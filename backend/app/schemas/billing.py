"""Pydantic schemas for subscription-ready billing APIs."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field


class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    price_inr_monthly: Decimal
    currency: str
    max_projects: int
    max_workflow_runs_per_month: int
    max_team_members: int
    export_enabled: bool
    analytics_enabled: bool
    recommendations_enabled: bool
    openai_provider_enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    status: str
    provider: str
    provider_subscription_id: str | None
    current_period_start: datetime | None
    current_period_end: datetime | None
    cancel_at_period_end: bool
    created_at: datetime
    updated_at: datetime


class BillingCheckoutRequest(BaseModel):
    plan_slug: str = Field(min_length=1, max_length=80)


class BillingCheckoutResponse(BaseModel):
    provider: str
    plan_slug: str
    test_checkout_url: str
    message: str


class UsageSummaryRead(BaseModel):
    period_month: str
    projects_used: int
    max_projects: int
    workflow_runs_used: int
    max_workflow_runs_per_month: int


class BillingMeRead(BaseModel):
    plan: PlanRead
    subscription: SubscriptionRead
    usage: UsageSummaryRead
    payment_mode: str = "test/sandbox"


class BillingWebhookResponse(BaseModel):
    stored: bool
    processed: bool
    message: str
