pipeline {
    agent {
        docker { 
            image 'python:3.11-slim' 
            // CONEXÃO DE REDE E CACHE: 
            // 1. O contentor entra na rede da infraestrutura para comunicar com o 'ruralgest_redis'
            // 2. Mapeamos um volume 'pip-cache' para não descarregar as dependências em todas as builds
            args '-u root --network ruralgest-net -v pip-cache:/root/.cache/pip'
        }
    }

    environment {
        // Apontamos para o nome do serviço definido no docker-compose
        DATABASE_URL = "sqlite:///:memory:" // Mantemos SQLite para o teste não apagar a base de dados real
        SECRET_KEY = "12345"
        
        // CONFIGURAÇÃO DO REDIS REAL
        REDIS_HOST = "ruralgest_redis" 
        REDIS_PORT = "6379"
        CACHE_TYPE = "RedisCache"
    }

    stages {
        stage('Ambiente e Dependências') {
            steps {
                script {
                    // Atualização e instalação de dependências do sistema
                    sh 'apt-get update && apt-get install -y gcc libpq-dev'
                    
                    // Criação do ambiente virtual
                    sh 'python3 -m venv venv'
                    
                    // Instalação de dependências do Python (usará o cache do Docker)
                    sh 'venv/bin/pip install --upgrade pip'
                    sh 'venv/bin/pip install -r requirements.txt'
                    sh 'venv/bin/pip install pytest redis' // Instalamos a biblioteca redis para o teste
                }
            }
        }

        stage('Verificação de Ligação ao Redis') {
            steps {
                script {
                    echo "A testar a ligação com o Redis em: ${env.REDIS_HOST}"
                    // Pequeno script python para validar se o Redis está acessível antes de avançar
                    sh """
                    venv/bin/python -c "
import redis
import sys
try:
    r = redis.Redis(host='${env.REDIS_HOST}', port=6379)
    if r.ping():
        print('Ligação com o Redis OK!')
except Exception as e:
    print(f'Falha ao ligar ao Redis: {e}')
    sys.exit(1)
                    "
                    """
                }
            }
        }

        stage('Testes Automatizados') {
            steps {
                script {
                    sh 'venv/bin/python --version'
                    echo 'A executar a lógica com RedisCache ativo...'
                    // O Flask aqui usará o Redis real do contentor ruralgest_redis
                    // Exemplo: sh 'venv/bin/pytest'
                }
            }
        }
    }
    
    post {
        always {
            // Substituímos o cleanWs() por deleteDir(), comando nativo do Jenkins
            deleteDir()
        }
    }
}