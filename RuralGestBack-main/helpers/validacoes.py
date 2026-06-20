import re

def validar_cpf(cpf):
    """
    Componente centralizado para validação matemática de CPF.
    Retorna uma tupla: (True, 'cpf_limpo') se válido, ou (False, 'mensagem de erro') se inválido.
    """
    if not cpf:
        return False, "CPF não informado."

    # 1. Remove tudo que não for número (pontos e traços)
    cpf_limpo = re.sub(r'[^0-9]', '', str(cpf))
    
    # 2. Verifica tamanho exato
    if len(cpf_limpo) != 11:
        return False, "O CPF deve conter exatamente 11 dígitos."

    # 3. Verifica se tem números repetidos (ex: 111.111.111-11)
    if cpf_limpo == cpf_limpo[0] * 11:
        return False, "CPF inválido: Você digitou uma sequência repetida."

    # 4. Cálculo do 1º Dígito Verificador
    soma_1 = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto_1 = (soma_1 * 10) % 11
    if resto_1 == 10: 
        resto_1 = 0

    # 5. Cálculo do 2º Dígito Verificador
    soma_2 = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto_2 = (soma_2 * 10) % 11
    if resto_2 == 10: 
        resto_2 = 0

    # 6. Validação final dos cálculos matemáticos
    if resto_1 != int(cpf_limpo[9]) or resto_2 != int(cpf_limpo[10]):
        return False, "O CPF informado é matematicamente inválido."

    return True, cpf_limpo