from pydantic import BaseModel, Field



class IncomeTransactionView(BaseModel):
    category: str = Field(description="Откуда деньги")
    amount: float = Field(description="Сумма")
    target_card: int = Field(alias="targetCard", description="Номер кaрты")

    class Config:
        orm_mode = True
        from_attributes = True

class IncomeBillView(BaseModel):
    category: str = Field(description="Откуда деньги")
    amount: float = Field(description="Сумма")
    target_card: int = Field(alias="targetСard", description="Номер карты")

    class Config:
        orm_mode = True
        from_attributes = True



