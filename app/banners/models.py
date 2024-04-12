import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import JSON


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)]


class FeaturesORM(Base):
    __tablename__ = "features"
    feature_id: Mapped[intpk]

    banners: Mapped["BannersORM"] = relationship(
        back_populates="feature"
    )


class BannersORM(Base):
    __tablename__ = "banners"
    banner_id: Mapped[intpk]
    content: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=text("false"))
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.feature_id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    feature: Mapped["FeaturesORM"] = relationship(
        back_populates="banners"
    )

    tags: Mapped[list["TagsORM"] | None] = relationship(
        back_populates="banners",
        secondary="banners_tags"
    )


class TagsORM(Base):
    __tablename__ = "tags"
    tag_id: Mapped[intpk]

    banners: Mapped[list["BannersORM"] | None] = relationship(
        back_populates="tags",
        secondary="banners_tags"
    )


class Banners_TagsORM(Base):
    __tablename__ = "banners_tags"
    banner_id: Mapped[intpk] = mapped_column(
        ForeignKey("banners.banner_id", ondelete="CASCADE"),
        primary_key=True
    )
    tag_id: Mapped[intpk] = mapped_column(
        ForeignKey("tags.tag_id", ondelete="CASCADE"),
        primary_key=True
    )
