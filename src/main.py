from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.configs.base_config import auth_backend, fastapi_users
from src.models.auth_models import user
from src.schemas.auth_schemas import UserRead, UserCreate

from src.routers.router_bank import router as bank_router
from src.routers.router_bank import router_admin
from src.configs.cur_user import current_user
from src.routers.page_router import router as router_pages




app = FastAPI(
    title="Банк народного благосостояния "
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: user = Depends(current_user)):
    return f"Hello, {user.username}, your amount {user.amount}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


#
# @app.get("/admin/get_messages")
# async def admin_get_messages(user: user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
#     if user.role_id == 2:
#         stmt = messages.join(message_status, messages.c.message_status == message_status.c.id)
#         stmt = stmt.select()
#         a = await session.execute(stmt)
#         fin = []
#         for item in a.all():
#             print(item)
#             fin.append(
#                 {
#                     "from user": item[1],
#                     "message": item[2],
#                     "status": item[5],
#                 }
#             )
#         return fin
#     else:
#         raise HTTPException(status_code=404, detail="you have no rights")

#
# @app.get("/admin/get_transactions")
# async def admin_get_transactions(user: user = Depends(current_user),
#                                  session: AsyncSession = Depends(get_async_session)):
#     if user.role_id == 2:
#         stmt = transaction.join(transaction_stat, transaction.c.status == transaction_stat.c.id)
#         stmt = stmt.select()
#         a = await session.execute(stmt)
#         fin = []
#         for item in a.all():
#             print(item)
#             fin.append(
#                 {
#                     "from user": item[1],
#                     "to user": item[2],
#                     "amount": item[3],
#                     "status": item[6]
#                 }
#             )
#         return fin
#     else:
#         raise HTTPException(status_code=404, detail="you have no rights")

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(bank_router)
app.include_router(router_admin)
app.include_router(router_pages)