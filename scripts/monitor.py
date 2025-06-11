#!/usr/bin/env python3

# Script de Monitoramento - Gerenciador de Projetos e Personas
# Este script verifica o status atual do sistema, identifica personas ativas,
# verifica a necessidade de rotação de personas e geração de relatórios,
# e exibe o status geral do projeto.

import os
import json
import time
from pathlib import Path

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"
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
    STATE_DIR = BASE_DIR / "scripts" / "state"
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        with open(STATE_FILE, 'w') as f:
            json.dump({"active_personas": [], "last_rotation": 0, "last_report": 0}, f)

# Verificar se os arquivos de configuração e estado existem
check_file(CONFIG_FILE)
setup_directories()
check_file(STATE_FILE)

# Ler dados do arquivo de configuração
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    PERSONAS = config_data["personas"]
    ROTATION_INTERVAL = config_data["rotation_interval"]
    REPORT_INTERVAL = config_data["report_interval"]

# Ler estado atual
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]
    LAST_ROTATION = state_data["last_rotation"]
    LAST_REPORT = state_data["last_report"]

# Obter timestamp atual
CURRENT_TIME = int(time.time())

# Calcular tempo desde a última rotação e último relatório
TIME_SINCE_ROTATION = CURRENT_TIME - LAST_ROTATION
TIME_SINCE_REPORT = CURRENT_TIME - LAST_REPORT

# Verificar necessidade de rotação de personas
NEED_ROTATION = TIME_SINCE_ROTATION >= ROTATION_INTERVAL

# Verificar necessidade de geração de relatórios
NEED_REPORT = TIME_SINCE_REPORT >= REPORT_INTERVAL

# Exibir status atual
print_header("📊 STATUS DO PROJETO")
print("Status do Projeto:")
print("- Progresso geral: Ainda não implementado (aguardando script de status do projeto).")
print("- Tarefas pendentes: Ainda não implementado (aguardando script de tarefas).")

# Exibir personas ativas ou necessidade de rotação
if NEED_ROTATION:
    print_header("📢 ALTERAÇÃO DE PERSONAS NECESSÁRIA")
    print("PROMPT DE TRANSIÇÃO:")
    print("- Necessidade de nova rotação de personas detectada.")
    print("- Execute 'python scripts/rotate_personas.py' para alternar personas.")
else:
    print_header("👥 PERSONAS ATUAIS")
    if not ACTIVE_PERSONAS:
        print("Nenhuma persona ativa no momento. Execute 'python scripts/rotate_personas.py' para iniciar.")
    else:
        print(f"Personas ativas: {', '.join(ACTIVE_PERSONAS)}")

# Exibir necessidade de relatórios
if NEED_REPORT:
    print_header("📝 RELATÓRIOS DE PROGRESSO NECESSÁRIOS")
    print("Personas que precisam atualizar seus relatórios:")
    if not ACTIVE_PERSONAS:
        print("Nenhuma persona ativa para relatórios.")
    else:
        for persona in ACTIVE_PERSONAS:
            print(persona)

# Instruções finais
print("=" * 61)
print("Para mais informações sobre os próximos passos, consulte os fluxos de trabalho em 'docs/FLUXOS.md'.")
print("=" * 61)

# Fim do script
exit(0)
