from typing import Any, Dict, List
from pydantic import BaseModel


class SBanner(BaseModel):
    def __init__(self, **kwargs):
        self.tag_ids = kwargs["tag_ids"]
        self.feature_id = kwargs["feature_id"]
        self.content = kwargs["content"]
        self.is_active = kwargs["is_active"]

    tag_ids: List[int] | None = None
    feature_id: int | None = None
    content: Dict[str, Any] | None = None
    is_active: bool | None = None
