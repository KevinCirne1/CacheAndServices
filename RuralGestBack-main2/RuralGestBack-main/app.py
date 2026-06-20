from flask import Flask, jsonify
from flask_migrate import Migrate
from helpers.database import db, ma, bcrypt
from helpers.application import app, api
from helpers.cors import cors
from models import Agricultor, Propriedade, Usuario, Servico, Solicitacao
from commands import seed_admin, reset_db, seed_agricultor

# Importação dos Resources (Endpoints)
from resources.agricultor import AgricultorResource, AgricultorListResource
from resources.propriedade import PropriedadeResource, PropriedadeListResource, AllPropriedadesListResource
from resources.usuario import UsuarioResource, UsuarioListResource
from resources.servico import ServicoResource, ServicoListResource
from resources.solicitacao import SolicitacaoResource, SolicitacaoListResource
from resources.auth import LoginResource, RegistroAgricultorResource 
from resources.veiculo import VeiculoResource, VeiculoListResource


from resources.notificacao import NotificacaoListResource, NotificacaoLerResource, NotificacaoLerTudoResource

from resources.visita_tecnica import VisitaListResource, VisitaResource
from resources.dashboard import DashboardResumoResource, DashboardGraficosResource 
from resources.documento import DocumentoListResource, DocumentoResource, DocumentoDownloadResource

# Inicialização das extensões
#db.init_app(app)
#ma.init_app(app)
#cors.init_app(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://10.112.136.42:3000"])
#bcrypt.init_app(app)
migrate = Migrate(app, db)

# Registrar comandos de terminal
app.cli.add_command(seed_admin)
app.cli.add_command(reset_db)
app.cli.add_command(seed_agricultor) 



# Adicionar os endpoints à API
from resources.agricultor import AgricultorResource, AgricultorListResource
from resources.propriedade import PropriedadeResource, PropriedadeListResource, AllPropriedadesListResource
from resources.usuario import UsuarioResource, UsuarioListResource
from resources.servico import ServicoResource, ServicoListResource
from resources.solicitacao import SolicitacaoResource, SolicitacaoListResource

api.add_resource(AgricultorListResource, '/agricultores')
api.add_resource(AgricultorResource, '/agricultores/<int:agricultor_id>')
api.add_resource(PropriedadeListResource, '/agricultores/<int:agricultor_id>/propriedades')
api.add_resource(PropriedadeResource, '/propriedades/<int:propriedade_id>')
api.add_resource(AllPropriedadesListResource, '/propriedades')

# Usuários
api.add_resource(UsuarioListResource, '/usuarios')
api.add_resource(UsuarioResource, '/usuarios/<int:usuario_id>')

# Serviços e Solicitações
api.add_resource(ServicoListResource, '/servicos')
api.add_resource(ServicoResource, '/servicos/<int:servico_id>')
api.add_resource(SolicitacaoListResource, '/solicitacoes')
api.add_resource(SolicitacaoResource, '/solicitacoes/<int:solicitacao_id>')

# Veículos e Visitas
api.add_resource(VeiculoListResource, '/veiculos') 
api.add_resource(VeiculoResource, '/veiculos/<int:veiculo_id>')
api.add_resource(VisitaListResource, '/visitas')
api.add_resource(VisitaResource, '/visitas/<int:visita_id>')

# Dashboard
api.add_resource(DashboardResumoResource, '/dashboard/resumo')
api.add_resource(DashboardGraficosResource, '/dashboard/graficos')

# Documentos
api.add_resource(DocumentoListResource, '/documentos')
api.add_resource(DocumentoResource, '/documentos/<int:documento_id>')

# Notificações 
api.add_resource(NotificacaoListResource, '/notificacoes')
api.add_resource(NotificacaoLerResource, '/notificacoes/<int:notificacao_id>')
api.add_resource(NotificacaoLerTudoResource, '/notificacoes/ler-tudo')

# ROTA DE DOWNLOAD 
api.add_resource(DocumentoDownloadResource, '/documentos/download/<int:documento_id>')

if __name__ == '__main__':
    app.run(debug=True)
