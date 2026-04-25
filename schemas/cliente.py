from pydantic import BaseModel, EmailStr
from typing import Optional


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    pass


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True
