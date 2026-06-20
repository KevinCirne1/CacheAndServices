from __future__ import annotations
from typing import List, Optional
import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db, bcrypt

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(String(50), nullable=False)
    contato: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    solicitacoes_atendidas: Mapped[List["Solicitacao"]] = relationship(back_populates="operador")

    def __init__(self, nome, login, senha, perfil='tecnico', contato=None):
        self.nome = nome
        self.login = login
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')
        self.perfil = perfil
        self.contato = contato  

    def verificar_senha(self, senha_texto_plano):
        """
        Verifica se a senha em texto simples bate com o hash do banco.
        Retorna True ou False.
        """
        return bcrypt.check_password_hash(self.senha, senha_texto_plano)