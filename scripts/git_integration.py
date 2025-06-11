#!/usr/bin/env python3

# Script de Integração com Git - Gerenciador de Projetos e Personas
# Este script automatiza commits de relatórios com autoria das personas,
# garantindo que as alterações sejam rastreadas no controle de versão.

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "scripts" / "reports"
STATE_FILE = BASE_DIR / "scripts" / "state" / "agent_state.json"
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"
GIT_LOG_FILE = BASE_DIR / "scripts" / "logs" / "git_commits.log"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para verificar se um arquivo existe e é legível
def check_file(file_path, description):
    if not file_path.exists() or not os.access(file_path, os.R_OK):
        print(f"Erro: {description} não encontrado ou não é legível em {file_path}.")
        return False
    return True

# Função para criar diretórios necessários se não existirem
def setup_directories():
    LOG_DIR = BASE_DIR / "scripts" / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not GIT_LOG_FILE.exists():
        with open(GIT_LOG_FILE, 'w') as f:
            f.write(f"Log de Commits Git - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(GIT_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
setup_directories()

# Verificar se os arquivos existem
if not check_file(STATE_FILE, "Arquivo de Estado do Sistema"):
    print_header("⚠️ ARQUIVO DE ESTADO NÃO ENCONTRADO")
    print("O arquivo de estado não foi encontrado. Certifique-se de que o sistema foi inicializado com 'monitor.py'.")
    exit(1)

if not check_file(CONFIG_FILE, "Arquivo de Configuração de Personas"):
    print_header("⚠️ ARQUIVO DE CONFIGURAÇÃO NÃO ENCONTRADO")
    print("O arquivo de configuração de personas não foi encontrado. Certifique-se de que 'config.json' está configurado.")
    exit(1)

# Ler estado atual do sistema
with open(STATE_FILE, 'r') as f:
    state_data = json.load(f)
    ACTIVE_PERSONAS = state_data["active_personas"]

# Ler configuração de personas para obter informações de autoria
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    PERSONAS = {p["name"]: p["role"] for p in config_data["personas"]}

# Função para verificar se o diretório é um repositório Git
def check_git_repo():
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        print("✅ Repositório Git detectado no diretório do projeto.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Este diretório não é um repositório Git. Inicialize um repositório com 'git init'.")
        return False
    except FileNotFoundError:
        print("❌ Git não está instalado. Instale o Git para usar este script.")
        return False

# Função para adicionar arquivos ao staging
def git_add_files(files):
    try:
        subprocess.run(['git', 'add'] + files, cwd=BASE_DIR, check=True, capture_output=True, text=True)
        print(f"Arquivos adicionados ao staging: {', '.join(files)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao adicionar arquivos ao staging: {e.stderr}")
        return False

# Função para fazer commit com autoria da persona
def git_commit(message, author_name, author_email=None):
    author_str = f"{author_name} <{author_email if author_email else f'{author_name.lower()}@example.com'}>"
    try:
        subprocess.run(['git', 'commit', '-m', message, f'--author={author_str}'], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        print(f"Commit realizado com sucesso como {author_name}: {message}")
        log_action(f"Commit realizado por {author_name}: {message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao fazer commit: {e.stderr}")
        return False

# Iniciar integração com Git
print_header("🔄 INTEGRAÇÃO COM GIT")
if not check_git_repo():
    print("Integração com Git não pode prosseguir. Corrija os problemas acima.")
    exit(1)

# Verificar relatórios para commit
reports_to_commit = []
for persona in ACTIVE_PERSONAS:
    persona_dir = REPORTS_DIR / persona
    if persona_dir.exists() and persona_dir.is_dir():
        for report_file in persona_dir.glob("report_*.md"):
            reports_to_commit.append(str(report_file.relative_to(BASE_DIR)))

if not reports_to_commit:
    print_header("ℹ️ NENHUM RELATÓRIO PARA COMMIT")
    print("Nenhum relatório encontrado para as personas ativas. Gere relatórios com 'generate_report.py'.")
    exit(0)

# Adicionar relatórios ao staging
print_header("📁 ADICIONANDO RELATÓRIOS AO STAGING")
if not git_add_files(reports_to_commit):
    print("Falha ao adicionar relatórios ao staging. Verifique o status do repositório com 'git status'.")
    exit(1)

# Fazer commit para cada persona ativa
print_header("📝 REALIZANDO COMMITS")
for persona in ACTIVE_PERSONAS:
    persona_reports = [r for r in reports_to_commit if f"/{persona}/" in r]
    if persona_reports:
        role = PERSONAS.get(persona, "Desconhecido")
        commit_message = f"Relatório de progresso de {persona} ({role}) - {datetime.now().strftime('%Y-%m-%d')}"
        if not git_commit(commit_message, persona):
            print(f"Falha ao fazer commit para {persona}. Verifique o status do repositório com 'git status'.")
            exit(1)

# Resumo da integração
print_header("✅ INTEGRAÇÃO CONCLUÍDA")
print(f"Relatórios de {len(ACTIVE_PERSONAS)} persona(s) foram commitados com sucesso.")
print(f"Log de Commits: {GIT_LOG_FILE}")
print("Use 'git log' para ver o histórico de commits com autoria das personas.")

# Fim do script
exit(0)
