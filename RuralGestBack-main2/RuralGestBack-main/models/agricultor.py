from __future__ import annotations
from typing import List
from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Agricultor(db.Model):
    __tablename__ = 'agricultor'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cpf: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    comunidade: Mapped[str] = mapped_column(String(100), nullable=False)
    contato: Mapped[str] = mapped_column(String(20), nullable=True)
    documentacao_validada: Mapped[bool] = mapped_column(Boolean, default=False)
    comprovante_residencia: Mapped[str] = mapped_column(String(50), nullable=True) 
    
    data_atualizacao_cadastro: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=True 
    )

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=True)

    propriedades: Mapped[List["Propriedade"]] = relationship(back_populates="agricultor", cascade="all, delete-orphan")
    solicitacoes: Mapped[List["Solicitacao"]] = relationship(back_populates="agricultor", cascade="all, delete-orphan")
