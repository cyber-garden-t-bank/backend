from pydantic import BaseModel, Field


class CardView(BaseModel):
    card_number: str = Field(validation_alias="card_number", alias="cardNumber", description="Card number")
    wallet_number: str = Field(validation_alias="wallet_number", alias="walletNumber", description="Wallet uuid")
    balance: float = Field(description="Card balance")
    expiration_date: str = Field(validation_alias="expiration_date", alias="expirationDate", description="Card expiration date")
    card_type: str   = Field(validation_alias="card_type", alias="cardType", description="Card type")

    class Config:
        orm_mode = True
        from_attributes = True

class CardCreateView(BaseModel):
    wallet_number: str = Field(serialization_alias="wallet_number", validation_alias="walletNumber",
                               description="Wallet number")
    card_type: str = Field(serialization_alias="card_type", validation_alias="cardType", description="Card type")

    class Config:
        orm_mode = True
        from_attributes = True

class CardInsertView(BaseModel):
    wallet_number: str = Field(serialization_alias="wallet_number", validation_alias="walletNumber", description="Wallet number")
    card_type: str = Field(serialization_alias="card_type", validation_alias="cardType", description="Card type")
    card_number: str = Field(serialization_alias="card_number", validation_alias="cardNumber", description="Card number")
    expiration_date: str = Field(serialization_alias="expiration_date", validation_alias="expirationDate", description="Card expiration date")

    class Config:
        orm_mode = True
        from_attributes = True

