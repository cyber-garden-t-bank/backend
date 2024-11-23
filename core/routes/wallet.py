from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from common.exceptions import BadRequestException, ForbiddenException
from common.jwt.jwt import oauth2_scheme, decode_access_token, SUB
from core.lib.generic import list_view, create_view, get_view, selected_list
from core.lib.schemas.wallet import WalletView, WalletCreateView, WalletUserRequiredView
from db.database import get_db
from db.models.finance import Wallet
from db.models.users import User

router = APIRouter(
    prefix="/wallet",
    tags=["wallets"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_wallets(token: Annotated[str, Depends(oauth2_scheme)],db: AsyncSession = Depends(get_db)) -> list[WalletView]:
    token_data = await decode_access_token(token=token, db=db)
    expr = (Wallet.user_uuid == token_data[SUB])
    return await selected_list(expr, Wallet, WalletView, db)



@router.post("/create")
async def create_wallet(token: Annotated[str, Depends(oauth2_scheme)],wallet: WalletCreateView, db: AsyncSession = Depends(get_db)) -> WalletView:
    token_data = await decode_access_token(token=token, db=db)
    expr = (User.user_uuid == token_data[SUB])
    user = await User.find_by_expr(db=db, expr=expr)

    if not user:
        raise ForbiddenException("User not found")

    wallet = WalletCreateView(user_uuid=user.user_uuid, wallet_number=wallet.wallet_number, wallet_type=wallet.wallet_type)

    return await create_view(Wallet, wallet, WalletUserRequiredView, db)


@router.get("/detail/{wallet_number}")
async def get_wallet(wallet_number: str, db: AsyncSession = Depends(get_db)) -> WalletView:
    expr = (Wallet.wallet_number == wallet_number)
    return await get_view(Wallet, WalletView, db, by_expr= expr)