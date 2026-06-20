from flask_restful import Resource, reqparse 
from models import Notificacao
from helpers.database import db
from schemas import NotificacaoListaSchema

# Inicializa o schema 
notificacao_schema = NotificacaoListaSchema(many=True)

# Configura o leitor de parâmetros (usado tanto no GET quanto no LER TUDO)
parser = reqparse.RequestParser()
parser.add_argument('usuario_id', type=int, location='args', required=True)

class NotificacaoListResource(Resource):
    def get(self): 
        """Lista as notificações de um usuário específico"""
        args = parser.parse_args()
        usuario_id = args.get('usuario_id')
        
        # Busca notificações ordenando por não lidas primeiro e depois por data
        notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id)\
            .order_by(Notificacao.lida.asc(), Notificacao.data_criacao.desc())\
            .all()
        return notificacao_schema.dump(notificacoes), 200

class NotificacaoLerResource(Resource):
    def post(self, notificacao_id): 
        """Marca uma notificação específica como lida no banco de dados"""
        notificacao = Notificacao.query.get_or_404(notificacao_id)
        
        # Altera o status no PostgreSQL para persistir após o recarregamento
        notificacao.lida = True
        db.session.commit()
        
        return {'message': 'Notificação marcada como lida'}, 200

class NotificacaoLerTudoResource(Resource):
    def post(self):
        """Marca TODAS as notificações de um usuário como lidas de uma só vez"""
        args = parser.parse_args()
        usuario_id = args.get('usuario_id')

        # Atualização em massa para evitar erros de concorrência no banco
        Notificacao.query.filter_by(usuario_id=usuario_id, lida=False).update({Notificacao.lida: True})
        db.session.commit()

        return {'message': 'Todas as notificações foram marcadas como lidas'}, 200