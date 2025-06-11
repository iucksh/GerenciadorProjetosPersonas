#!/usr/bin/env python3

# Script de Atualização de Relatórios - Gerenciador de Projetos e Personas
# Este script atualiza campos específicos nos relatórios de progresso de uma persona,
# permitindo adicionar informações sobre progresso, próximos passos, bloqueadores e notas.

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
REPORTS_DIR = BASE_DIR / "scripts" / "reports"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para verificar se um arquivo existe e é legível
def check_file(file_path):
    if not file_path.exists() or not os.access(file_path, os.R_OK):
        print(f"Erro: Arquivo {file_path} não encontrado ou não é legível.")
        exit(1)

# Função para criar diretórios necessários se não existirem
def setup_directories():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # Criar subdiretórios para cada persona
    with open(CONFIG_FILE, 'r') as f:
        config_data = json.load(f)
        for persona in config_data["personas"]:
            persona_dir = REPORTS_DIR / persona["name"]
            persona_dir.mkdir(parents=True, exist_ok=True)

# Verificar se o arquivo de configuração existe
check_file(CONFIG_FILE)
setup_directories()

# Verificar parâmetros de entrada
if len(sys.argv) < 4:
    print_header("❌ ERRO DE USO")
    print(f"Uso: {sys.argv[0]} <nome_persona> <campo> \"<conteúdo>\"")
    print("Campos disponíveis: progress, next_steps, blockers, notes")
    print(f"Exemplo: {sys.argv[0]} João progress \"Implementei a API de autenticação hoje.\"")
    exit(1)

PERSONA_NAME = sys.argv[1]
FIELD = sys.argv[2]
CONTENT = sys.argv[3]

# Verificar se a persona existe no arquivo de configuração
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    PERSONA_EXISTS = next((p for p in config_data["personas"] if p["name"] == PERSONA_NAME), None)

if not PERSONA_EXISTS:
    print_header("❌ PERSONA NÃO ENCONTRADA")
    print(f"A persona '{PERSONA_NAME}' não foi encontrada no arquivo de configuração.")
    print("Verifique o arquivo 'scripts/personas/config.json' e tente novamente.")
    exit(1)

# Verificar se o campo é válido
VALID_FIELDS = {"progress", "next_steps", "blockers", "notes"}
if FIELD not in VALID_FIELDS:
    print_header("❌ CAMPO INVÁLIDO")
    print(f"Campo '{FIELD}' não é válido. Campos disponíveis: {', '.join(VALID_FIELDS)}")
    exit(1)

# Obter a data atual para encontrar o relatório mais recente
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
REPORT_FILE = REPORTS_DIR / PERSONA_NAME / f"report_{CURRENT_DATE}.md"

# Verificar se o relatório existe; se não, criar um básico
if not REPORT_FILE.exists():
    print(f"Relatório para {PERSONA_NAME} não encontrado para {CURRENT_DATE}. Criando um novo...")
    with open(REPORT_FILE, 'w') as f:
        f.write(f"""# Relatório de Progresso - {PERSONA_NAME}
**Data:** {CURRENT_DATE}

## Progresso Recente
- Ainda não atualizado.

## Próximos Passos
- Ainda não atualizado.

## Bloqueadores
- Ainda não atualizado.

## Notas
- Este é um relatório gerado automaticamente. Atualize os campos conforme necessário.
""")

# Mapear o campo para o título correspondente no relatório
FIELD_TO_SECTION = {
    "progress": "Progresso Recente",
    "next_steps": "Próximos Passos",
    "blockers": "Bloqueadores",
    "notes": "Notas"
}
SECTION = FIELD_TO_SECTION[FIELD]

# Ler o conteúdo atual do relatório
with open(REPORT_FILE, 'r') as f:
    REPORT_CONTENT = f.readlines()

# Verificar se a seção existe no relatório
section_found = False
for line in REPORT_CONTENT:
    if line.strip() == f"## {SECTION}":
        section_found = True
        break

if not section_found:
    print(f"Seção '{SECTION}' não encontrada no relatório. Adicionando...")
    with open(REPORT_FILE, 'a') as f:
        f.write(f"\n## {SECTION}\n- Ainda não atualizado.\n")
    with open(REPORT_FILE, 'r') as f:
        REPORT_CONTENT = f.readlines()

# Atualizar o campo no relatório
new_content = []
in_section = False
for line in REPORT_CONTENT:
    if line.strip() == f"## {SECTION}":
        in_section = True
        new_content.append(line)
        new_content.append(f"- {CONTENT}\n")
    elif in_section and line.strip().startswith("## "):
        in_section = False
        new_content.append(line)
    elif in_section and line.strip().startswith("- "):
        continue  # Ignorar linhas antigas da seção
    else:
        new_content.append(line)

# Escrever o novo conteúdo de volta ao arquivo
with open(REPORT_FILE, 'w') as f:
    f.writelines(new_content)

# Exibir resultado da atualização
print_header("✅ RELATÓRIO ATUALIZADO")
print(f"Campo '{FIELD}' atualizado para a persona '{PERSONA_NAME}'.")
print(f"Relatório: {REPORT_FILE}")
print(f"Conteúdo adicionado: - {CONTENT}")
print("Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'.")

# Fim do script
exit(0)
