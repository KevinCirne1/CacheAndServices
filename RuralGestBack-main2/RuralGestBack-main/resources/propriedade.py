from flask import request
from flask_restful import Resource
from models import Propriedade, Agricultor
from helpers.database import db
from marshmallow import ValidationError

from schemas import (
    PropriedadeDetalhadoSchema,
    PropriedadeListaSchema,
    PropriedadeLoadSchema
)

# --- Instâncias dos Schemas ---
propriedade_schema_detalhado = PropriedadeDetalhadoSchema()
propriedades_schema_lista = PropriedadeListaSchema(many=True)
propriedade_schema_carga = PropriedadeLoadSchema()

# --- Resources ---

class AllPropriedadesListResource(Resource):
    def get(self):
        propriedades = Propriedade.query.all()
        return propriedades_schema_lista.dump(propriedades)

class PropriedadeListResource(Resource):
    def get(self, agricultor_id):
        Agricultor.query.get_or_404(agricultor_id)
        propriedades = Propriedade.query.filter_by(agricultor_id=agricultor_id).all()
        return propriedades_schema_lista.dump(propriedades)
    
    def post(self, agricultor_id):
        Agricultor.query.get_or_404(agricultor_id)
        json_data = request.get_json()
        try:
            dados_validados = propriedade_schema_carga.load(json_data)
            nova_propriedade = Propriedade(agricultor_id=agricultor_id, **dados_validados)
        except ValidationError as err:
            return {"messages": err.messages}, 400
        
        db.session.add(nova_propriedade)
        db.session.commit()
        return propriedade_schema_detalhado.dump(nova_propriedade), 201

class PropriedadeResource(Resource):
    def get(self, propriedade_id):
        propriedade = Propriedade.query.get_or_404(propriedade_id)
        return propriedade_schema_detalhado.dump(propriedade)

    def put(self, propriedade_id):
        propriedade = Propriedade.query.get_or_404(propriedade_id)
        json_data = request.get_json()
        try:
            dados_validados = propriedade_schema_carga.load(json_data, partial=True)
            for key, value in dados_validados.items():
                setattr(propriedade, key, value)
        except ValidationError as err:
            return {"messages": err.messages}, 400
        
        db.session.commit()
        return propriedade_schema_detalhado.dump(propriedade)

    def delete(self, propriedade_id):
        propriedade = Propriedade.query.get_or_404(propriedade_id)
        db.session.delete(propriedade)
        db.session.commit()
        return '', 204