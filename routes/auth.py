from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.auth import LoginRequest, UsuarioCreate
from services.auth_service import criar_usuario_service, login_service

router = APIRouter(tags=["Autenticação"])


@router.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario_service(db, usuario)


@router.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, dados)
