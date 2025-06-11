#!/usr/bin/env python3

# Script de Notificações - Gerenciador de Projetos e Personas
# Este script simula o envio de notificações para alertar sobre rotação de personas
# ou relatórios pendentes. Futuramente, pode ser expandido para suportar e-mail ou outras formas de notificação.

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
NOTIFICATION_LOG = BASE_DIR / "scripts" / "logs" / "notifications.log"

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
    LOG_DIR = BASE_DIR / "scripts" / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not NOTIFICATION_LOG.exists():
        with open(NOTIFICATION_LOG, 'w') as f:
            f.write(f"Log de Notificações - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")

# Configurar diretórios e arquivos necessários
setup_directories()

# Verificar se os arquivos existem
if not check_file(STATE_FILE):
    print_header("⚠️ ARQUIVO DE ESTADO NÃO ENCONTRADO")
    print("O arquivo de estado não foi encontrado. Certifique-se de que o sistema foi inicializado com 'monitor.py'.")
    exit(1)

if not check_file(CONFIG_FILE):
    print_header("⚠️ ARQUIVO DE CONFIGURAÇÃO NÃO ENCONTRADO")
    print("O arquivo de configuração de personas não foi encontrado. Certifique-se de que 'config.json' está configurado.")
    exit(1)

# Ler estado atual do sistema
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]
    LAST_ROTATION = state_data["last_rotation"]
    LAST_REPORT = state_data["last_report"]

# Ler configuração de personas
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    ROTATION_INTERVAL = config_data["rotation_interval"]
    REPORT_INTERVAL = config_data["report_interval"]
    PERSONAS = [p["name"] for p in config_data["personas"]]

# Função para registrar notificação no log
def log_notification(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(NOTIFICATION_LOG, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Notificação registrada: {message}")

# Verificar necessidade de rotação de personas
current_time = datetime.now().timestamp()
rotation_due = LAST_ROTATION + ROTATION_INTERVAL if LAST_ROTATION > 0 else 0
if rotation_due < current_time and LAST_ROTATION > 0:
    time_since_last_rotation = timedelta(seconds=int(current_time - LAST_ROTATION))
    log_notification(f"Rotação de personas necessária! Última rotação foi há {time_since_last_rotation} atrás.")
else:
    if LAST_ROTATION == 0:
        log_notification("Rotação de personas nunca foi realizada. Considere executar 'rotate_personas.py'.")
    else:
        time_until_next_rotation = timedelta(seconds=int(rotation_due - current_time))
        print(f"Rotação de personas não é necessária. Próxima rotação em {time_until_next_rotation}.")

# Verificar necessidade de relatórios
report_due = LAST_REPORT + REPORT_INTERVAL if LAST_REPORT > 0 else 0
if report_due < current_time and LAST_REPORT > 0:
    time_since_last_report = timedelta(seconds=int(current_time - LAST_REPORT))
    for persona in ACTIVE_PERSONAS:
        log_notification(f"Relatório pendente para {persona}! Último relatório foi há {time_since_last_report} atrás.")
else:
    if LAST_REPORT == 0:
        log_notification("Relatórios nunca foram gerados. Considere executar 'generate_report.py'.")
    else:
        time_until_next_report = timedelta(seconds=int(report_due - current_time))
        print(f"Relatórios não são necessários. Próximo relatório em {time_until_next_report}.")

# Exibir status atual
print_header("📢 STATUS DAS NOTIFICAÇÕES")
print(f"Personas Ativas: {', '.join(ACTIVE_PERSONAS) if ACTIVE_PERSONAS else 'Nenhuma'}")
print(f"Intervalo de Rotação Configurado: {timedelta(seconds=ROTATION_INTERVAL)}")
print(f"Intervalo de Relatório Configurado: {timedelta(seconds=REPORT_INTERVAL)}")
print(f"Log de Notificações: {NOTIFICATION_LOG}")

# Instruções para expansão futura
print_header("ℹ️ EXPANSÃO FUTURA")
print("Este script atualmente registra notificações em um arquivo de log. Futuramente, pode ser expandido para:")
print("- Enviar e-mails para os responsáveis pelas personas.")
print("- Enviar mensagens via plataformas como Slack ou Discord.")
print("- Integrar com sistemas de notificação do sistema operacional.")

# Fim do script
exit(0)
