from pydantic import BaseModel, Field


class WalletView(BaseModel):
    wallet_number: str = Field(validation_alias="wallet_number", serialization_alias="walletNumber", description="Wallet number")
    balance: float = Field(description="Wallet balance")
    wallet_type: str = Field(validation_alias="wallet_number",serialization_alias="walletType", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

class WalletCreateView(BaseModel):
    wallet_number: str = Field(validation_alias="wallet_number", alias="walletNumber", description="Wallet number")
    wallet_type: str = Field(validation_alias="wallet_number",alias="walletType", description="Wallet type")

    class Config:
        orm_mode = True
        from_attributes = True

class WalletUserRequiredView(WalletView):
    user_uuid: str = Field(validation_alias="user_uuid", alias="userUUID", description="User uuid")
    wallet_number: str = Field(validation_alias="wallet_number", alias="walletNumber", description="Wallet number")
    wallet_type: str = Field(validation_alias="wallet_number",alias="walletType", description="Wallet type")