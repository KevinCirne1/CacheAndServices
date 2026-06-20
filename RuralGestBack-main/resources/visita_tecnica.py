from flask import request
from flask_restful import Resource
from models import VisitaTecnica, Solicitacao
from helpers.database import db
from marshmallow import ValidationError

from schemas import VisitaTecnicaLoadSchema, VisitaTecnicaDetalhadoSchema, VisitaTecnicaListaSchema


visita_schema_carga = VisitaTecnicaLoadSchema()
visita_schema_detalhado = VisitaTecnicaDetalhadoSchema()
visitas_schema_lista = VisitaTecnicaListaSchema(many=True)

class VisitaListResource(Resource):
    def get(self):
        
        solicitacao_id = request.args.get('solicitacao_id')
        if solicitacao_id:
            visitas = VisitaTecnica.query.filter_by(solicitacao_id=solicitacao_id).all()
        else:
            visitas = VisitaTecnica.query.all()
        return visitas_schema_lista.dump(visitas)

    def post(self):
        json_data = request.get_json()
        try:
            data = visita_schema_carga.load(json_data)
            nova_visita = VisitaTecnica(**data)
            solicitacao = Solicitacao.query.get(data['solicitacao_id'])
            if solicitacao and solicitacao.status == 'Pendente':
                solicitacao.status = 'Em Andamento'
                
            db.session.add(nova_visita)
            db.session.commit()
            return visita_schema_detalhado.dump(nova_visita), 201
        except ValidationError as err:
            return {"messages": err.messages}, 400

class VisitaResource(Resource):
    def get(self, visita_id):
        visita = VisitaTecnica.query.get_or_404(visita_id)
        return visita_schema_detalhado.dump(visita)

    def put(self, visita_id):
        visita = VisitaTecnica.query.get_or_404(visita_id)
        json_data = request.get_json()
        try:
            data = visita_schema_carga.load(json_data, partial=True)
            for key, value in data.items():
                setattr(visita, key, value)
            db.session.commit()
            return visita_schema_detalhado.dump(visita)
        except ValidationError as err:
            return {"messages": err.messages}, 400

    def delete(self, visita_id):
        visita = VisitaTecnica.query.get_or_404(visita_id)
        db.session.delete(visita)
        db.session.commit()
        return '', 204