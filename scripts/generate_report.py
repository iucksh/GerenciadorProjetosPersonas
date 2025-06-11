#!/usr/bin/env python3

# Script de Geração de Relatórios - Gerenciador de Projetos e Personas
# Este script gera relatórios de progresso para as personas ativas,
# salvando-os no diretório de relatórios com a data atual.

import os
import json
import time
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"
REPORTS_DIR = BASE_DIR / "scripts" / "reports"
TEMPLATE_FILE = BASE_DIR / "scripts" / "report_template.md"

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
    # Criar subdiretórios para cada persona
    with open(CONFIG_FILE, 'r') as f:
        config_data = json.load(f)
        for persona in config_data["personas"]:
            persona_dir = REPORTS_DIR / persona["name"]
            persona_dir.mkdir(parents=True, exist_ok=True)

# Verificar se os arquivos de configuração e estado existem
check_file(CONFIG_FILE)
setup_directories()
check_file(STATE_FILE)

# Ler estado atual
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]
    LAST_REPORT = state_data["last_report"]

# Ler intervalo de relatórios do arquivo de configuração
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    REPORT_INTERVAL = config_data["report_interval"]

CURRENT_TIME = int(time.time())

# Calcular tempo desde o último relatório
TIME_SINCE_REPORT = CURRENT_TIME - LAST_REPORT

# Verificar se a geração de relatórios é necessária
if TIME_SINCE_REPORT < REPORT_INTERVAL:
    print_header("⏳ GERAÇÃO DE RELATÓRIOS NÃO NECESSÁRIA")
    print(f"Tempo desde o último relatório: {TIME_SINCE_REPORT} segundos.")
    print(f"Intervalo configurado: {REPORT_INTERVAL} segundos.")
    print("Geração de relatórios não é necessária no momento.")
    exit(0)

# Verificar se há personas ativas
if not ACTIVE_PERSONAS:
    print_header("⚠️ NENHUMA PERSONA ATIVA")
    print("Não há personas ativas para gerar relatórios.")
    print("Execute 'python scripts/rotate_personas.py' para ativar novas personas.")
    exit(0)

# Criar ou usar um modelo de relatório básico se o arquivo de template não existir
if not TEMPLATE_FILE.exists():
    with open(TEMPLATE_FILE, 'w') as f:
        f.write("""# Relatório de Progresso - {PERSONA_NAME}
**Data:** {DATE}

## Progresso Recente
- Ainda não atualizado.

## Próximos Passos
- Ainda não atualizado.

## Bloqueadores
- Ainda não atualizado.

## Notas
- Este é um relatório gerado automaticamente. Atualize os campos conforme necessário.
""")

# Obter a data atual para o nome do arquivo e conteúdo do relatório
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
REPORT_COUNT = 0

# Ler o conteúdo do template
with open(TEMPLATE_FILE, 'r') as f:
    template_content = f.read()

# Gerar relatório para cada persona ativa
for persona_name in ACTIVE_PERSONAS:
    REPORT_FILE = REPORTS_DIR / persona_name / f"report_{CURRENT_DATE}.md"
    
    # Verificar se o relatório já existe para evitar sobrescrever
    if REPORT_FILE.exists():
        print(f"Relatório para {persona_name} já existe para a data {CURRENT_DATE}. Pulando...")
    else:
        # Substituir placeholders no template
        report_content = template_content.replace("{PERSONA_NAME}", persona_name).replace("{DATE}", CURRENT_DATE)
        with open(REPORT_FILE, 'w') as f:
            f.write(report_content)
        print(f"Relatório gerado para {persona_name} em {REPORT_FILE}.")
        REPORT_COUNT += 1

# Atualizar o estado com o timestamp do último relatório
state_data["last_report"] = CURRENT_TIME
with open(STATE_FILE, 'w') as f:
    json.dump(state_data, f)

# Exibir resultado da geração de relatórios
print_header("📝 RELATÓRIOS GERADOS")
print(f"Número de relatórios gerados ou verificados: {REPORT_COUNT}")
print(f"Último relatório atualizado para: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(CURRENT_TIME))}")
print(f"Os relatórios estão disponíveis no diretório '{REPORTS_DIR}'.")
print("Para atualizar campos específicos, use 'python scripts/update_report.py <persona> <campo> <conteúdo>'.")
print("Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'.")

# Fim do script
exit(0)
