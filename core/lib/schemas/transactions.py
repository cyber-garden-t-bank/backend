from pydantic import BaseModel, Field


class _Transaction(BaseModel):
    amount: float = Field(description="Transaction amount")
    status: str = Field(description="Transaction status")

# class IncomeTransaction(Base, TimeMixin):
#     __tablename__ = "income_transaction"
#     transaction_uuid: Mapped[pk_id]
#     category: Mapped[IncomeTransactionCategory] = mapped_column(String(255))
#     target_card: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
#     amount: Mapped[float] = mapped_column(DECIMAL, default=0.0)

class _IncomeTransaction(BaseModel):
    amount: float = Field(description="Transaction amount")
    category: str = Field(description="Transaction category")


class TransactionView(_Transaction):
    transaction_uuid: str = Field(validation_alias="transaction_uuid", alias="transactionUuid", description="Transaction uuid")
    status: str = Field(description="Transaction status")

    transaction_card_target: str = Field(validation_alias="transaction_card_target", alias="transactionCardTarget",
                                         description="Transaction card target")
    transaction_source_card: str = Field(validation_alias="transaction_source_card", alias="transactionSourceCard",
                                         description="Transaction source card")
    transaction_type: str = Field(validation_alias="transaction_type", alias="transactionType",
                                  description="Transaction type")

    created_at: str = Field(validation_alias="created_at", alias="createdAt", description="Created at")
    updated_at: str = Field(validation_alias="updated_at", alias="updatedAt", description="Updated at")

    class Config:
        orm_mode = True
        from_attributes = True


class TransactionCreateView(_Transaction):
    transaction_type: str = Field(validation_alias="transactionType", alias="transaction_type", description="Transaction type")
    transaction_card_target: str = Field(validation_alias="transactionCardTarget", alias="transaction_card_target", description="Transaction card target")
    transaction_source_card: str = Field(validation_alias="transactionSourceCard", alias="transaction_source_card", description="Transaction source card")


    class Config:
        orm_mode = True
        from_attributes = True





class IncomeTransactionView(_IncomeTransaction):
    transaction_uuid: str = Field(validation_alias="transaction_uuid", alias="transactionUuid", description="Transaction uuid")

    created_at: str = Field(validation_alias="created_at", alias="createdAt", description="Created at")
    updated_at: str = Field(validation_alias="updated_at", alias="updatedAt", description="Updated at")

    class Config:
        orm_mode = True