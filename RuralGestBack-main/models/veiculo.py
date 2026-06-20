from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from helpers.database import db

class Veiculo(db.Model):
    __tablename__ = 'veiculo'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False) 
    placa: Mapped[str] = mapped_column(String(20), nullable=True) 
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) 
    status: Mapped[str] = mapped_column(String(20), default='DISPONIVEL', nullable=False) 
