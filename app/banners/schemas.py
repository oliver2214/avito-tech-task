from typing import Any, Dict
from pydantic import BaseModel


class SBanner(BaseModel):
    tag_ids: list = [0]
    feature_id: int = 0
    content: Dict[str, Any]
    is_active: bool = True
