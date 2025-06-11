#!/usr/bin/env python3

# Script de Diagnóstico - Gerenciador de Projetos e Personas
# Este script verifica problemas no sistema, como scripts não executáveis,
# configurações inválidas ou arquivos ausentes, e fornece sugestões para correção.

import os
import json
import stat
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
TASKS_FILE = BASE_DIR / "scripts" / "tasks" / "tasks.json"
REPORTS_DIR = BASE_DIR / "scripts" / "reports"
LOGS_DIR = BASE_DIR / "scripts" / "logs"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para verificar se um arquivo existe e é legível
def check_file(file_path, description):
    if not file_path.exists():
        print(f"❌ Problema: {description} não encontrado em {file_path}.")
        return False
    if not os.access(file_path, os.R_OK):
        print(f"❌ Problema: {description} não é legível em {file_path}.")
        return False
    print(f"✅ {description} encontrado e legível em {file_path}.")
    return True

# Função para verificar se um diretório existe e é gravável
def check_directory(dir_path, description):
    if not dir_path.exists():
        print(f"❌ Problema: {description} não encontrado em {dir_path}.")
        return False
    if not os.access(dir_path, os.W_OK):
        print(f"❌ Problema: {description} não é gravável em {dir_path}.")
        return False
    print(f"✅ {description} encontrado e gravável em {dir_path}.")
    return True

# Função para verificar se um script é executável
def check_executable(file_path, description):
    if not file_path.exists():
        print(f"❌ Problema: {description} não encontrado em {file_path}.")
        return False
    mode = os.stat(file_path).st_mode
    if not (mode & stat.S_IXUSR):
        print(f"❌ Problema: {description} não é executável em {file_path}. Corrija com 'chmod +x {file_path}'.")
        return False
    print(f"✅ {description} é executável em {file_path}.")
    return True

# Função para validar JSON de um arquivo
def validate_json(file_path, description):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ {description} tem formato JSON válido em {file_path}.")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Problema: {description} tem formato JSON inválido em {file_path}. Erro: {e}")
        return False
    except Exception as e:
        print(f"❌ Problema: Erro ao ler {description} em {file_path}. Erro: {e}")
        return False

# Iniciar diagnóstico
print_header("🔍 DIAGNÓSTICO DO SISTEMA")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Verificando a integridade do sistema 'Gerenciador de Projetos e Personas'...")

# Contador de problemas encontrados
issues_count = 0

# Verificar arquivos críticos
if not check_file(CONFIG_FILE, "Arquivo de Configuração de Personas"):
    issues_count += 1
else:
    if not validate_json(CONFIG_FILE, "Arquivo de Configuração de Personas"):
        issues_count += 1

if not check_file(STATE_FILE, "Arquivo de Estado do Sistema"):
    issues_count += 1
else:
    if not validate_json(STATE_FILE, "Arquivo de Estado do Sistema"):
        issues_count += 1

if not check_file(TASKS_FILE, "Arquivo de Tarefas"):
    issues_count += 1
else:
    if not validate_json(TASKS_FILE, "Arquivo de Tarefas"):
        issues_count += 1

# Verificar diretórios críticos
if not check_directory(REPORTS_DIR, "Diretório de Relatórios"):
    issues_count += 1

if not check_directory(LOGS_DIR, "Diretório de Logs"):
    issues_count += 1

# Verificar scripts executáveis
scripts_to_check = [
    ("monitor.py", "Script de Monitoramento"),
    ("rotate_personas.py", "Script de Rotação de Personas"),
    ("generate_report.py", "Script de Geração de Relatórios"),
    ("update_report.py", "Script de Atualização de Relatórios"),
    ("task_manager.py", "Script de Gerenciamento de Tarefas"),
    ("project_status.py", "Script de Status do Projeto"),
    ("notify.py", "Script de Notificações")
]

for script_name, description in scripts_to_check:
    script_path = SCRIPTS_DIR / script_name
    if not check_executable(script_path, description):
        issues_count += 1

# Resumo do diagnóstico
print_header("📋 RESUMO DO DIAGNÓSTICO")
if issues_count == 0:
    print("🎉 Nenhum problema encontrado! O sistema está funcionando corretamente.")
else:
    print(f"⚠️ {issues_count} problema(s) encontrado(s). Revise os itens acima e siga as sugestões para correção.")
    print("Sugestões Gerais:")
    print("- Certifique-se de que todos os arquivos e diretórios necessários existem.")
    print("- Verifique as permissões de leitura, escrita e execução com 'chmod' se necessário.")
    print("- Valide a formatação JSON dos arquivos de configuração, estado e tarefas.")
    print("- Execute 'monitor.py' para inicializar o sistema se os arquivos de estado estiverem ausentes.")

# Fim do script
exit(0 if issues_count == 0 else 1)
