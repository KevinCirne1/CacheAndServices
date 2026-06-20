from __future__ import annotations
from datetime import datetime
import pytz # Certifique-se de ter o pytz instalado
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from helpers.database import db 

# Função para pegar a hora de Brasília limpa
def hora_brasil():
    fuso = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso).replace(tzinfo=None)

class Notificacao(db.Model):
    __tablename__ = 'notificacao'

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)
    mensagem: Mapped[str] = mapped_column(String(255), nullable=False)
    lida: Mapped[bool] = mapped_column(Boolean, default=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=hora_brasil)

    def __init__(self, usuario_id: int, mensagem: str):
        self.usuario_id = usuario_id
        self.mensagem = mensagem