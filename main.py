from typing import Annotated, Optional, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()
app.title = "Сервис баннеров"


@app.get("/user_banner")
def user_banner(tag_id: int,
                feature_id: int,
                use_last_revision: bool = False,
                token: Annotated[str | None, Header()] = None):

    return {
        "tag_id": tag_id,
        "feature_id": feature_id,
        "use_last_revision": use_last_revision,
        "token": token
    }


@app.get("/banner")
def banner(token: Annotated[str | None, Header()] = None,
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
