from pydantic import Field, BaseModel


# class Transaction(Base, TimeMixin):
#     __tablename__ = "transaction"
#     transaction_uuid: Mapped[pk_id]
#     transaction_user: Mapped[str] = mapped_column(ForeignKey("bank_user.user_uuid"))
#     transaction_card_target: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
#     transaction_source_card: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
#     amount: Mapped[float] = mapped_column(DECIMAL, default=0.0)
#     category: Mapped[str] = mapped_column(String(255))
#
#     transaction_type: Mapped[TransactionType] = mapped_column(String(255))
#     status: Mapped[str] = mapped_column(String(255), default="undefined")
#
#
#     __table_args__ = (
#         CheckConstraint("amount > 0"),
#     )
#
# class IncomeTransaction(Base, TimeMixin):
#     __tablename__ = "income_transaction"
#     transaction_uuid: Mapped[pk_id]
#     category: Mapped[IncomeTransactionCategory] = mapped_column(String(255))
#     target_card: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
#     source: Mapped[str] = mapped_column(String(255), default="none")
#     amount: Mapped[float] = mapped_column(DECIMAL, default=0.0)

class FinanceCreateView(BaseModel):
    category: str
    source: str = Field(description="Transaction uuid")
    transaction_uuid: str = Field(validation_alias="id", serialization_alias="transaction_uuid", description="Transaction uuid")
    target_card: str = Field(validation_alias="cardNumber", serialization_alias="target_card", description="Target card")
    amount: float

class FinanceView(BaseModel):
    target_card: str = Field(serialization_alias="cardNumber", validation_alias="target_card", description="Target card")
    category: str
    source: str
    transaction_uuid: str = Field(validation_alias="transaction_uuid", serialization_alias="id", description="Transaction uuid")
    amount: float



