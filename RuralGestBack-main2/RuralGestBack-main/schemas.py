from helpers.database import ma
from marshmallow import fields, EXCLUDE, validate, validates, ValidationError, pre_load
from helpers.validacoes import validar_cpf
import re

# --- Schemas de Visualização (Dumps) ---

class VeiculoSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    status = fields.Str()

class AgricultorSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    documentacao_validada = fields.Bool()
    comprovante_residencia = fields.Str() 

class PropriedadeSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    terreno = fields.Str()

class UsuarioSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()

class ServicoSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome_servico = fields.Str()
    tipo_veiculo = fields.Str()
    requer_funcionario = fields.Bool()

class SolicitacaoSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    data_solicitacao = fields.DateTime()
    data_execucao = fields.DateTime(allow_none=True) 
    status = fields.Str()

class VisitaTecnicaSimplesSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    data_visita = fields.DateTime(format='%d/%m/%Y')
    observacoes = fields.Str()

# --- Schemas de Lista (Dumps Principais) ---

class VeiculoListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    placa = fields.Str()
    tipo = fields.Str()
    status = fields.Str()

class NotificacaoListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    mensagem = fields.Str()
    lida = fields.Bool()
    data_criacao = fields.DateTime(format='%d/%m/%Y %H:%M')

class AgricultorListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    cpf = fields.Str()
    comunidade = fields.Str()
    contato = fields.Str()
    documentacao_validada = fields.Bool()
    comprovante_residencia = fields.Str()
    data_atualizacao_cadastro = fields.DateTime(format='%d/%m/%Y')

class PropriedadeListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    terreno = fields.Str()
    vinculo = fields.Str()
    tipo_agricultura = fields.Str()
    area_total = fields.Float()
    area_exploravel = fields.Float()
    coordenadas_geograficas = fields.Str()
    agricultor_id = fields.Int()
    cultura_principal = fields.Str()
    quantidade_gado = fields.Int()

class UsuarioListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    login = fields.Str()
    perfil = fields.Str()
    contato = fields.Str() 

class ServicoListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nome_servico = fields.Str()
    descricao = fields.Str()
    capacidade_hectares = fields.Float()
    tipo_veiculo = fields.Str()
    requer_funcionario = fields.Bool() 

class SolicitacaoListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    
    
    data_solicitacao = fields.DateTime()
    data_execucao = fields.DateTime(allow_none=True) 
    

    operador_id = fields.Int()
    veiculo_id = fields.Int()   
    status = fields.Str()
    motivo_recusa = fields.Str()
    
    # Campos de Observação
    observacao = fields.Str()  
    observacao_funcionario = fields.Str()  
    observacoes = fields.Str()  
    
    # Relacionamentos (Nested)
    agricultor = fields.Nested(AgricultorSimplesSchema, dump_only=True)
    servico = fields.Nested(ServicoSimplesSchema, dump_only=True)
    propriedade = fields.Nested(PropriedadeSimplesSchema, dump_only=True)
    veiculo = fields.Nested(VeiculoSimplesSchema, dump_only=True)
    operador = fields.Nested(UsuarioSimplesSchema, dump_only=True)

class VisitaTecnicaListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    data_visita = fields.DateTime(format='%d/%m/%Y')
    observacoes = fields.Str()
    tecnico_nome = fields.Function(lambda obj: obj.tecnico.nome if obj.tecnico else "N/A")
    solicitacao_id = fields.Int()

class AuditoriaListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    acao = fields.Str()
    tabela_afetada = fields.Str()
    registro_id = fields.Int()
    login = fields.Str()
    detalhes = fields.Str()
    data_hora = fields.DateTime(format='%d/%m/%Y %H:%M:%S')

# --- Schemas de Detalhe ---

class PropriedadeDetalhadoSchema(PropriedadeListaSchema):
    agricultor = fields.Nested(AgricultorSimplesSchema, dump_only=True)

class AgricultorDetalhadoSchema(AgricultorListaSchema):
    propriedades = fields.Nested("PropriedadeSimplesSchema", many=True, dump_only=True)
    solicitacoes = fields.Nested("SolicitacaoSimplesSchema", many=True, dump_only=True)

class UsuarioDetalhadoSchema(UsuarioListaSchema):
    solicitacoes_atendidas = fields.Nested("SolicitacaoSimplesSchema", many=True, dump_only=True)

class SolicitacaoDetalhadoSchema(SolicitacaoListaSchema):
    pass

class VisitaTecnicaDetalhadoSchema(VisitaTecnicaListaSchema):
    pass

# --- Schemas de Carga (Load / Input de Dados) ---

class BaseLoadSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

class VeiculoLoadSchema(BaseLoadSchema):
    nome = fields.Str(required=True)
    placa = fields.Str(allow_none=True)
    tipo = fields.Str(required=True)
    status = fields.Str(allow_none=True)

class AgricultorLoadSchema(BaseLoadSchema):
    nome = fields.Str(required=True)
    cpf = fields.Str(required=True)
    comunidade = fields.Str(required=True)
    contato = fields.Str(required=True)
    documentacao_validada = fields.Bool(allow_none=True)
    comprovante_residencia = fields.Str(allow_none=True)
    
    @validates('cpf')
    def validate_cpf(self, value, **kwargs):
        
        valido, resultado = validar_cpf(value)
        if not valido:
            raise ValidationError(resultado) 

class PropriedadeLoadSchema(BaseLoadSchema):
    terreno = fields.Str(required=True)
    vinculo = fields.Str(
        required=True, 
        validate=validate.OneOf(["Própria", "Alugada", "Cedida"], error="Vínculo inválido")
    )
    tipo_agricultura = fields.Str(required=True)
    area_total = fields.Float(required=True)
    area_exploravel = fields.Float(required=True)
    coordenadas_geograficas = fields.Str(required=True)
    agricultor_id = fields.Int()
    cultura_principal = fields.Str(allow_none=True)
    quantidade_gado = fields.Int(load_default=0)

class UsuarioLoadSchema(BaseLoadSchema):
    nome = fields.Str(required=True)
    login = fields.Str(required=True)
    senha = fields.Str(required=True, load_only=True)
    perfil = fields.Str(required=True)
    contato = fields.Str(allow_none=True)

class ServicoLoadSchema(BaseLoadSchema):
    nome_servico = fields.Str(required=True)
    descricao = fields.Str(allow_none=True)
    capacidade_hectares = fields.Float(allow_none=True)
    tipo_veiculo = fields.Str(allow_none=True)
    requer_funcionario = fields.Bool(allow_none=True) 

class SolicitacaoLoadSchema(BaseLoadSchema):
    agricultor_id = fields.Int(required=True)
    propriedade_id = fields.Int(required=True)
    servico_id = fields.Int(required=True)
    operador_id = fields.Int(allow_none=True)
    veiculo_id = fields.Int(allow_none=True)
    status = fields.Str()
    motivo_recusa = fields.Str(allow_none=True)
    
    # Campos editáveis
    observacao = fields.Str(allow_none=True) 
    observacao_funcionario = fields.Str(allow_none=True) 
    observacoes = fields.Str(allow_none=True) 
    
    data_execucao = fields.DateTime(allow_none=True, load_default=None)

    @pre_load
    def process_input(self, data, **kwargs):
        for key, value in data.items():
            if value == "":
                data[key] = None
        return data

class VisitaTecnicaLoadSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
    solicitacao_id = fields.Int(required=True)
    tecnico_id = fields.Int(required=True)
    data_visita = fields.DateTime(allow_none=True)
    observacoes = fields.Str(required=True)

class DocumentoListaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    tipo_documento = fields.Str()
    arquivo_pdf = fields.Str()
    assinatura_digital = fields.Str()
    data_geracao = fields.DateTime(format='%d/%m/%Y')
    solicitacao_id = fields.Int()

class DocumentoLoadSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
    solicitacao_id = fields.Int(required=True)
    tipo_documento = fields.Str(required=True)