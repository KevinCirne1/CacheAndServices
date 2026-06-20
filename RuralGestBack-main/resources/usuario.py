from flask import request
from flask_restful import Resource
from models import Usuario, Agricultor 
from helpers.database import db
from marshmallow import ValidationError
from schemas import (
    UsuarioDetalhadoSchema, 
    UsuarioListaSchema, 
    UsuarioLoadSchema
)

# --- Instâncias dos Schemas ---
usuario_schema_detalhado = UsuarioDetalhadoSchema()
usuarios_schema_lista = UsuarioListaSchema(many=True)
usuario_schema_carga = UsuarioLoadSchema()

# --- Resources ---

class UsuarioListResource(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        return usuarios_schema_lista.dump(usuarios)

    def post(self):
        json_data = request.get_json()
        try:
            # Carrega e valida os dados (incluindo contato)
            dados_validados = usuario_schema_carga.load(json_data)
            
            # Cria o usuário passando todos os dados validados
            novo_usuario = Usuario(**dados_validados)
            
        except ValidationError as err:
            return {"messages": err.messages}, 400
        
        db.session.add(novo_usuario)
        db.session.commit()
        return usuario_schema_detalhado.dump(novo_usuario), 201

class UsuarioResource(Resource):
    def get(self, usuario_id):
        usuario = Usuario.query.get_or_404(usuario_id)
        return usuario_schema_detalhado.dump(usuario)

    def put(self, usuario_id):
        usuario = Usuario.query.get_or_404(usuario_id)
        json_data = request.get_json()
        
        try:
            
            dados = usuario_schema_carga.load(json_data, partial=True)
        except ValidationError as err:
            return {"messages": err.messages}, 400

        # Atualiza os campos se eles vierem na requisição
        if 'nome' in dados: usuario.nome = dados['nome']
        if 'login' in dados: usuario.login = dados['login']
        if 'perfil' in dados: usuario.perfil = dados['perfil']
        if 'contato' in dados: usuario.contato = dados['contato']
        
        # Só atualiza a senha se ela for enviada e não for vazia
        if 'senha' in dados and dados['senha']:
            usuario.senha = dados['senha']

        # --- INÍCIO DA SINCRONIZAÇÃO COM AGRICULTOR ---
        
        if usuario.login:
            # Remove caracteres não numéricos para verificar se é um CPF
            login_limpo = ''.join(filter(str.isdigit, usuario.login))

            # Se tiver 11 dígitos, assumimos que é um CPF
            if len(login_limpo) == 11:
                # Busca se existe um agricultor com esse CPF (formatado ou limpo)
                agricultor_vinculado = Agricultor.query.filter(
                    (Agricultor.cpf == login_limpo) | (Agricultor.cpf == usuario.login)
                ).first()

                if agricultor_vinculado:
                    # Se achou, sincroniza os dados que foram alterados
                    if 'contato' in dados:
                        agricultor_vinculado.contato = dados['contato']
                    if 'nome' in dados:
                        agricultor_vinculado.nome = dados['nome']
        

        db.session.commit()
        return usuario_schema_detalhado.dump(usuario)

    def delete(self, usuario_id):
        usuario = Usuario.query.get_or_404(usuario_id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204