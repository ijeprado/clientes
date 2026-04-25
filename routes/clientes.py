from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from core.security import obter_usuario_atual
from database import get_db
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from services import cliente_service
from models.usuario import Usuario

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    print(f"Usuário {usuario.username} acessou clientes")
    return cliente_service.listar_clientes_service(db)


@router.post("/")
def criar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    return cliente_service.criar_cliente_service(db, dados)


@router.get("/{cliente_id}")
def buscar_cliente_por_id(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    return cliente_service.buscar_cliente_por_id_service(db, cliente_id)


@router.put("/{cliente_id}")
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    return cliente_service.atualizar_cliente_service(db, cliente_id, dados)


@router.delete("/{cliente_id}")
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    return cliente_service.excluir_cliente_service(db, cliente_id)
