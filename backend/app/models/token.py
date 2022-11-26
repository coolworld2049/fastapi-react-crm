import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as ps

from backend.app.db.base_class import Base


class Token(Base):
    sub = sa.Column(ps.INTEGER, sa.ForeignKey("user.id"), primary_key=True, nullable=False)
    access_token = sa.Column(ps.TEXT, unique=True)
    expires_in = sa.Column(sa.DateTime(timezone=False))
    token_type = sa.Column(ps.TEXT)
