from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from common.jwt.jwt import decode_access_token, oauth2_scheme, SUB
from core.lib.generic import list_view, create_view, get_view, selected_list
from core.lib.schemas.finance import FinanceView, FinanceCreateView
from db.database import get_db
from db.models.transactions import Transaction, IncomeTransaction

router = APIRouter(
    prefix="/income",
    tags=["income"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_transactions( token: Annotated[str, Depends(oauth2_scheme)], from_date: Optional[str] = None, to_date: Optional[str] = None, db: AsyncSession = Depends(get_db)) -> list[FinanceView]:
    token_data = await decode_access_token(token=token, db=db)
    expr = (IncomeTransaction.transaction_user == token_data[SUB])

    if from_date:
        from_date_parsed = datetime.fromisoformat(from_date)
        expr = and_(expr, IncomeTransaction.created_at >= from_date_parsed)

    if to_date:
        to_date_parsed = datetime.fromisoformat(to_date)
        expr = and_(expr, IncomeTransaction.created_at <= to_date_parsed)

    return await selected_list(expr, IncomeTransaction, FinanceView, db)


@router.post("/create")
async def create_transaction(token: Annotated[str, Depends(oauth2_scheme)],trans: FinanceCreateView, db: AsyncSession = Depends(get_db)) -> FinanceView:
    token_data = await decode_access_token(token=token, db=db)
    trans.transaction_user = token_data[SUB]
    print(trans)
    return await create_view(IncomeTransaction, trans, FinanceView, db)


@router.get("/detail/{finance_uuid}")
async def get_transaction(finance_uuid: str, db: AsyncSession = Depends(get_db)) -> FinanceView:
    expr = (IncomeTransaction.transaction_uuid == finance_uuid)
    return await get_view(IncomeTransaction, FinanceView, db, by_expr=expr)



