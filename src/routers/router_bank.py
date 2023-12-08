from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.bank_models import transaction, transaction_stat, messages, message_status
from src.schemas.bank_schemas import TransactionCreate, Message, MessageUpd, TransactionUpd
from src.configs.cur_user import current_user
from src.database.database import get_async_session

from src.models.auth_models import user, role

router = APIRouter(
    prefix="/bank",
    tags=["Bank"]
)


@router.get("/about_me")
async def about_me(user1: user = Depends(current_user)):
    return {
        "email": user1.email,
        "username": user1.username,
        "amount": user1.amount,
        "registered_at": user1.registered_at}


@router.get("/user_transactions")
async def get_transactions(user1: user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    # j = join(transaction, transaction_stat, transaction.c.status == transaction_stat.c.id)
    stmt = transaction.join(transaction_stat, transaction.c.status == transaction_stat.c.id)
    stmt = stmt.select().where(transaction.c.fromUser == user1.id)
    a = await session.execute(stmt)

    # query = select(transaction).select_from(j).where(transaction.c.fromUser == user.id)
    # result = await session.execute(query)
    fin = []
    i = 0
    for item in a.all():
        fin.append(
            {
                "number": i,
                "from_user": item[1],
                "to_user": item[2],
                "amount": item[3],
                "status": item[6]
            }
        )
        i+=1
    return fin


@router.post("/add_transaction")
async def add_transactions(tr: TransactionCreate, user1: user = Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)):
    if float(tr.amount) > float(user1.amount) and float(tr.amount) > 0:
        raise HTTPException(status_code=404, detail='insufficient funds')
    if tr.userTo == user1.id:
        raise HTTPException(status_code=404, detail='you need to enter another user')
    userTo = await session.execute(select(user).where(user.c.id == tr.userTo))
    if userTo:
        trans = dict(toUser=tr.userTo, amountOf=tr.amount, fromUser=user1.id, status=1)
        stam = insert(transaction).values(trans)
        await session.execute(stam)
        user1.amount = str(float(user1.amount) - float(tr.amount))
        userToAm = str(float(userTo.first()[3]) + float(tr.amount))
        stmt = (user.update().where(user.c.id == tr.userTo).values(amount=userToAm))
        await session.execute(stmt)
        await session.commit()
        return {"message": "success"}
    else:
        raise HTTPException(status_code=404, detail='user not found')


@router.get("/get_messages")
async def get_messages(user1: user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = messages.join(message_status, messages.c.message_status == message_status.c.id)
    stmt = stmt.select().where(messages.c.fromUser == user1.id)
    a = await session.execute(stmt)
    fin = []
    for item in a.all():
        print(item)
        fin.append(
            {
                "from user": item[1],
                "message": item[2],
                "status": item[5],
            }
        )
    return fin


@router.post("/add_message")
async def add_message(ms: Message, user1: user = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if len(ms.text) < 20:
        raise HTTPException(status_code=404, detail='enter more than 20 symbols')
    stam = insert(messages).values(dict({
        "fromUser": user1.id,
        "text": ms.text,
        "message_status": 2
    }))
    await session.execute(stam)
    await session.commit()
    return {"message": "success"}


router_admin = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/")
async def get_bank():
    return


@router_admin.get("/get_users")
async def admin_get_users(user1: user = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    if user1.role_id == 2:
        stmt = user.join(role, role.c.id == user.c.role_id)
        stmt = stmt.select()
        a = await session.execute(stmt)
        fin = []
        for item in a.all():
            print(item)
            fin.append(
                {
                    "id": item[0],
                    "email": item[1],
                    "username": item[2],
                    "amount": item[3],
                    "registered_at": item[4],
                }
            )
        return fin
    else:
        raise HTTPException(status_code=404, detail="you have no rights")


@router_admin.get("/get_transactions")
async def admin_get_transactions(user1: user = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)):
    if user1.role_id == 2:
        stmt = transaction.join(transaction_stat, transaction.c.status == transaction_stat.c.id)
        stmt = stmt.select()
        a = await session.execute(stmt)
        fin = []
        for item in a.all():
            fin.append(
                {
                    "id": item[0],
                    "from user": item[1],
                    "to user": item[2],
                    "amount": item[3],
                    "status": item[6]
                }
            )
        return fin
    else:
        raise HTTPException(status_code=404, detail="you have no rights")


@router_admin.get("/get_messages")
async def admin_get_messages(user1: user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if user1.role_id == 2:
        stmt = messages.join(message_status, messages.c.message_status == message_status.c.id)
        stmt = stmt.select()
        a = await session.execute(stmt)
        fin = []
        for item in a.all():
            print(item)
            fin.append(
                {
                    "id": item[0],
                    "from user": item[1],
                    "message": item[2],
                    "status": item[5],
                }
            )
        return fin
    else:
        raise HTTPException(status_code=404, detail="you have no rights")



@router_admin.delete("/delete_message/{message_id}")
async def delete_message(message_id: int, user1: user = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    pass


@router_admin.delete("/delete_transaction/{transaction_id}")
async def delete_transaction(transaction_id: int, user1: user = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    pass


@router_admin.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, user1: user = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    pass



@router_admin.put("/delete_user/{user_id}")
async def update_user(user_id: int, user1: user = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    pass


@router_admin.put("/update_message/{message_id}")
async def update_message(message_id: int, upd: MessageUpd, user1: user = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    if user1.role_id == 2:
        st = select(messages).where(messages.c.id == message_id)
        mes = await session.execute(st)
        mes = mes.first()
        if mes:
            mes = mes[2] + f"\nAnswer: {upd.text}"
            stmt = (messages.update().where(messages.c.id == message_id).values(text=mes,
                                                                                message_status=upd.message_status))
            await session.execute(stmt)
            await session.commit()
            return {"detail": "successful update"}, upd.dict()
        else:
            raise HTTPException(status_code=404, detail="message not found")
    else:
        raise HTTPException(status_code=404, detail="you have no rights")


@router_admin.put(f"/update_transaction/transaction_id")
async def update_transaction(transaction_id: int, upd: TransactionUpd, user1: user = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    if user1.role_id == 2:
        st = select(transaction).where(transaction.c.id == transaction_id)
        tr = await session.execute(st)
        tr = tr.first()
        if tr:
            if tr[4] != upd.status:
                stat = (transaction.update().where(transaction.c.id == transaction_id).values(
                    status=upd.status))
                userFrom = await session.execute(select(user).where(user.c.id == tr[1]))
                userTo = await session.execute(select(user).where(user.c.id == tr[2]))
                if upd.status == 1:
                    userFromAmount = str(float(userFrom.first()[3]) - float(tr[3]))
                    userToAmount = str(float(userTo.first()[3]) + float(tr[3]))
                    mes = {"detail": "successful apply transaction"}
                else:
                    userFromAmount = str(float(userFrom.first()[3]) + float(tr[3]))
                    userToAmount = str(float(userTo.first()[3]) - float(tr[3]))
                    mes = {"detail": "successful cancelling of transaction"}
                stmtUs1 = (user.update().where(user.c.id == tr[1]).values(amount=userFromAmount))
                stmtUs2 = (user.update().where(user.c.id == tr[2]).values(amount=userToAmount))
                await session.execute(stmtUs1)
                await session.execute(stmtUs2)
                await session.execute(stat)
                await session.commit()
                return mes
            else:
                return {"detail": "nothing to update"}

        else:
            raise HTTPException(status_code=404, detail="transaction not found")
    else:
        raise HTTPException(status_code=404, detail="you have no rights")
