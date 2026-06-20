from flask_restful import Resource
from models import Auditoria
from schemas import AuditoriaListaSchema

# Instancia o Schema a partir do ficheiro central schemas.py
auditorias_schema = AuditoriaListaSchema(many=True)

class AuditoriaListResource(Resource):
    def get(self):
        # Busca todos os logs ordenados do mais recente para o mais antigo
        logs = Auditoria.query.order_by(Auditoria.data_hora.desc()).all()
        return auditorias_schema.dump(logs), 200