from sqlalchemy import select
from app.database import session_factory
from app.banners.models import FeaturesORM, BannersORM, TagsORM
from sqlalchemy.orm import selectinload, joinedload


class BannersDAO:
    @staticmethod
    def banner(feature_id, tag_id, limit, offset):
        with session_factory() as session:
            query = select(BannersORM)
            if feature_id is not None:
                query = query.filter(BannersORM.feature_id == feature_id)
            if tag_id is not None:
                query = query.join(BannersORM.tags).filter(TagsORM.tag_id == tag_id)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)

            response = session.execute(query)
            result = response.scalars().all()
            return result
