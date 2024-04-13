from .exceptions import InvalidDataException
from sqlalchemy import select
from app.database import session_factory
from app.banners.models import FeaturesORM, BannersORM, TagsORM
from sqlalchemy.orm import selectinload, joinedload
from app.banners.schemas import SBanner


class BannersDAO:
    @staticmethod
    def user_banner(feature_id, tag_id):
        with session_factory() as session:
            query = (select(BannersORM)
                     .options(selectinload(BannersORM.tags))
                     .filter(BannersORM.feature_id == feature_id)
                     .join(BannersORM.tags)
                     .filter(TagsORM.tag_id == tag_id)
            )

            response = session.execute(query)
            banner = response.scalar()

            return banner.content if banner else None

    @staticmethod
    def banner(feature_id, tag_id, limit, offset):
        with session_factory() as session:
            query = (select(BannersORM)
                     .options(selectinload(BannersORM.tags)))
            if feature_id is not None:
                query = query.filter(BannersORM.feature_id == feature_id)
            if tag_id is not None:
                query = query.join(BannersORM.tags).filter(TagsORM.tag_id == tag_id)

            query = query.limit(limit).offset(offset)

            response = session.execute(query)
            banners = response.scalars().all()

            # Собираем результат в нужном формате
            result = []
            for banner in banners:
                banner_dict = {
                    "banner_id": banner.banner_id,
                    "tag_ids": [tag.tag_id for tag in banner.tags],  # Собираем список идентификаторов тегов
                    "feature_id": banner.feature_id,
                    "content": banner.content,
                    "is_active": banner.is_active,
                    "created_at": banner.created_at,
                    "updated_at": banner.updated_at,
                }
                result.append(banner_dict)

            return result

    @staticmethod
    def post_banner(banner: SBanner):
        '''К БД выполняется 6 запросов:
        1. Проверка что такого сочетания фичи и каждого тега в списке нет в бд
        2. Поиск всех тегов, которые необходимо добавить в БД, которых нет
        3. Добавление новых тегов, если нет
        4. Поиск фичи
        5. Добавление фичи, если нет
        6. Поиск тегов к которым нужно добавить баннер
        7. Добавление баннера'''
        with session_factory() as session:
            # 1. Проверка сочетания фичи и каждого тега
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

            # 2. Поиск всех тегов, которые необходимо добавить
            existing_tags = session.query(TagsORM.tag_id).filter(TagsORM.tag_id.in_(banner.tag_ids)).all()
            existing_tags = {tag.tag_id for tag in existing_tags}
            missing_tags = [tag_id for tag_id in banner.tag_ids if tag_id not in existing_tags]
            # 3. Добавление новых тегов
            for tag_id in missing_tags:
                session.add(TagsORM(tag_id=tag_id))
            session.flush()

            # 4. Поиск фичи
            feature = session.query(FeaturesORM).filter_by(feature_id=banner.feature_id).first()
            # 5. Добавление фичи
            if not feature:
                session.add(FeaturesORM(feature_id=banner.feature_id))
                session.flush()

            # Определение баннера
            new_banner = BannersORM(
                content=banner.content,
                is_active=banner.is_active,
                feature_id=banner.feature_id,
            )

            # 6. Поиск тегов к которым нужно добавить баннер
            tags = session.execute(select(TagsORM).filter(TagsORM.tag_id.in_(banner.tag_ids))).scalars().all()
            for tag in tags:
                tag.banners.append(new_banner)

            # 7. Добавление баннера
            session.add(new_banner)
            session.commit()

            return new_banner.banner_id
