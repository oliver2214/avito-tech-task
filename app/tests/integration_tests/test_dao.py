from app.banners.dao import BannersDAO
from app.banners.exceptions import InvalidDataException, NotFoundException
from app.banners.schemas import SBanner


def test_add_and_get_banner():
    # Попытаемся добавить баннер с уже существующим сочетанием фича-тег
    try:
        invalid_banner = SBanner(
            tag_ids=[1, 2, 3, 4, 5],
            feature_id=1,
            content={"title": "Banner Title", "text": "Banner Text", "url": "https://example.com/banner"},
            is_active=True
        )
        banner_id = BannersDAO.post_banner(invalid_banner)
    except Exception as e:
        assert isinstance(e, InvalidDataException)

    banner = SBanner(
        tag_ids=[9],
        feature_id=9,
        content={"title": "Our unique banner)", "text": "Banner Text", "url": "https://example.com/banner"},
        is_active=True
    )
    banner_id = BannersDAO.post_banner(banner)

    assert banner_id is not None
    assert isinstance(banner_id, int)

    # Найдем этот баннер
    banner = BannersDAO.user_banner(feature_id=9, tag_id=9)
    assert banner.feature_id == 9
    assert banner.content == {"title": "Our unique banner)", "text": "Banner Text", "url": "https://example.com/banner"}
    assert isinstance(banner.banner_id, int)

    # поменяем уже созданный баннер
    update_banner = SBanner(
        tag_ids=[10, 11, 12]
    )

    BannersDAO.patch_banner(banner=update_banner, banner_id=banner_id)

    try:
        # попытаемся поменять на уже существующий тег-фичу баннер
        update_banner = SBanner(
            tag_ids=[1, 2, 3, 4, 5],
            feature_id=1
        )
        banner_id = BannersDAO.patch_banner(banner=update_banner, banner_id=banner_id)
    except Exception as e:
        assert isinstance(e, InvalidDataException)

    # удалим этот баннер, который изначально добавили
    BannersDAO.delete_banner(banner_id=banner_id)

    # Попробуем найти этот баннер
    try:
        banner = BannersDAO.user_banner(feature_id=9, tag_id=9)
    except Exception as e:
        assert isinstance(e, NotFoundException)

    # Найдем баннер из числа добавленных при создании базы
    # Например c banner_id = 1:
    # {
    #     "tag_ids": [5],
    #     "feature_id": 1,
    #     "content": {
    #         "title": "Banner 1",
    #         "text": "Some text for banner 1",
    #         "url": "https://example.com/banner1"
    #     },
    #     "is_active":true
    # }
    banner = BannersDAO.user_banner(feature_id=1, tag_id=5)
    assert banner.feature_id == 1
    assert banner.content == {
            "title": "Banner 1",
            "text": "Some text for banner 1",
            "url": "https://example.com/banner1"
        }

    # А теперь найдем этот по фильтру
    # {
    #     "tag_ids": [1,2,3,4,5],
    #     "feature_id": 6,
    #     "content": {
    #         "title": "Banner 6",
    #         "text": "Some text for banner 6",
    #         "url": "https://example.com/banner6"
    #     },
    #     "is_active":true
    # }
    banners = BannersDAO.banner(feature_id=6, tag_id=5, limit=None, offset=None)
    print(banners)
    assert isinstance(banners, list)
    banner = banners[0]
    assert banner["feature_id"] == 6
    assert banner["content"] == {
            "title": "Banner 6",
            "text": "Some text for banner 6",
            "url": "https://example.com/banner6"
        }
    # dima.tovstokor@yandex.ru =)
