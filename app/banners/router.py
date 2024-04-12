from typing import Annotated
from fastapi import APIRouter, Header

from app.banners.schemas import SBanner
from app.banners.dao import BannersDAO


router = APIRouter()


@router.get("/user_banner")
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


@router.get("/banner")
def banner(token: Annotated[str, Header()] = "admin_token",
           feature_id: int = None,
           tag_id: int = None,
           limit: int = None,
           offset: int = None):
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
