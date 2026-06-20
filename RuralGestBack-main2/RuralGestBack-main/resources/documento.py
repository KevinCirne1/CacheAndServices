from flask import request, send_file
from flask_restful import Resource
from models import Documento, Solicitacao
from helpers.database import db
from marshmallow import ValidationError
from schemas import DocumentoListaSchema, DocumentoLoadSchema
import os

from helpers.pdf.gerador_pdf import gerar_pdf_solicitacao

# --- Instâncias dos Schemas ---
documento_schema_carga = DocumentoLoadSchema()
documentos_schema_lista = DocumentoListaSchema(many=True)
documento_schema_detalhado = DocumentoListaSchema() 

class DocumentoListResource(Resource):
    def get(self):
        solicitacao_id = request.args.get('solicitacao_id')
        if solicitacao_id:
            documentos = Documento.query.filter_by(solicitacao_id=solicitacao_id).all()
        else:
            documentos = Documento.query.all()
        return documentos_schema_lista.dump(documentos)

    def post(self):
        # Gera o PDF e cria o registro no banco
        json_data = request.get_json()
        try:
            data = documento_schema_carga.load(json_data)
            
            # 1. Busca a solicitação (necessária para preencher o PDF)
            solicitacao = Solicitacao.query.get_or_404(data['solicitacao_id'])
            
            # 2. Instancia o documento 
            novo_doc = Documento(
                solicitacao_id=data['solicitacao_id'],
                tipo_documento=data['tipo_documento']
            )
            
            # GERA O ARQUIVO FÍSICO NO DISCO 
           
            gerar_pdf_solicitacao(solicitacao, data['tipo_documento'], novo_doc.arquivo_pdf)
            
            # 4. Salva no banco de dados
            db.session.add(novo_doc)
            db.session.commit()
            
            return documento_schema_detalhado.dump(novo_doc), 201
            
        except ValidationError as err:
            return {"messages": err.messages}, 400

class DocumentoResource(Resource):
    def get(self, documento_id):
        doc = Documento.query.get_or_404(documento_id)
        return documento_schema_detalhado.dump(doc)
    
    def delete(self, documento_id):
        doc = Documento.query.get_or_404(documento_id)
        
        # Remove ficheiro físico ao apagar da DB para não deixar lixo
        pasta = os.path.abspath("documentos_gerados")
        caminho = os.path.join(pasta, doc.arquivo_pdf)
        
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
            except Exception as e:
                print(f"Erro ao apagar arquivo físico: {e}")
            
        db.session.delete(doc)
        db.session.commit()
        return '', 204

# --- ENDPOINT PARA DOWNLOAD REAL ---
class DocumentoDownloadResource(Resource):
    def get(self, documento_id):
        
        doc = Documento.query.get_or_404(documento_id)
        
        # Caminho absoluto da pasta de armazenamento
        base_dir = os.path.abspath("documentos_gerados")
        file_path = os.path.join(base_dir, doc.arquivo_pdf)
        
        if not os.path.exists(file_path):
            return {"message": "O ficheiro PDF não foi encontrado no servidor físico."}, 404
            
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=doc.arquivo_pdf
        )