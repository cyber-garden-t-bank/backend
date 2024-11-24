from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession



from core.lib.generic import list_view, create_view, get_view
from core.lib.schemas.organizations import OrganizationView, OrganizationCreateView
from db.database import get_db
from db.models.organizations import Organization

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_organizations(db: AsyncSession = Depends(get_db)) -> list[OrganizationView]:
    return await list_view(Organization, OrganizationView, db)

@router.post("/create")
async def create_organization(organization: OrganizationCreateView, db: AsyncSession = Depends(get_db)) -> OrganizationView:
    return await create_view(Organization, organization,OrganizationView, db)


@router.get("/detail/{organization_name}")
async def get_organization(organization_name: str, db: AsyncSession = Depends(get_db)) -> OrganizationView:
    expr = (Organization.system_name == organization_name)
    return await get_view(Organization, OrganizationView, db, by_expr= expr)