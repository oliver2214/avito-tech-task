from sqlalchemy import select
from app.database import session_factory
from app.banners.models import FeaturesORM, BannersORM, TagsORM
from sqlalchemy.orm import selectinload, joinedload


class BannersDAO:
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
