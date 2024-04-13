from .exceptions import InvalidDataException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import BannersORM, TagsORM, FeaturesORM


def check_feature_tags_combination(session, banner):
    """
    Проверка существования комбинации фичи и тегов
    """
    query = (select(BannersORM)
                .options(selectinload(BannersORM.tags))
                .filter(BannersORM.feature_id == banner.feature_id)
                .join(BannersORM.tags)
                .filter(TagsORM.tag_id.in_(banner.tag_ids))
    )

    existing_banner_response = session.execute(query)
    existing_banner = existing_banner_response.scalar()

    if existing_banner:
        raise InvalidDataException(detail="Попытка создания баннера с имеющимся сочетанием фича - тег")


def add_missing_tags(session, banner):
    """
    Добавление отсутствующих тегов в базу данных
    """
    existing_tags = session.query(TagsORM.tag_id).filter(TagsORM.tag_id.in_(banner.tag_ids)).all()
    existing_tags = {tag.tag_id for tag in existing_tags}
    missing_tags = [tag_id for tag_id in banner.tag_ids if tag_id not in existing_tags]

    for tag_id in missing_tags:
        session.add(TagsORM(tag_id=tag_id))

    session.flush()


def add_feature_if_missing(session, banner):
    """
    Добавление фичи, если она отсутствует в базе данных
    """
    feature = session.query(FeaturesORM).filter_by(feature_id=banner.feature_id).first()
    if not feature:
        session.add(FeaturesORM(feature_id=banner.feature_id))
        session.flush()
