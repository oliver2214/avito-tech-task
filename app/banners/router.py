from typing import Annotated, Any, Dict
from fastapi import APIRouter, Header, HTTPException

from app.banners.schemas import SBanner
from app.banners.dao import BannersDAO


router = APIRouter()


@router.get("/user_banner")
def user_banner(tag_id: int,
                feature_id: int,
                use_last_revision: bool = False,
                token: Annotated[str, Header()] = "user_token") -> Dict[str, Any]:
    if len(token) == 0:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    elif token not in ("user_token", "admin_token"):
        raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")

    content = BannersDAO.user_banner(feature_id, tag_id)

    if content is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return content


@router.get("/banner")
def banner(token: Annotated[str | None, Header()] = "admin_token",
           feature_id: int = None,
           tag_id: int = None,
           limit: int = None,
           offset: int = None):
    if len(token) == 0:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    elif token != "admin_token":
        raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")

    banners = BannersDAO.banner(feature_id, tag_id, limit, offset)
    return banners


@router.post("/banner")
def post_banner(banner: SBanner,
                token: Annotated[str, Header()] = "admin_token"):

    return banner


@router.patch("/banner/{id}")
def patch_banner(id: int,
                 token: Annotated[str, Header()] = "admin_token",
                 banner: SBanner = None):
    return banner


@router.delete("/banner/{id}")
def delete_banner(id: int,
                  token: Annotated[str, Header()] = "admin_token"):
    return id
