from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
