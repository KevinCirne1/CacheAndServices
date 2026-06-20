from datetime import datetime
import pytz
from models.auditoria import Auditoria
from models.usuario import Usuario
from helpers.database import db

def obter_agora_brasil():
    """Retorna a data e hora atual no fuso de Brasília."""
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasil).replace(tzinfo=None)

def registrar_log(acao, tabela, registro_id, usuario_id=None, detalhes=""):
    """
    Função para salvar um log no banco com captura de nome e horário de Brasília.
    """
    try:
        login_nome = "Sistema/Desconhecido"
        if usuario_id:
            user = Usuario.query.get(usuario_id)
            if user:
                login_nome = user.login

       
        novo_log = Auditoria(
            acao=acao,
            tabela=tabela, 
            registro_id=registro_id,
            usuario_id=usuario_id,
            login=login_nome,     
            detalhes=detalhes
        )
        
        
        novo_log.data_hora = obter_agora_brasil()
        
        db.session.add(novo_log)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"\n[!] ERRO AO GRAVAR AUDITORIA: {str(e)}\n")