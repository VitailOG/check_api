import sqlalchemy as sa

from sqlalchemy import Identity
from sqlalchemy.dialects.postgresql import JSONB

from src.models.base import Base
from src.models.user import User


class Check(Base):
    __tablename__ = "checks"

    id = sa.Column(sa.Integer, Identity(always=True))

    user = sa.Column(sa.UnicodeText, nullable=False)

    # Один із варіантів організації даних є декомпозииція по різних таблицях
    order_details = sa.Column(JSONB, nullable=False)

    type = sa.Column(sa.UnicodeText, nullable=False)
    amount = sa.Column(sa.Numeric(precision=8, scale=3), nullable=False)

    rest = sa.Column(sa.Numeric(precision=8, scale=3), nullable=False)
    total = sa.Column(sa.Numeric(precision=8, scale=3), nullable=False)

    created_at = sa.Column(
        sa.DateTime, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint((user,), (User.username,))
    )
