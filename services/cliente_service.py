from fastapi import HTTPException

from models.cliente import Cliente


def serializar_cliente(cliente):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
    }


def listar_clientes_service(db):
    clientes = db.query(Cliente).all()
    return [serializar_cliente(cliente) for cliente in clientes]


def criar_cliente_service(db, dados):
    cliente = Cliente(
        nome=dados.nome,
        email=dados.email,
        telefone=dados.telefone,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return serializar_cliente(cliente)


def buscar_cliente_por_id_service(db, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return serializar_cliente(cliente)


def atualizar_cliente_service(db, cliente_id: int, dados):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nome = dados.nome
    cliente.email = dados.email
    cliente.telefone = dados.telefone
    db.commit()
    db.refresh(cliente)

    return serializar_cliente(cliente)


def excluir_cliente_service(db, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(cliente)
    db.commit()

    return {"message": "Cliente excluído com sucesso"}
