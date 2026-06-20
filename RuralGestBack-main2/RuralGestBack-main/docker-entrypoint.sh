#!/bin/sh

set -e

echo "==> Verificando e preparando migrações do Flask..."

# Verifica se o diretório migrations existe
if [ ! -d "migrations" ]; then
    echo "==> Diretório migrations não encontrado. Executando flask db init..."
    flask db init
    echo "==> Diretório migrations criado com sucesso!"
else
    echo "==> Diretório migrations já existe."
fi

# Verifica se já existem versões de migração
if [ -z "$(ls -A migrations/versions/ 2>/dev/null)" ]; then
    echo "==> Nenhuma migração encontrada. Criando migração inicial..."
    echo "==> Executando flask db migrate -m 'Migracao inicial'"
    flask db migrate -m "Migracao inicial"
    echo "==> Migração inicial criada com sucesso!"
else
    echo "==> Migrações existentes encontradas."
fi

echo "==> Executando flask db upgrade"
flask db upgrade

echo "==> Migrações aplicadas com sucesso!"

echo "==> Configurando pasta de PDFs..."
mkdir -p /app/documentos_gerados
chmod 777 /app/documentos_gerados

echo "==> Iniciando uWSGI..."

# Executa o comando principal do contêiner (o CMD que é o uwsgi)
exec "$@"