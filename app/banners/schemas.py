from pydantic import BaseModel


class SBanner(BaseModel):
    tag_ids: list = [0]
    feature_id: int = 0
    content: dict = {
        "title": "some_title",
        "text": "some_text",
        "url": "some_url"
    }
    is_active: bool = True
