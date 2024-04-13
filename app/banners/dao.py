from sqlalchemy import select
from .exceptions import NotFoundException
from app.database import session_factory
from .models import FeaturesORM, BannersORM, TagsORM
from sqlalchemy.orm import selectinload
from .schemas import SBanner
from .services import *


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
        '''К БД выполняется 7 запросов:
        1. Проверка что такого сочетания фичи и каждого тега в списке нет в бд
        2. Поиск всех тегов, которые необходимо добавить в БД, которых нет
        3. Добавление новых тегов, если нет
        4. Поиск фичи
        5. Добавление фичи, если нет
        6. Поиск тегов к которым нужно добавить баннер
        7. Добавление баннера'''
        with session_factory() as session:
            # 1. Проверка сочетания фичи и каждого тега
            check_feature_tags_combination(session, banner)

            # 2 - 3. Поиск всех тегов, которых еще нет в БД и добавление их в базу
            add_missing_tags(session, banner)

            # 4 - 5. Поиск фичи и добавление при ее отсутствии
            add_feature_if_missing(session, banner)

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

    @staticmethod
    def patch_banner(banner_id, banner: SBanner):
        with session_factory() as session:
            # 1. Проверка сочетания фичи и каждого тега
            if banner.tag_ids and banner.feature_id:
                check_feature_tags_combination(session, banner)

            # 2 - 3. Поиск всех тегов, которых еще нет в БД и добавление их в базу
            if banner.tag_ids:
                add_missing_tags(session, banner)

            # 4 - 5. Поиск фичи и добавление при ее отсутствии
            if banner.feature_id:
                add_feature_if_missing(session, banner)

            # Получение существующего баннера
            existing_banner = session.get(BannersORM, banner_id)
            if not existing_banner:
                raise NotFoundException(detail="Баннер не найден")

            # Обновление параметров баннера, если они переданы и не являются None
            if banner.tag_ids:
                tags = session.execute(select(TagsORM).filter(TagsORM.tag_id.in_(banner.tag_ids))).scalars().all()
                existing_banner.tags.clear()  # Очищаем старые теги
                for tag in tags:
                    tag.banners.append(existing_banner)

            if banner.feature_id is not None:
                existing_banner.feature_id = banner.feature_id

            if banner.content is not None:
                existing_banner.content = banner.content

            if banner.is_active is not None:
                existing_banner.is_active = banner.is_active

            session.commit()

    @staticmethod
    def delete_banner(banner_id):
        with session_factory() as session:
            banner = session.get(BannersORM, banner_id)
            if not banner:
                raise NotFoundException(detail="Баннер не найден")

            session.delete(banner)
            session.commit()
