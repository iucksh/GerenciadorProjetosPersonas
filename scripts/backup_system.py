#!/usr/bin/env python3

# Script de Sistema de Backup - Gerenciador de Projetos e Personas
# Este script implementa um sistema de backup para configurações e relatórios,
# garantindo que os dados não sejam perdidos em caso de falhas ou exclusões acidentais.

import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
BACKUP_DIR = BASE_DIR / "scripts" / "backups"
CONFIG_DIR = BASE_DIR / "scripts" / "personas"
STATE_DIR = BASE_DIR / "scripts" / "state"
REPORTS_DIR = BASE_DIR / "scripts" / "reports"
TASKS_DIR = BASE_DIR / "scripts" / "tasks"
LOGS_DIR = BASE_DIR / "scripts" / "logs"
BACKUP_LOG_FILE = LOGS_DIR / "backup.log"

# Configurações de backup
MAX_BACKUPS = 10  # Número máximo de backups a serem mantidos
BACKUP_FREQUENCY = timedelta(days=1)  # Frequência padrão para backups automáticos

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para verificar se um diretório existe e é legível
def check_directory(dir_path, description):
    if not dir_path.exists():
        print(f"❌ Problema: {description} não encontrado em {dir_path}.")
        return False
    if not os.access(dir_path, os.R_OK):
        print(f"❌ Problema: {description} não é legível em {dir_path}.")
        return False
    print(f"✅ {description} encontrado e legível em {dir_path}.")
    return True

# Função para criar diretórios necessários se não existirem
def setup_directories():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not BACKUP_LOG_FILE.exists():
        with open(BACKUP_LOG_FILE, 'w') as f:
            f.write(f"Log de Backup - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(BACKUP_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
setup_directories()

# Função para criar um arquivo zip de backup
def create_backup_zip(backup_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{backup_name}_{timestamp}.zip"
    backup_path = BACKUP_DIR / backup_filename
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Adicionar diretórios ao backup
        for dir_to_backup, dir_name in [
            (CONFIG_DIR, "personas"),
            (STATE_DIR, "state"),
            (REPORTS_DIR, "reports"),
            (TASKS_DIR, "tasks")
        ]:
            if dir_to_backup.exists():
                for item in dir_to_backup.rglob('*'):
                    if item.is_file():
                        arcname = f"{dir_name}/{item.relative_to(dir_to_backup)}"
                        zipf.write(item, arcname)
                        print(f"Adicionado ao backup: {arcname}")
    
    log_action(f"Backup criado: {backup_filename}")
    print(f"Backup salvo em: {backup_path}")
    return backup_path

# Função para gerenciar backups antigos (limitar ao número máximo)
def manage_old_backups():
    backups = sorted(BACKUP_DIR.glob("backup_*.zip"), key=os.path.getmtime)
    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[:-MAX_BACKUPS]:
            try:
                old_backup.unlink()
                log_action(f"Backup antigo removido: {old_backup.name}")
                print(f"Backup antigo removido: {old_backup.name}")
            except Exception as e:
                log_action(f"Erro ao remover backup antigo {old_backup.name}: {e}")
                print(f"Erro ao remover backup antigo: {old_backup.name}")

# Função para restaurar um backup
def restore_backup(backup_filename):
    backup_path = BACKUP_DIR / backup_filename
    if not backup_path.exists():
        print(f"Erro: Backup {backup_filename} não encontrado em {BACKUP_DIR}.")
        return False
    
    restore_dir = BASE_DIR / "scripts" / "restored_backup"
    restore_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(backup_path, 'r') as zipf:
        zipf.extractall(restore_dir)
    
    log_action(f"Backup restaurado: {backup_filename} para {restore_dir}")
    print(f"Backup restaurado em: {restore_dir}")
    print("Nota: Os arquivos restaurados estão em um diretório temporário. Mova manualmente para os locais apropriados se necessário.")
    return True

# Iniciar sistema de backup
print_header("💾 SISTEMA DE BACKUP")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Verificar diretórios críticos
dirs_to_check = [
    (CONFIG_DIR, "Diretório de Configurações"),
    (STATE_DIR, "Diretório de Estado"),
    (REPORTS_DIR, "Diretório de Relatórios"),
    (TASKS_DIR, "Diretório de Tarefas")
]

for dir_path, desc in dirs_to_check:
    check_directory(dir_path, desc)

# Criar um novo backup
print_header("📦 CRIANDO NOVO BACKUP")
backup_name = "system"
create_backup_zip(backup_name)

# Gerenciar backups antigos
print_header("🗑️ GERENCIANDO BACKUPS ANTIGOS")
manage_old_backups()

# Listar backups disponíveis
print_header("📋 BACKUPS DISPONÍVEIS")
backups = sorted(BACKUP_DIR.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
if backups:
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup.name} (Criado em: {datetime.fromtimestamp(backup.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
else:
    print("Nenhum backup encontrado.")

# Instruções para restauração
print_header("ℹ️ COMO RESTAURAR UM BACKUP")
print("Para restaurar um backup, execute este script com o nome do arquivo de backup como argumento:")
print("  ./backup_system.py restore <nome_do_arquivo.zip>")
print("Exemplo:")
print(f"  ./backup_system.py restore {backups[0].name if backups else 'backup_system_YYYYMMDD_HHMMSS.zip'}")

# Verificar se há um argumento para restauração
import sys
if len(sys.argv) > 2 and sys.argv[1] == "restore":
    backup_to_restore = sys.argv[2]
    print_header(f"🔄 RESTAURANDO BACKUP: {backup_to_restore}")
    restore_backup(backup_to_restore)
    exit(0)

# Resumo do backup
print_header("✅ BACKUP CONCLUÍDO")
print(f"Log de Backup: {BACKUP_LOG_FILE}")
print(f"Diretório de Backups: {BACKUP_DIR}")
print(f"Número máximo de backups mantidos: {MAX_BACKUPS}")

# Fim do script
exit(0)
