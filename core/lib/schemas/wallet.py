import uuid

from pydantic import BaseModel, Field



class WalletView(BaseModel):
    wallet_number: str = Field(alias="walletNumber", description="Wallet number")
    balance: float = Field(description="Wallet balance")
    wallet_type: str = Field(alias="walletType", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

class WalletCreateView(BaseModel):
    wallet_number: str = Field(validation_alias="walletNumber", alias="wallet_number", description="Wallet number")
    wallet_type: str = Field(validation_alias="walletType", alias="wallet_type", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

class WalletInsertView(BaseModel):
    user_uuid: uuid.UUID = Field( description="User  uuid")
    wallet_number: str = Field(validation_alias="walletNumber", alias="wallet_number", description="Wallet number")
    wallet_type: str = Field(validation_alias="walletType", alias="wallet_type", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True


