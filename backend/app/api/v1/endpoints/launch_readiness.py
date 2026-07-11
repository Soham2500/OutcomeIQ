"""Protected launch-readiness endpoint for production safety review."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.services.launch_readiness_service import get_launch_readiness


router = APIRouter()


@router.get("/readiness")
def get_launch_readiness_endpoint(
    _current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, object]:
    return get_launch_readiness()
