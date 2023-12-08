from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from src.models.auth_models import user

metadata = MetaData()

transaction_stat = Table(
    "trans_status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False)
)

transaction = Table(
    "transaction",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fromUser", Integer, ForeignKey(user.c.id), nullable=False),
    Column("toUser", Integer, ForeignKey(user.c.id), nullable=False),
    Column("amountOf", String, nullable=False),
    Column("status", Integer, ForeignKey(transaction_stat.c.id), nullable=False),
)

message_status= Table(
    "message_status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fromUser", Integer, ForeignKey(user.c.id)),
    Column("text", String, nullable=False),
    Column("message_status", Integer, ForeignKey(message_status.c.id)),
)

