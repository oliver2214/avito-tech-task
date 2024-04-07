from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()
app.title = "Сервис баннеров"


class SBanner(BaseModel):
    tag_ids: list = [0]
    feature_id: int = 0
    content: dict = {
        "title": "some_title",
        "text": "some_text",
        "url": "some_url"
    }
    is_active: bool = True


@app.get("/user_banner")
def user_banner(tag_id: int,
                feature_id: int,
                use_last_revision: bool = False,
                token: Annotated[str, Header()] = "user_token"):

    return {
        "tag_id": tag_id,
        "feature_id": feature_id,
        "use_last_revision": use_last_revision,
        "token": token
    }


@app.get("/banner")
def banner(token: Annotated[str, Header()] = "admin_token",
           feature_id: int = None,
           tag_id: int = None,
           limit: int = None,
           offset: int = None):

    return {
        "token": token,
        "feature_id": feature_id,
        "tag_id": tag_id,
        "limit": limit,
        "offset": offset
    }


@app.post("/banner")
def post_banner(token: Annotated[str, Header()] = "admin_token",
                banner: SBanner = None):
    return banner


@app.patch("/banner/{id}")
def patch_banner(id: int,
                 token: Annotated[str, Header()] = "admin_token",
                 banner: SBanner = None):
    return banner


@app.delete("/banner/{id}")
def delete_banner(id: int,
                  token: Annotated[str, Header()] = "admin_token"):
    return id
