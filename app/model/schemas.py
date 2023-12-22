from datetime import datetime
from pydantic import BaseModel

"""
This file contains the schemas of the models

"""


class MessageIn(BaseModel):

    """
    MessageIn is the schema of the message model    
    """

    text: str
    role: str
    sentAt: str


class DebtsIn(BaseModel):
    
    """
    DebtsIn is the schema of the debts model
    """

    institution: str
    amount: int
    dueDate: str


class MessageOut(MessageIn):

    """
    MessageOut is the schema of the message model
    """
    id: int
    sentAt: datetime

    class Config:
        orm_mode = True


class DebtsOut(DebtsIn):
    
    """
    DebtsOut is the schema of the debts model
    """

    id: int
    dueDate: datetime

    class Config:
        orm_mode = True


class ClientIn(BaseModel):

    """
    ClientIn is the schema of the client model
    """
    name: str
    rut: str
    salary: int
    savings: int
    messages: list[MessageIn] = []
    debts: list[DebtsIn] = []


class ClientOut(BaseModel):

    """
    ClientOut is the schema of the client model
    """
    id: int
    name: str
    rut: str
    salary: int
    savings: int
    messages: list[MessageOut] = []
    debts: list[DebtsOut] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            bytes: lambda b: b.decode(),
        }
