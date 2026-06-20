import click
from models.usuario import Usuario
from models.veiculo import Veiculo
from models.agricultor import Agricultor
from helpers.database import db
from sqlalchemy import text
from sqlalchemy import text

@click.command('seed_admin')
def seed_admin():
    """Cria o utilizador administrador inicial."""
    try:
        login = click.prompt('Digite o login para o administrador', type=str)
        nome = click.prompt('Digite o nome do administrador', type=str)
        senha = click.prompt('Digite a senha para o administrador', type=str, hide_input=True, confirmation_prompt=True)
        
        if Usuario.query.filter_by(login=login).first():
            click.echo('Erro: O utilizador com este login já existe.')
            click.echo('Erro: O utilizador com este login já existe.')
            return

        # Cria o admin com perfil 'gestor'
        # Cria o admin com perfil 'gestor'
        admin = Usuario(nome=nome, login=login, senha=senha, perfil='gestor')
        
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Administrador "{nome}" criado com sucesso!')
        click.echo(f'Administrador "{nome}" criado com sucesso!')

    except Exception as e:
        click.echo(f"Erro ao criar o administrador: {e}")

@click.command('seed_agricultor')
def seed_agricultor():
    """Cria um utilizador com perfil de Agricultor para testes de login."""
    try:
        login = click.prompt('Digite o login para o agricultor', type=str)
        nome = click.prompt('Digite o nome do agricultor', type=str)
        senha = click.prompt('Digite a senha', type=str, hide_input=True, confirmation_prompt=True)
        
        if Usuario.query.filter_by(login=login).first():
            click.echo('Erro: O utilizador com este login já existe.')
            return

        # Cria o utilizador com perfil 'agricultor'
        # Nota: Isto cria um login no sistema. Não cria o registo na tabela 'Agricultor' (dados pessoais),
        # apenas na tabela 'Usuario' para permitir o acesso ao sistema.
        agricultor_user = Usuario(nome=nome, login=login, senha=senha, perfil='agricultor')
        
        db.session.add(agricultor_user)
        db.session.commit()
        click.echo(f'Utilizador Agricultor "{nome}" criado com sucesso!')

    except Exception as e:
        click.echo(f"Erro ao criar o agricultor: {e}")

@click.command('reset_db')
def reset_db():
    """Apaga todos os dados de todas as tabelas."""
    if click.confirm('Tem a certeza que quer apagar TODOS os dados da base de dados? Esta ação é irreversível.'):
        try:
            # Apaga os dados em ordem de dependência para evitar erros de chave estrangeira
            db.session.execute(text('TRUNCATE TABLE solicitacao, servico, usuario, propriedade, agricultor RESTART IDENTITY CASCADE;'))
            # Apaga os dados em ordem de dependência para evitar erros de chave estrangeira
            db.session.execute(text('TRUNCATE TABLE solicitacao, servico, usuario, propriedade, agricultor RESTART IDENTITY CASCADE;'))
            db.session.commit()
            click.echo('Todos os dados foram apagados e os contadores de ID reiniciados.')
        except Exception as e:
            db.session.rollback()
            click.echo(f"Erro ao zerar a base de dados: {e}")

@click.command('seed_veiculos')
def seed_veiculos():
    """Cadastra a frota inicial de veículos."""
    frota = [
        {"nome": "Caminhão Caçamba 01", "tipo": "Caminhão", "placa": "PM-0001"},
        {"nome": "Retroescavadeira 01", "tipo": "Retroescavadeira", "placa": "PM-0002"},
        {"nome": "Motoniveladora 01", "tipo": "Motoniveladora", "placa": "PM-0003"},
        {"nome": "Trator com Grade", "tipo": "Trator", "placa": "PM-0005"},
    ]
    try:
        count = 0
        for v in frota:
            if not Veiculo.query.filter_by(nome=v["nome"]).first():
                novo = Veiculo(nome=v["nome"], tipo=v["tipo"], placa=v["placa"], status="DISPONIVEL")
                db.session.add(novo)
                count += 1
        db.session.commit()
        click.echo(f"Sucesso! {count} veículos adicionados.")
    except Exception as e:
        click.echo(f"Erro: {e}")