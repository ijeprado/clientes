import json

from pydantic import BaseModel, model_validator


class UsuarioCreate(BaseModel):
    username: str
    senha: str


class LoginRequest(BaseModel):
    username: str
    senha: str

    @model_validator(mode="before")
    @classmethod
    def aceitar_json_em_texto(cls, data):
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as exc:
                raise ValueError("Body do login deve ser um JSON valido") from exc
        return data
