from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from models.usuario import Usuario

SECRET_KEY = "sua_chave_secreta_aqui"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def criar_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha, hash_senha)


def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        usuario = db.query(Usuario).filter(Usuario.username == username).first()

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    finally:
        db.close()
