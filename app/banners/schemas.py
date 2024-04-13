from typing import Any, Dict
from pydantic import BaseModel


class SBanner(BaseModel):
    tag_ids: list | None = None
    feature_id: int | None = None
    content: Dict[str, Any] | None = None
    is_active: bool | None = None
