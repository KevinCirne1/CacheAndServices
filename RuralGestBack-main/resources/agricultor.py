from flask import request
from flask_restful import Resource
from models import Agricultor, Usuario 
from helpers.database import db
from marshmallow import ValidationError
import json # <--- ADICIONADO PARA O REDIS
import redis # <--- ADICIONADO PARA O REDIS

from schemas import (
    AgricultorDetalhadoSchema, 
    AgricultorListaSchema, 
    AgricultorLoadSchema
)

# Instâncias dos Schemas
agricultor_schema_detalhado = AgricultorDetalhadoSchema()
agricultores_schema_lista = AgricultorListaSchema(many=True)
agricultor_schema_carga = AgricultorLoadSchema()

# --- INÍCIO DA CONFIGURAÇÃO DO REDIS ---
cache = redis.Redis(host='redis', port=6379, decode_responses=True)
# --- FIM DA CONFIGURAÇÃO DO REDIS ---


class AgricultorListResource(Resource):
    def get(self):
        agricultores = Agricultor.query.all()
        return agricultores_schema_lista.dump(agricultores)

    def post(self):
        json_data = request.get_json()
        
        # 1. Valida os dados do Agricultor com Marshmallow
        try:
            dados_validados = agricultor_schema_carga.load(json_data)
        except ValidationError as err:
            return {"messages": err.messages}, 400

        try:
            # 2. Prepara dados de Login
            senha_digitada = json_data.get('senha')
            # Tenta usar email, se não tiver, usa CPF (apenas números)
            login_usuario = json_data.get('email')
            if not login_usuario and 'cpf' in dados_validados:
                login_usuario = ''.join(filter(str.isdigit, dados_validados['cpf']))

            if not senha_digitada:
                return {"message": "Senha é obrigatória para criar o acesso."}, 400
            if not login_usuario:
                return {"message": "CPF ou Email obrigatório para login."}, 400

            # Verifica duplicidade no Usuário
            if Usuario.query.filter_by(login=login_usuario).first():
                return {"message": f"O login '{login_usuario}' já está em uso."}, 409

            # 3. Cria o Usuário vinculado
            novo_usuario = Usuario(
                nome=dados_validados.get('nome'),
                login=login_usuario,
                senha=senha_digitada, 
                perfil="produtor",
                contato=dados_validados.get('contato') 
            )

            db.session.add(novo_usuario)
            db.session.flush() 

            # 4. Cria o Agricultor vinculado
            if hasattr(Agricultor, 'usuario_id'):
                dados_validados['usuario_id'] = novo_usuario.id
            
            novo_agricultor = Agricultor(**dados_validados)
            
            db.session.add(novo_agricultor)
            db.session.commit()
            
            return agricultor_schema_detalhado.dump(novo_agricultor), 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Erro interno ao cadastrar.", "error": str(e)}, 500


class AgricultorResource(Resource):
    def get(self, agricultor_id):
        # --- INÍCIO DA LÓGICA DO REDIS (Recuperação e Persistência) ---
        chave_cache = f"agricultor:{agricultor_id}"
        
        try:
            dado_cache = cache.get(chave_cache)
            if dado_cache:
                print("Recuperado do Cache (Redis)")
                return json.loads(dado_cache), 200
        except Exception as e:
            print(f"Erro ao acessar Redis (GET): {e}")
        
        # Se não tem no cache, busca no banco
        agricultor = Agricultor.query.get_or_404(agricultor_id)
        dado_resposta = agricultor_schema_detalhado.dump(agricultor)

        # Salva no Redis
        try:
            cache.setex(chave_cache, 3600, json.dumps(dado_resposta))
            print("Salvo no Cache (Redis)")
        except Exception as e:
            print(f"Erro ao salvar no Redis: {e}")

        return dado_resposta, 200
        # --- FIM DA LÓGICA DO REDIS ---

    def put(self, agricultor_id):
        agricultor = Agricultor.query.get_or_404(agricultor_id)
        json_data = request.get_json()
        
        try:
            # partial=True permite editar só alguns campos
            dados_validados = agricultor_schema_carga.load(json_data, partial=True)
            
            # Atualiza os dados do Agricultor
            for key, value in dados_validados.items():
                setattr(agricultor, key, value)
            
            if agricultor.cpf:
                # 1. Gera versão LIMPA (só números: 12345678900)
                cpf_limpo = ''.join(filter(str.isdigit, agricultor.cpf))
                
                # 2. Gera versão FORMATADA (123.456.789-00)
                cpf_formatado = cpf_limpo
                if len(cpf_limpo) == 11:
                    cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

                # 3. Busca o usuário por QUALQUER UMA das versões
                usuario_vinculado = Usuario.query.filter(
                    (Usuario.login == cpf_limpo) | (Usuario.login == cpf_formatado)
                ).first()

                # 4. Se achou, atualiza os dados dele
                if usuario_vinculado:
                    if 'contato' in dados_validados:
                        usuario_vinculado.contato = dados_validados['contato']
                        
                    if 'nome' in dados_validados:
                        usuario_vinculado.nome = dados_validados['nome']
                    
                    # Garante que o SQLAlchemy viu a mudança no usuário
                    db.session.add(usuario_vinculado) 

            db.session.commit()
            
            # --- INÍCIO INVALIDAÇÃO DO CACHE REDIS ---
            try:
                cache.delete(f"agricultor:{agricultor_id}")
            except Exception as e:
                 print(f"Erro ao deletar cache (PUT): {e}")
            # --- FIM INVALIDAÇÃO DO CACHE REDIS ---

            return agricultor_schema_detalhado.dump(agricultor)
            
        except ValidationError as err:
            return {"messages": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": "Erro ao atualizar.", "error": str(e)}, 500

    def delete(self, agricultor_id):
        agricultor = Agricultor.query.get_or_404(agricultor_id)
        
        # Verifica se tem registros vinculados que impediriam a exclusão
        tem_solicitacoes = agricultor.solicitacoes and len(agricultor.solicitacoes) > 0
        tem_propriedades = agricultor.propriedades and len(agricultor.propriedades) > 0
        
        if tem_solicitacoes or tem_propriedades:
             return {"message": "Não é possível excluir: existem propriedades ou solicitações vinculadas."}, 409

        try:
            # Tenta pegar o ID do usuário antes de deletar o agricultor
            usuario_id_vinculado = getattr(agricultor, 'usuario_id', None)
            usuario_vinculado = getattr(agricultor, 'usuario', None)

            db.session.delete(agricultor)
            
            # Se tinha usuário vinculado, deleta também
            if usuario_vinculado:
                db.session.delete(usuario_vinculado)
            elif usuario_id_vinculado:
                user = Usuario.query.get(usuario_id_vinculado)
                if user:
                    db.session.delete(user)

            db.session.commit()
            
            # --- INÍCIO INVALIDAÇÃO DO CACHE REDIS ---
            try:
                 cache.delete(f"agricultor:{agricultor_id}")
            except Exception as e:
                 print(f"Erro ao deletar cache (DELETE): {e}")
            # --- FIM INVALIDAÇÃO DO CACHE REDIS ---

            return '', 204
            
        except Exception as e:
            db.session.rollback()
            return {"message": "Erro ao excluir.", "error": str(e)}, 500