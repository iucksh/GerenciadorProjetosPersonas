#!/usr/bin/env python3

# Script de Rotação de Personas - Gerenciador de Projetos e Personas
# Este script realiza a rotação de personas com base nas prioridades e no intervalo
# configurado, garantindo que todas as perspectivas sejam consideradas regularmente.

import os
import json
import time
import random
from pathlib import Path

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"

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

# Ler estado atual
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]
    LAST_ROTATION = state_data["last_rotation"]

CURRENT_TIME = int(time.time())

# Calcular tempo desde a última rotação
TIME_SINCE_ROTATION = CURRENT_TIME - LAST_ROTATION

# Verificar se a rotação é necessária
if TIME_SINCE_ROTATION < ROTATION_INTERVAL:
    print_header("⏳ ROTAÇÃO NÃO NECESSÁRIA")
    print(f"Tempo desde a última rotação: {TIME_SINCE_ROTATION} segundos.")
    print(f"Intervalo configurado: {ROTATION_INTERVAL} segundos.")
    print("Rotação não é necessária no momento.")
    print(f"Personas ativas: {', '.join(ACTIVE_PERSONAS) if ACTIVE_PERSONAS else 'Nenhuma'}")
    exit(0)

# Lógica de rotação de personas
# Selecionar novas personas com base na prioridade (P0 tem maior peso)
# Este é um exemplo simplificado: seleciona até 3 personas, priorizando P0, depois P1, depois P2
P0_PERSONAS = [p["name"] for p in PERSONAS if p["priority"] == "P0"]
P1_PERSONAS = [p["name"] for p in PERSONAS if p["priority"] == "P1"]
P2_PERSONAS = [p["name"] for p in PERSONAS if p["priority"] == "P2"]

# Inicializar nova lista de personas ativas
NEW_ACTIVE_PERSONAS = []

# Selecionar pelo menos uma persona P0 se disponível
if P0_PERSONAS:
    selected_p0 = random.choice(P0_PERSONAS)
    NEW_ACTIVE_PERSONAS.append(selected_p0)

# Preencher até 3 personas, priorizando P0, depois P1, depois P2
for _ in range(2):
    if len(NEW_ACTIVE_PERSONAS) < 3:
        if P0_PERSONAS and len([p for p in NEW_ACTIVE_PERSONAS if p in P0_PERSONAS]) < len(P0_PERSONAS):
            available_p0 = [p for p in P0_PERSONAS if p not in NEW_ACTIVE_PERSONAS]
            if available_p0:
                NEW_ACTIVE_PERSONAS.append(random.choice(available_p0))
        elif P1_PERSONAS and len(NEW_ACTIVE_PERSONAS) < 3:
            available_p1 = [p for p in P1_PERSONAS if p not in NEW_ACTIVE_PERSONAS]
            if available_p1:
                NEW_ACTIVE_PERSONAS.append(random.choice(available_p1))
        elif P2_PERSONAS and len(NEW_ACTIVE_PERSONAS) < 3:
            available_p2 = [p for p in P2_PERSONAS if p not in NEW_ACTIVE_PERSONAS]
            if available_p2:
                NEW_ACTIVE_PERSONAS.append(random.choice(available_p2))

# Atualizar o estado com as novas personas ativas e o timestamp da rotação
state_data["active_personas"] = NEW_ACTIVE_PERSONAS
state_data["last_rotation"] = CURRENT_TIME
with open(STATE_FILE, 'w') as f:
    json.dump(state_data, f)

# Exibir resultado da rotação
print_header("🔄 ROTAÇÃO DE PERSONAS REALIZADA")
print(f"Novas personas ativas: {', '.join(NEW_ACTIVE_PERSONAS)}")
print(f"Última rotação atualizada para: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(CURRENT_TIME))}")
print("Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'.")

# Fim do script
exit(0)
