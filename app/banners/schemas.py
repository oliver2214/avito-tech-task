from typing import Any, Dict, List
from pydantic import BaseModel


class SBanner(BaseModel):
    tag_ids: List[int] | None = None
    feature_id: int | None = None
    content: Dict[str, Any] | None = None
    is_active: bool | None = None
