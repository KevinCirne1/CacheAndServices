from flask import request
from flask_restful import Resource
from models import Veiculo
from helpers.database import db
from schemas import VeiculoListaSchema, VeiculoLoadSchema
from marshmallow import ValidationError

veiculo_schema = VeiculoListaSchema()
veiculos_schema_lista = VeiculoListaSchema(many=True)
veiculo_load_schema = VeiculoLoadSchema()

class VeiculoListResource(Resource):
    def get(self):
        veiculos = Veiculo.query.all()
        return veiculos_schema_lista.dump(veiculos)

    def post(self):
        json_data = request.get_json()
        try:
            data = veiculo_load_schema.load(json_data)
            novo_veiculo = Veiculo(**data)
            db.session.add(novo_veiculo)
            db.session.commit()
            return veiculo_schema.dump(novo_veiculo), 201
        except ValidationError as err:
            return {"messages": err.messages}, 400

class VeiculoResource(Resource):
    def get(self, veiculo_id):
        veiculo = Veiculo.query.get_or_404(veiculo_id)
        return veiculo_schema.dump(veiculo)

    def put(self, veiculo_id):
        veiculo = Veiculo.query.get_or_404(veiculo_id)
        json_data = request.get_json()
        try:
            data = veiculo_load_schema.load(json_data, partial=True)
            for key, value in data.items():
                setattr(veiculo, key, value)
            db.session.commit()
            return veiculo_schema.dump(veiculo)
        except ValidationError as err:
            return {"messages": err.messages}, 400

    def delete(self, veiculo_id):
        veiculo = Veiculo.query.get_or_404(veiculo_id)
        db.session.delete(veiculo)
        db.session.commit()
        return '', 204