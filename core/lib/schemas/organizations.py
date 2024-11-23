from pydantic import BaseModel, Field


# class Organization(Base):
#     __tablename__ = "organization"
#     organization_uuid: Mapped[pk_id]
#     system_name: Mapped[str] = mapped_column(String(255), unique=True)
#     verbose_name: Mapped[str] = mapped_column(String(255))
#     accreditation: Mapped[Accreditation] = mapped_column(String(255))
#     description: Mapped[str] = mapped_column(String(255))


class OrganizationView(BaseModel):
    system_name: str = Field(validation_alias="system_name",alias="systemName", description="Имя организации")
    description: str = Field(description="Описание организации")
    verbose_name: str = Field(validation_alias="verbose_name", alias="verboseName", description="Имя(красивое для фронта) организации")
    accreditation: str = Field(description="Аккредитация организации")

    class Config:
        orm_mode = True
        from_attributes = True

class OrganizationCreateView(OrganizationView):
    system_name: str = Field(validation_alias="systemName",alias="system_name")
    verbose_name: str = Field(validation_alias="verboseName", alias="verbose_name")

    class Config:
        orm_mode = True
        from_attributes = True
