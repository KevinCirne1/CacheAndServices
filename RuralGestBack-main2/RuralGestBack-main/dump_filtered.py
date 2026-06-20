import os
from pathlib import Path
import fnmatch

# --- ALTERAÇÃO AQUI: Pega a pasta onde o script está rodando ---
ROOT_PATH = Path(os.getcwd()) 
OUT_FILE = ROOT_PATH / "codigo_completo.txt"

print(f"Lendo arquivos de: {ROOT_PATH}")

# Diretórios que queremos incluir (o código fonte)
INCLUDE_DIRS = {"helpers", "models", "resources", "infra"} # Adicionei infra se quiser

# Arquivos na raiz que queremos incluir
ROOT_PATTERNS = ["schemas.py", "commands.py", ".env", "app.py", "config.py", "requirements.txt", "Dockerfile", "docker-compose.yml"]

# Diretórios para IGNORAR (lixo, caches, venv)
EXCLUDE_DIRS = {".venv", "venv", ".git", ".idea", "__pycache__", "migrations", ".pytest_cache"}

files = []

for root, dirs, filenames in os.walk(ROOT_PATH):
    root_path = Path(root)

    # Pula pastas excluídas
    if any(part in EXCLUDE_DIRS for part in root_path.parts):
        continue

    # Calcula o caminho relativo
    try:
        rel_root = root_path.relative_to(ROOT_PATH)
    except ValueError:
        continue

    # Regra 1: Se estiver dentro das pastas permitidas (helpers, models, etc)
    if len(rel_root.parts) > 0 and rel_root.parts[0] in INCLUDE_DIRS:
        for fname in filenames:
            if not fname.endswith(".pyc"): # Ignora arquivos compilados
                files.append(root_path / fname)
        continue

    # Regra 2: Se estiver na Raiz, verifica se bate com os padrões
    if root_path == ROOT_PATH:
        for fname in filenames:
            for pat in ROOT_PATTERNS:
                if fnmatch.fnmatch(fname.lower(), pat.lower()):
                    files.append(root_path / fname)
                    break

# Ordena e escreve o arquivo final
files = sorted(list(set(files)))
print(f"Encontrados {len(files)} arquivos para documentar.")

with OUT_FILE.open("w", encoding="utf-8", errors="replace") as out:
    for i, f in enumerate(files, start=1):
        try:
            rel = f.relative_to(ROOT_PATH)
            out.write("# " + "="*77 + "\n")
            out.write(f"# ARQUIVO {i}: {rel}\n")
            out.write("# " + "="*77 + "\n")
            out.write(f"```python:{f.name}\n") # Formato Markdown
            
            text = f.read_text(encoding="utf-8", errors="replace")
            out.write(text)
            
            if not text.endswith("\n"):
                out.write("\n")
            out.write("```\n\n")
        except Exception as e:
            print(f"Erro ao ler {f}: {e}")

print("-" * 30)
print(f"SUCESSO! Arquivo gerado em: {OUT_FILE}")
print("-" * 30)