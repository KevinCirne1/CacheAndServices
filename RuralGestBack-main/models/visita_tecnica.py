from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class VisitaTecnica(db.Model):
    __tablename__ = 'visita_tecnica'

    id: Mapped[int] = mapped_column(primary_key=True)
    data_visita: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    observacoes: Mapped[str] = mapped_column(Text, nullable=False)
    
 
    solicitacao_id: Mapped[int] = mapped_column(ForeignKey("solicitacao.id"), nullable=False)
    tecnico_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    solicitacao: Mapped["Solicitacao"] = relationship(backref="visitas")
    tecnico: Mapped["Usuario"] = relationship(backref="visitas_realizadas")