import uuid

from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from db.models.lib.types import pk_id, created_at, updated_at




class AttributeMixin:
    id: Mapped[pk_id]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class User(Base, AttributeMixin):
    __tablename__ = "user"

