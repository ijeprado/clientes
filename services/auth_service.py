from fastapi import HTTPException

from models.usuario import Usuario
from core.security import criar_token, gerar_hash_senha, verificar_senha


def criar_usuario_service(db, usuario):
    hash_senha = gerar_hash_senha(usuario.senha)
    novo = Usuario(username=usuario.username, senha_hash=hash_senha)
    db.add(novo)
    db.commit()

    return {"message": "Usuário criado com sucesso"}


def login_service(db, dados):
    usuario = db.query(Usuario).filter(Usuario.username == dados.username).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = criar_token({"sub": usuario.username})

    return {"access_token": token, "token_type": "bearer"}
