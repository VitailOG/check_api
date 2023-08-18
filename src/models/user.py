import sqlalchemy as sa

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    username = sa.Column(sa.UnicodeText, nullable=False)

    name = sa.Column(sa.UnicodeText, nullable=False)

    password = sa.Column(sa.UnicodeText, nullable=False)

    __table_args__ = (sa.PrimaryKeyConstraint("username"),)
