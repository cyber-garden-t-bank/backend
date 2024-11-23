from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from core.lib.generic import list_view, create_view, get_view
from core.lib.schemas.services import ServiceCreateView, ServiceView

from db.database import get_db
from db.models.organizations import Service

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_services(db: AsyncSession = Depends(get_db)) -> list[ServiceView]:
    return await list_view(Service, ServiceView, db)

@router.post("/create")
async def create_wallet(wallet: ServiceCreateView, db: AsyncSession = Depends(get_db)) -> ServiceView:
    return await create_view(Service, wallet, ServiceView, db)


@router.get("/detail/{service_name}")
async def get_wallet(service_name: str, db: AsyncSession = Depends(get_db)) -> ServiceView:
    expr = (Service.system_name == service_name)
    return await get_view(Service, ServiceView, db, by_expr= expr)