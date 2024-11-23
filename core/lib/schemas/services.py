from pydantic import Field, BaseModel


# class Service(Base):
#     __tablename__ = "service"
#     service_uuid: Mapped[pk_id]
#     organization_name: Mapped[pk_id] = mapped_column(ForeignKey("organization.system_name"))
#     system_name: Mapped[str] = mapped_column(String(255), unique=True)
#     description: Mapped[str] = mapped_column(String(255))
#     verbose_name: Mapped[str] = mapped_column(String(255))

class ServiceCreateView(BaseModel):
    system_name: str = Field(validation_alias="system_name",alias="systemName", description="Имя услуги")
    organization_name: str = Field(validation_alias="organization_name",alias="organizationName", description="Имя организации")
    description: str = Field(description="Описание услуги")
    verbose_name: str = Field(validation_alias="verbose_name", alias="verboseName", description="Имя(красивое для фронта) услуги")
