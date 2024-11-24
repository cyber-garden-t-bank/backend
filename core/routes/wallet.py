from collections import defaultdict
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from common.exceptions import BadRequestException, ForbiddenException
from common.jwt.jwt import oauth2_scheme, decode_access_token, SUB
from core.lib.generic import list_view, create_view, get_view, selected_list, create_view_from_dict
from core.lib.schemas.wallet import WalletView, WalletCreateView, WalletInsertView, WalletRowsView
from db.database import get_db
from db.models.finance import Wallet, Card
from db.models.users import User


router = APIRouter(
    prefix="/wallet",
    tags=["wallets"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_wallets(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    token_data = await decode_access_token(token=token, db=db)

    query = (
        select(Wallet)
        .outerjoin(Card, Card.wallet_number == Wallet.wallet_number)
        .where(Wallet.user_uuid == token_data[SUB])
    )

    result = await db.execute(query)
    rows = result.scalars().all()

    print(rows)

    # Создаем словарь для группировки карточек по кошелькам
    wallet_dicts = []

    cards_dict = []

    for row in rows:
        if row.Wallet.wallet_number not in wallet_dicts:
            wallet_dicts.append(row.Wallet.wallet_number)
        if row.Card is not None:
            cards_dict.append(row.Card)

    joined_dicts = []

    for wallet in wallet_dicts:
        for card in cards_dict:
            if card.wallet_number == wallet.wallet_number:
                joined_dicts.append({**wallet, "card":card})


    return joined_dicts




@router.post("/create")
async def create_wallet(token: Annotated[str, Depends(oauth2_scheme)],wallet: WalletCreateView, db: AsyncSession = Depends(get_db)):
    token_data = await decode_access_token(token=token, db=db)
    expr = (User.user_uuid == token_data[SUB])
    user = await User.find_by_expr(db=db, expr=expr)

    if not user:
        raise ForbiddenException("User not found")

    wallet = wallet.model_dump()
    wallet["user_uuid"] = token_data[SUB]

    return await create_view_from_dict(Wallet, wallet, db)


@router.get("/detail/{wallet_number}")
async def get_wallet(wallet_number: str, db: AsyncSession = Depends(get_db)) -> WalletView:
    expr = (Wallet.wallet_number == wallet_number)
    return await get_view(Wallet, WalletView, db, by_expr= expr)