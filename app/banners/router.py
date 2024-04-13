from typing import Annotated, Any, Dict
from fastapi import APIRouter, Header
from .exceptions import InvalidDataException, UnauthorizedException, ForbiddenException, NotFoundException

from .schemas import SBanner
from .dao import BannersDAO


router = APIRouter()


@router.get("/user_banner", summary="Получение баннера для пользователя")
def user_banner(tag_id: int,
                feature_id: int,
                use_last_revision: bool = False,
                token: Annotated[str, Header()] = "user_token") -> Dict[str, Any]:
    if len(token) == 0:
        raise UnauthorizedException()
    elif token not in ("user_token", "admin_token"):
        raise ForbiddenException()

    content = BannersDAO.user_banner(feature_id, tag_id)

    if content is None:
        raise NotFoundException()
    return content


@router.get("/banner", summary="Получение всех баннеров c фильтрацией по фиче и/или тегу")
def banner(token: Annotated[str | None, Header()] = "admin_token",
           feature_id: int = None,
           tag_id: int = None,
           limit: int = None,
           offset: int = None):
    if len(token) == 0:
        raise UnauthorizedException()
    elif token != "admin_token":
        raise ForbiddenException()

    banners = BannersDAO.banner(feature_id, tag_id, limit, offset)
    return banners


@router.post("/banner", status_code=201, summary="Создание нового баннера")
def post_banner(banner: SBanner,
                token: Annotated[str, Header()] = "admin_token"):
    if len(token) == 0:
        raise UnauthorizedException()
    elif token != "admin_token":
        raise ForbiddenException()
    if banner.feature_id is None or not banner.tag_ids:
        raise InvalidDataException(detail="Переданы пустые или null данные")

    banner_id = BannersDAO.post_banner(banner)
    return { "banner_id": banner_id }


@router.patch("/banner/{id}", summary="Обновление содержимого баннера")
def patch_banner(id: int,
                 token: Annotated[str, Header()] = "admin_token",
                 banner: SBanner = None):
    return banner


@router.delete("/banner/{id}", summary="Удаление баннера по идентификатору")
def delete_banner(id: int,
                  token: Annotated[str, Header()] = "admin_token"):
    return id
