import json
import pytest
from sqlalchemy import insert, select
from app.banners.schemas import SBanner
from app.banners.services import check_feature_tags_combination, add_missing_tags, add_feature_if_missing
from app.config import settings
from app.database import Base, session_factory, sync_engine
from app.banners.models import FeaturesORM, BannersORM, TagsORM, Banners_TagsORM

from fastapi.testclient import TestClient
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    assert settings.MODE == "TEST"

    with sync_engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    banners = open_mock_json("banners")

    with session_factory() as session:
        unique_features = set()
        unique_tags = set()
        for banner_data in banners:
            # Создаем объекты FeaturesORM, TagsORM и BannersORM для каждого баннера
            feature_id = banner_data["feature_id"]
            tag_ids = banner_data["tag_ids"]
            content = banner_data["content"]
            is_active = banner_data["is_active"]

            feature = FeaturesORM(feature_id=feature_id)
            if feature_id not in unique_features:
                session.add(feature)
            unique_features.add(feature_id)

            tags = [TagsORM(tag_id=tag_id) for tag_id in tag_ids if tag_id not in unique_tags]

            session.add_all(tags)
            session.flush()

            banner = BannersORM(
                feature_id=feature_id,
                content=content,
                is_active=is_active
            )
            tags = session.execute(select(TagsORM).filter(TagsORM.tag_id.in_(tag_ids))).scalars().all()
            for tag in tags:
                tag.banners.append(banner)

            unique_tags.update(tag_ids)
            session.add(banner)

        session.commit()


@pytest.fixture(scope="function")
def c():
    with TestClient(app=fastapi_app, base_url="http://test") as c:
        yield c
