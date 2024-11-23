
from datetime import datetime
from pydantic import BaseModel, PositiveInt, field_validator, EmailStr, UUID4, Field


# class User(Base, AttributeMixin):
#     __tablename__ = "user"
#     user_uuid: Mapped[pk_id]
#     email: Mapped[str] = mapped_column(String(255), unique=True)
#     phone: Mapped[str] = mapped_column(String(255), unique=True)
#     firstname: Mapped[str] = mapped_column(String(255))
#     middlename: Mapped[str] = mapped_column(String(255))
#     lastname: Mapped[str] = mapped_column(String(255))
#     password: Mapped[str]
#     birthday: Mapped[str] = mapped_column(String(255))
#     gender: Mapped[str] = mapped_column(String(255))
#     account_status: Mapped[str] = mapped_column(String(255))


class UserBase(BaseModel):
    email: EmailStr
    phone: str
    firstname: str
    middlename: str
    lastname: str
    password: str


class UserCreate(UserBase):
    password: str


class User(UserBase):

    class Config:
        orm_mode = True
        from_attributes = True



class UserRegister(UserBase):
    password: str
    confirm_password: str = Field(alias="repeatPassword")
    class Config:
        orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime

    class Config:
        orm_mode = True
        from_attributes = True



class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema

    class Config:
        orm_mode = True
        from_attributes = True




class RefreshToken(BaseModel):
    refresh: str

    class Config:
        orm_mode = True
        from_attributes = True

class AccessToken(BaseModel):
    access: str

    class Config:
        orm_mode = True
        from_attributes = True
class SuccessResponseScheme(BaseModel):
    msg: str

    class Config:
        orm_mode = True
        from_attributes = True


class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

