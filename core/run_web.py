import os

from fastapi import FastAPI
import uvicorn

from core.routes.card import router as router_cards
from core.routes.income import router as router_income
from core.routes.wallet import router as router_wallet
from core.routes.services import router as router_services
from core.routes.organization import router as router_organizations
from core.routes.transactions import router as router_transactions
from core.routes.finance import router as router_finance
from core.routes.expense import router as router_expense
from core.routes.media import router as router_media
# from core.routes.kafka.test import router as router_kafka

from fastapi import Response


app = FastAPI()


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = Response()

    if request.method == "OPTIONS":
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response


app.include_router(router_income)
app.include_router(router_cards)
app.include_router(router_wallet)
app.include_router(router_organizations)
app.include_router(router_services)
app.include_router(router_transactions)
app.include_router(router_finance)
app.include_router(router_expense)
app.include_router(router_media)
# app.include_router(router_kafka)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #для запуска через консоль с перезагрузкой сервера на том же порту и хосте: uvicorn run_web:app --reload --host 0.0.0.0 --port 8000
