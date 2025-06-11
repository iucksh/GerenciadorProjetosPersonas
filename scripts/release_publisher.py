#!/usr/bin/env python3

# Script de Publicação de Release - Gerenciador de Projetos e Personas
# Este script auxilia na publicação de uma versão estável do sistema, gerando notas de release
# e atualizando informações de versão para garantir que os usuários tenham instruções claras
# para instalação e uso.

import os
import json
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
RELEASE_NOTES_DIR = DOCS_DIR / "releases"
LOGS_DIR = BASE_DIR / "scripts" / "logs"
RELEASE_LOG_FILE = LOGS_DIR / "release_publisher.log"
VERSION_FILE = BASE_DIR / "VERSION.txt"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(RELEASE_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
LOGS_DIR.mkdir(parents=True, exist_ok=True)
RELEASE_NOTES_DIR.mkdir(parents=True, exist_ok=True)
if not RELEASE_LOG_FILE.exists():
    with open(RELEASE_LOG_FILE, 'w') as f:
        f.write(f"Log de Publicação de Release - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")

# Função para obter a versão atual ou definir uma nova
def get_or_set_version(new_version=None):
    if VERSION_FILE.exists():
        with open(VERSION_FILE, 'r') as f:
            current_version = f.read().strip()
    else:
        current_version = "0.0.0"
    
    if new_version:
        with open(VERSION_FILE, 'w') as f:
            f.write(new_version)
        log_action(f"Versão atualizada para: {new_version}")
        return new_version
    return current_version

# Função para gerar notas de release
def generate_release_notes(version, changes):
    release_date = datetime.now().strftime('%Y-%m-%d')
    release_notes_filename = f"release_notes_v{version}_{release_date}.md"
    release_notes_path = RELEASE_NOTES_DIR / release_notes_filename
    
    with open(release_notes_path, 'w', encoding='utf-8') as f:
        f.write(f"# Notas de Release - Versão {version}\n\n")
        f.write(f"Data de Lançamento: {release_date}\n\n")
        f.write("## Visão Geral\n\n")
        f.write("Estamos felizes em anunciar a versão estável do Gerenciador de Projetos e Personas. ")
        f.write("Esta versão traz um sistema completo para gerenciamento de projetos e automação de personas, ")
        f.write("com ferramentas para rotação de personas, geração de relatórios, rastreamento de tarefas e muito mais.\n\n")
        f.write("## Principais Mudanças e Melhorias\n\n")
        for change in changes:
            f.write(f"- {change}\n")
        f.write("\n## Instruções de Instalação e Uso\n\n")
        f.write("### Instalação\n\n")
        f.write("1. Clone o repositório ou baixe os arquivos da versão mais recente.\n")
        f.write("2. Certifique-se de ter o Python 3 instalado em seu sistema.\n")
        f.write("3. Siga as instruções detalhadas no arquivo `INSTALACAO.md` na pasta `docs`.\n\n")
        f.write("### Uso Básico\n\n")
        f.write("1. Configure as personas do seu projeto editando `scripts/personas/config.json`.\n")
        f.write("2. Execute o script de monitoramento para verificar o status do sistema:\n")
        f.write("   ```\n")
        f.write("   python scripts/monitor.py\n")
        f.write("   ```\n")
        f.write("3. Consulte os tutoriais em `docs/tutorials` para guias detalhados sobre como usar o sistema.\n\n")
        f.write("## Suporte e Feedback\n\n")
        f.write("Se encontrar problemas ou tiver sugestões, abra uma issue no repositório do projeto ou entre em contato com a equipe de suporte.\n\n")
        f.write("## Agradecimentos\n\n")
        f.write("Agradecemos a todos os contribuidores e usuários que ajudaram a tornar este sistema uma realidade.\n")
    
    log_action(f"Notas de release geradas: {release_notes_filename}")
    print(f"Notas de release salvas em: {release_notes_path}")
    return release_notes_path

# Iniciar publicação de release
print_header("🚀 PUBLICANDO VERSÃO ESTÁVEL")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Definir nova versão (pode ser passada como argumento ou incrementada automaticamente)
import sys
if len(sys.argv) > 1:
    new_version = sys.argv[1]
else:
    current_version = get_or_set_version()
    version_parts = current_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)  # Incrementa a última parte (patch)
    new_version = '.'.join(version_parts)

# Atualizar versão
updated_version = get_or_set_version(new_version)
print_header(f"📌 VERSÃO ATUAL: {updated_version}")

# Definir mudanças para as notas de release
changes = [
    "Implementação completa do sistema de rotação de personas com intervalos configuráveis.",
    "Geração automática de relatórios de progresso para cada persona ativa.",
    "Ferramentas de gerenciamento de tarefas com priorização e rastreamento de status.",
    "Integração com Git para commits automáticos de relatórios com autoria das personas.",
    "Sistema de backup para configurações e relatórios, garantindo a segurança dos dados.",
    "Scripts de teste de automação para verificar o funcionamento do sistema.",
    "Testes de usabilidade simulados para identificar áreas de melhoria.",
    "Documentação abrangente com tutoriais, FAQs e exemplos detalhados."
]

# Gerar notas de release
print_header("📝 GERANDO NOTAS DE RELEASE")
release_notes_path = generate_release_notes(updated_version, changes)

# Atualizar README.md com informações de versão
print_header("📄 ATUALIZANDO README.MD")
readme_path = BASE_DIR / "README.md"
if readme_path.exists():
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    version_marker = "## Versão Atual"
    if version_marker in readme_content:
        start_idx = readme_content.find(version_marker)
        end_idx = readme_content.find("\n\n", start_idx)
        if end_idx == -1:
            end_idx = len(readme_content)
        old_version_line = readme_content[start_idx:end_idx]
        new_version_line = f"## Versão Atual: {updated_version}\nData de Lançamento: {datetime.now().strftime('%Y-%m-%d')}"
        updated_readme = readme_content.replace(old_version_line, new_version_line)
    else:
        updated_readme = readme_content + f"\n\n## Versão Atual: {updated_version}\nData de Lançamento: {datetime.now().strftime('%Y-%m-%d')}\n"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    log_action("README.md atualizado com a nova versão.")
    print(f"README.md atualizado com a versão {updated_version}.")
else:
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# Gerenciador de Projetos e Personas\n\n")
        f.write(f"## Versão Atual: {updated_version}\nData de Lançamento: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("Sistema para gerenciamento de projetos e automação de personas.\n")
    log_action("README.md criado com a nova versão.")
    print(f"README.md criado com a versão {updated_version}.")

# Resumo da publicação
print_header("✅ VERSÃO ESTÁVEL PUBLICADA")
print(f"Versão Publicada: {updated_version}")
print(f"Notas de Release: {release_notes_path}")
print(f"Log de Publicação: {RELEASE_LOG_FILE}")

# Instruções para próximos passos
print_header("📋 PRÓXIMOS PASSOS")
print("1. Compartilhe as notas de release com os usuários e stakeholders.")
print("2. Publique o repositório atualizado ou distribua os arquivos da versão estável.")
print("3. Monitore feedback dos usuários para planejar futuras melhorias ou correções.")

# Fim do script
log_action(f"Publicação da versão {updated_version} concluída.")
exit(0)
