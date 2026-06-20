from flask_restful import Resource
from sqlalchemy import func, or_
from helpers.database import db
from models import Agricultor, Solicitacao, Servico, Propriedade
from helpers.application import cache

class DashboardResumoResource(Resource):
    @cache.cached(timeout=60)
    def get(self):
        """Devolve os contadores principais para os cartões e gráfico de status"""
        
        # 1. Totais Gerais
        total_agricultores = db.session.query(func.count(Agricultor.id)).scalar()
        total_solicitacoes = db.session.query(func.count(Solicitacao.id)).scalar()
        total_hectares = db.session.query(func.sum(Propriedade.area_total)).scalar() or 0
        
        # Pega todos os status do banco 
        all_status = db.session.query(Solicitacao.status).all()
        status_list = [s[0].upper() for s in all_status] 
        
        # Agrupa nas 3 categorias do gráfico
        pendentes = status_list.count('PENDENTE')
        
        
        em_andamento = (status_list.count('EM ANDAMENTO') + 
                        status_list.count('APROVADA') + 
                        status_list.count('EM_USO'))
                        
        concluidas = (status_list.count('CONCLUÍDA') + 
                      status_list.count('CONCLUIDA') + 
                      status_list.count('FINALIZADA'))

        return {
            "total_agricultores": total_agricultores,
            "total_solicitacoes": total_solicitacoes,
            "total_hectares_cadastrados": round(total_hectares, 2),
            "solicitacoes_status": {
                "pendentes": pendentes,
                "em_andamento": em_andamento,
                "concluidas": concluidas
            }
        }, 200

class DashboardGraficosResource(Resource):
    @cache.cached(timeout=300)
    def get(self):
        """Devolve dados formatados para o gráfico de barras (Serviços)"""
        
        # Serviços mais solicitados
        servicos_populares = db.session.query(
            Servico.nome_servico, func.count(Solicitacao.id)
        ).join(Solicitacao).group_by(Servico.nome_servico).all()

        dados_grafico_servicos = [
            {"name": nome, "value": contagem} for nome, contagem in servicos_populares
        ]

        return {
            "servicos_populares": dados_grafico_servicos,
        }, 200