from datetime import datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    userTo: int
    amount: str


class Message(BaseModel):
    text: str


class MessageUpd(BaseModel):
    text: str
    message_status: int


class TransactionUpd(BaseModel):
    status: int
