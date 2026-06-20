from flask import request
from flask_restful import Resource
from models import Servico
from helpers.database import db
from marshmallow import ValidationError

from schemas import (
    ServicoListaSchema,
    ServicoLoadSchema
)

# --- Instâncias dos Schemas ---
servicos_schema_lista = ServicoListaSchema(many=True)
servico_schema_carga = ServicoLoadSchema()

# --- Resources ---

class ServicoListResource(Resource):
    def get(self):
        servicos = Servico.query.all()
        return servicos_schema_lista.dump(servicos)

    def post(self):
        json_data = request.get_json()
        try:
            dados_validados = servico_schema_carga.load(json_data)
            novo_servico = Servico(**dados_validados)
        except ValidationError as err:
            return {"messages": err.messages}, 400
        
        db.session.add(novo_servico)
        db.session.commit()
        return ServicoListaSchema().dump(novo_servico), 201

class ServicoResource(Resource):
    def get(self, servico_id):
        servico = Servico.query.get_or_404(servico_id)
        return ServicoListaSchema().dump(servico)
    
    def put(self, servico_id):
        servico = Servico.query.get_or_404(servico_id)
        json_data = request.get_json()
        try:
            dados_validados = servico_schema_carga.load(json_data, partial=True)
            for key, value in dados_validados.items():
                setattr(servico, key, value)
        except ValidationError as err:
            return {"messages": err.messages}, 400
        
        db.session.commit()
        return ServicoListaSchema().dump(servico)

    def delete(self, servico_id):
        servico = Servico.query.get_or_404(servico_id)
        db.session.delete(servico)
        db.session.commit()
        return '', 204
