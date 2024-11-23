
from pydantic import BaseModel, Field
from typing_extensions import Optional


class WalletView(BaseModel):
    wallet_number: str = Field(validation_alias="wallet_number", alias="walletNumber", description="Wallet number")
    balance: float = Field(description="Wallet balance")
    wallet_type: str = Field(validation_alias="wallet_number",alias="walletType", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

class WalletCreateView(BaseModel):
    user_uuid:str = Field(description="User uuid")
    wallet_number: str = Field(validation_alias="walletNumber", alias="wallet_number", description="Wallet number")
    wallet_type: str = Field(validation_alias="walletType", alias="wallet_type", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

