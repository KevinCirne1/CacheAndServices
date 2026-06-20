from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Solicitacao(db.Model):
    __tablename__ = 'solicitacao'

    id: Mapped[int] = mapped_column(primary_key=True)
    data_solicitacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    data_execucao: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default='Pendente')
    motivo_recusa: Mapped[str] = mapped_column(String(255), nullable=True)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)
    observacao: Mapped[str] = mapped_column(Text, nullable=True)
    observacao_funcionario: Mapped[str] = mapped_column(Text, nullable=True)
    
    # --- CHAVES ESTRANGEIRAS ---
    agricultor_id: Mapped[int] = mapped_column(ForeignKey('agricultor.id'), nullable=False)
    propriedade_id: Mapped[int] = mapped_column(ForeignKey('propriedade.id'), nullable=False)
    servico_id: Mapped[int] = mapped_column(ForeignKey('servico.id'), nullable=False)
    operador_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=True)
    veiculo_id: Mapped[int] = mapped_column(ForeignKey('veiculo.id'), nullable=True)

    # --- RELACIONAMENTOS ---
    agricultor: Mapped["Agricultor"] = relationship(back_populates="solicitacoes")
    propriedade: Mapped["Propriedade"] = relationship(back_populates="solicitacoes")
    servico: Mapped["Servico"] = relationship(back_populates="solicitacoes")
    operador: Mapped["Usuario"] = relationship(back_populates="solicitacoes_atendidas")
    veiculo: Mapped["Veiculo"] = relationship(backref="solicitacoes")