from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Documento(db.Model):
    __tablename__ = 'documento'

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_documento: Mapped[str] = mapped_column(String(50), nullable=False) 
    arquivo_pdf: Mapped[str] = mapped_column(String(255), nullable=True) 
    assinatura_digital: Mapped[str] = mapped_column(String(255), nullable=True) 
    data_geracao: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    solicitacao_id: Mapped[int] = mapped_column(ForeignKey('solicitacao.id', ondelete='CASCADE'), nullable=False)

    solicitacao: Mapped["Solicitacao"] = relationship(backref="documentos")

    def __init__(self, solicitacao_id, tipo_documento):
        self.solicitacao_id = solicitacao_id
        self.tipo_documento = tipo_documento
        # Simula uma assinatura digital única baseada na data e ID
        import uuid
        self.assinatura_digital = str(uuid.uuid4())
        self.arquivo_pdf = f"doc_{solicitacao_id}_{int(datetime.utcnow().timestamp())}.pdf"
