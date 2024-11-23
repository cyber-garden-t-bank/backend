from sqlalchemy.ext.asyncio import AsyncSession


async def list_view(model_db,model_pd, db: AsyncSession):
    rows = await model_db.select_all(db)
    return [model_pd.model_validate(row) for row in rows]

async def selected_list(expr, model_db, model_pd, db: AsyncSession):
    rows = await model_db.select_by_expr(expr, db)
    return [model_pd.model_validate(row) for row in rows]

async def create_view(model_db, model_create_pd, model_out_pd, db: AsyncSession):
    row = model_db(**model_create_pd.model_dump())
    await row.save(db)
    return model_out_pd.model_validate(row)

async def get_view(model_db, model_out_pd, db: AsyncSession, model_id=None, by_expr=None):
    if not model_id==None:
        row = await model_db.find_by_id(db, model_id)
    else:
        row = await model_db.find_by_expr(db, by_expr)
    if not row:
        return
    return model_out_pd.model_validate(row)
