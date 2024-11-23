import enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.lib.types import pk_id, created_at

class Category(Base):
    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(primary_key=True)
    main_category: Mapped[int] = mapped_column(ForeignKey("category.category_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    verbose_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))


class Accreditation(str, enum.Enum):
    light = "light"
    medium = "medium"
    strong = "strong"


class Organization(Base):
    __tablename__ = "organization"
    organization_uuid: Mapped[pk_id]
    system_name: Mapped[str] = mapped_column(String(255), unique=True)
    verbose_name: Mapped[str] = mapped_column(String(255))
    accreditation: Mapped[Accreditation] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))


class Service(Base):
    __tablename__ = "service"
    service_uuid: Mapped[pk_id]
    organization_name: Mapped[pk_id] = mapped_column(ForeignKey("organization.system_name"))
    system_name: Mapped[str] = mapped_column(String(255), unique=True)
    verbose_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
