# 1. Imagem Base: Python 3.11 leve (Slim)
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Instala dependências do SISTEMA (Linux)
# ADICIONEI 'dos2unix' AQUI PARA CORRIGIR O ARQUIVO DO WINDOWS
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia e instala as dependências do PYTHON
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o restante do código
COPY . .

# 7. Expõe a porta 5000
EXPOSE 5000


RUN dos2unix ./docker-entrypoint.sh && chmod +x ./docker-entrypoint.sh

# Definir o script como o ponto de entrada
ENTRYPOINT ["./docker-entrypoint.sh"]

# 8. Comando para iniciar o sistema
CMD ["uwsgi", "--ini", "uwsgi.ini"]