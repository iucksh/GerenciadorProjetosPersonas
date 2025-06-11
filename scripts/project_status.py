#!/usr/bin/env python3

# Script de Status do Projeto - Gerenciador de Projetos e Personas
# Este script exibe um resumo do status atual do projeto, incluindo progresso geral,
# tarefas pendentes, concluídas e distribuição por prioridade.

import os
import json
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
TASKS_FILE = BASE_DIR / "scripts" / "tasks" / "tasks.json"
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
        return False
    return True

# Função para criar diretórios necessários se não existirem
def setup_directories():
    TASKS_DIR = BASE_DIR / "scripts" / "tasks"
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        with open(TASKS_FILE, 'w') as f:
            json.dump({"tasks": []}, f)
    STATE_DIR = BASE_DIR / "scripts" / "state"
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        with open(STATE_FILE, 'w') as f:
            json.dump({"active_personas": [], "last_rotation": 0, "last_report": 0}, f)

# Configurar diretórios e arquivos necessários
setup_directories()

# Verificar se os arquivos existem
if not check_file(TASKS_FILE):
    print_header("⚠️ ARQUIVO DE TAREFAS NÃO ENCONTRADO")
    print("O arquivo de tarefas não foi encontrado. Certifique-se de que tarefas foram adicionadas usando 'task_manager.py'.")
    exit(1)

if not check_file(STATE_FILE):
    print_header("⚠️ ARQUIVO DE ESTADO NÃO ENCONTRADO")
    print("O arquivo de estado não foi encontrado. Certifique-se de que o sistema foi inicializado com 'monitor.py'.")
    exit(1)

# Ler tarefas do arquivo
with open(TASKS_FILE, 'r') as f:
    tasks_data = json.load(f)
    TASKS = tasks_data["tasks"]

# Ler estado atual do sistema
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]
    LAST_ROTATION = state_data["last_rotation"]
    LAST_REPORT = state_data["last_report"]

# Calcular estatísticas de tarefas
total_tasks = len(TASKS)
pending_tasks = len([t for t in TASKS if t["status"] == "Pendente"])
in_progress_tasks = len([t for t in TASKS if t["status"] == "Em Progresso"])
completed_tasks = len([t for t in TASKS if t["status"] == "Concluída"])
completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

# Calcular distribuição por prioridade
p0_tasks = len([t for t in TASKS if t["priority"] == "P0"])
p1_tasks = len([t for t in TASKS if t["priority"] == "P1"])
p2_tasks = len([t for t in TASKS if t["priority"] == "P2"])
p0_pending = len([t for t in TASKS if t["priority"] == "P0" and t["status"] == "Pendente"])

# Exibir resumo do status do projeto
print_header("📊 STATUS DO PROJETO")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Progresso Geral: {completion_percentage:.1f}% concluído")
print(f"Total de Tarefas: {total_tasks}")
print(f" - Pendentes: {pending_tasks}")
print(f" - Em Progresso: {in_progress_tasks}")
print(f" - Concluídas: {completed_tasks}")
print("")
print("Distribuição por Prioridade:")
print(f" - P0 (Crítico): {p0_tasks} tarefas (Pendentes: {p0_pending})")
print(f" - P1 (Importante): {p1_tasks} tarefas")
print(f" - P2 (Desejável): {p2_tasks} tarefas")

# Exibir personas ativas
print_header("👥 PERSONAS ATIVAS")
if not ACTIVE_PERSONAS:
    print("Nenhuma persona ativa no momento. Execute 'python scripts/rotate_personas.py' para ativar novas personas.")
else:
    print(f"Personas Ativas: {', '.join(ACTIVE_PERSONAS)}")
    if LAST_ROTATION > 0:
        print(f"Última Rotação: {datetime.fromtimestamp(LAST_ROTATION).strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("Última Rotação: Ainda não realizada.")

# Exibir status dos relatórios
print_header("📝 STATUS DOS RELATÓRIOS")
if LAST_REPORT > 0:
    print(f"Último Relatório Gerado: {datetime.fromtimestamp(LAST_REPORT).strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print("Último Relatório Gerado: Ainda não realizado.")
if total_tasks > 0 and p0_pending > 0:
    print("⚠️ Aviso: Existem tarefas P0 pendentes. Priorize sua conclusão.")

# Exibir próximas etapas recomendadas
print_header("🚀 PRÓXIMAS ETAPAS RECOMENDADAS")
if pending_tasks > 0:
    print("- Concentre-se nas tarefas pendentes, especialmente as de prioridade P0.")
    print("  Use 'python scripts/task_manager.py list --status \"Pendente\" --priority \"P0\"' para visualizar.")
else:
    print("- Não há tarefas pendentes. Considere adicionar novas tarefas ou revisar prioridades.")
    print("  Use 'python scripts/task_manager.py add' para criar novas tarefas.")
if not ACTIVE_PERSONAS:
    print("- Ative novas personas para trazer diferentes perspectivas ao projeto.")
    print("  Execute 'python scripts/rotate_personas.py' para rotacionar personas.")
else:
    print("- Continue trabalhando com as personas ativas ou rotacione se necessário.")
    print("  Execute 'python scripts/monitor.py' para verificar a necessidade de rotação.")

# Fim do script
exit(0)
