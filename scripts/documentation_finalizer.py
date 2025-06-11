#!/usr/bin/env python3

# Script de Finalização de Documentação - Gerenciador de Projetos e Personas
# Este script auxilia na finalização da documentação do sistema, gerando ou atualizando
# tutoriais completos, FAQs e exemplos detalhados para garantir que os usuários tenham
# todas as informações necessárias para usar o sistema.

import os
import json
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
TUTORIALS_DIR = DOCS_DIR / "tutorials"
FAQS_DIR = DOCS_DIR / "faqs"
EXAMPLES_DIR = BASE_DIR / "examples"
LOGS_DIR = BASE_DIR / "scripts" / "logs"
DOC_LOG_FILE = LOGS_DIR / "documentation_finalizer.log"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(DOC_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
LOGS_DIR.mkdir(parents=True, exist_ok=True)
if not DOC_LOG_FILE.exists():
    with open(DOC_LOG_FILE, 'w') as f:
        f.write(f"Log de Finalização de Documentação - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")

# Criar diretórios de documentação se não existirem
TUTORIALS_DIR.mkdir(parents=True, exist_ok=True)
FAQS_DIR.mkdir(parents=True, exist_ok=True)
EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Função para criar ou atualizar um arquivo de tutorial
def create_tutorial(filename, title, content):
    tutorial_path = TUTORIALS_DIR / filename
    with open(tutorial_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"Última atualização: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(content)
    log_action(f"Tutorial criado ou atualizado: {filename}")
    print(f"Tutorial salvo em: {tutorial_path}")

# Função para criar ou atualizar o arquivo de FAQs
def create_faqs(filename, title, faqs_content):
    faqs_path = FAQS_DIR / filename
    with open(faqs_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"Última atualização: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(faqs_content)
    log_action(f"FAQs criados ou atualizados: {filename}")
    print(f"FAQs salvos em: {faqs_path}")

# Função para criar um exemplo de projeto
def create_example_project(project_name, description, config_data, tasks_data):
    project_dir = EXAMPLES_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar README.md para o exemplo
    with open(project_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(f"# Exemplo de Projeto: {project_name}\n\n")
        f.write(f"Descrição: {description}\n\n")
        f.write("Este diretório contém um exemplo de configuração para o Gerenciador de Projetos e Personas.\n")
        f.write("Use como referência para configurar seu próprio projeto.\n")
    
    # Criar arquivo de configuração
    with open(project_dir / "config.json", 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2)
    
    # Criar arquivo de tarefas
    with open(project_dir / "tasks.json", 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, indent=2)
    
    # Criar diretório de relatórios
    reports_dir = project_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    log_action(f"Exemplo de projeto criado: {project_name}")
    print(f"Exemplo de projeto salvo em: {project_dir}")

# Iniciar finalização da documentação
print_header("📚 FINALIZAÇÃO DA DOCUMENTAÇÃO")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Criar tutoriais
print_header("📖 CRIANDO TUTORIAIS")
tutorial_content_1 = """
## Introdução

Este tutorial guia você pelos passos básicos para configurar e usar o Gerenciador de Projetos e Personas.

### Passo 1: Instalação

1. Clone o repositório ou baixe os arquivos do projeto.
2. Certifique-se de ter o Python 3 instalado em seu sistema.
3. Execute os scripts de instalação, se houver, ou siga as instruções em INSTALACAO.md.

### Passo 2: Configuração de Personas

1. Edite o arquivo `scripts/personas/config.json` para definir as personas do seu projeto.
2. Cada persona deve ter um nome, função e prioridade.

### Passo 3: Iniciar o Sistema

1. Execute o script `monitor.py` para verificar o status inicial do sistema:
   ```
   python scripts/monitor.py
   ```
2. Use o script `rotate_personas.py` para alternar entre personas:
   ```
   python scripts/rotate_personas.py
   ```

### Passo 4: Gerenciamento de Tarefas

1. Adicione tarefas usando o script `task_manager.py`:
   ```
   python scripts/task_manager.py add "Desenvolver nova funcionalidade" P0
   ```
2. Atualize o status das tarefas conforme o progresso:
   ```
   python scripts/task_manager.py update 1 "Em Progresso"
   ```

### Passo 5: Geração de Relatórios

1. Gere relatórios de progresso para as personas ativas:
   ```
   python scripts/generate_report.py
   ```
2. Atualize campos específicos nos relatórios:
   ```
   python scripts/update_report.py Carla progress "Concluí a análise de requisitos."
   ```

## Dicas

- Execute o script de monitoramento regularmente para verificar se é necessário rotacionar personas ou gerar relatórios.
- Use o script de status do projeto para ter uma visão geral do progresso:
  ```
  python scripts/project_status.py
  ```

## Próximos Passos

Depois de configurar o sistema básico, explore funcionalidades avançadas como integração com Git e backups automáticos.
"""

create_tutorial("tutorial_basico.md", "Tutorial Básico: Configuração e Uso do Sistema", tutorial_content_1)

tutorial_content_2 = """
## Introdução

Este tutorial aborda funcionalidades avançadas do Gerenciador de Projetos e Personas, como integração com controle de versão e backups.

### Integração com Git

1. Certifique-se de que o Git está instalado e que seu diretório de projeto é um repositório Git.
2. Execute o script de integração para commitar relatórios com autoria das personas:
   ```
   python scripts/git_integration.py
   ```
3. Verifique o histórico de commits para ver os relatórios commitados:
   ```
   git log --author="Nome da Persona"
   ```

### Sistema de Backup

1. Execute o script de backup para salvar configurações e relatórios:
   ```
   python scripts/backup_system.py
   ```
2. Para restaurar um backup, use:
   ```
   python scripts/backup_system.py restore backup_system_YYYYMMDD_HHMMSS.zip
   ```

### Notificações

1. Configure notificações para alertar sobre rotação de personas ou relatórios pendentes:
   ```
   python scripts/notify.py
   ```

### Testes de Automação

1. Execute os casos de teste para verificar o funcionamento dos scripts:
   ```
   python scripts/test_automation.py
   ```

## Dicas Avançadas

- Automatize backups e notificações usando cron jobs ou tarefas agendadas no Windows.
- Use o script de diagnóstico para identificar problemas no sistema:
  ```
  python scripts/diagnostics.py
  ```

## Personalização

Adapte os scripts conforme necessário para atender às necessidades específicas do seu projeto. Por exemplo, modifique os intervalos de rotação no arquivo de configuração.
"""

create_tutorial("tutorial_avancado.md", "Tutorial Avançado: Integrações e Funcionalidades", tutorial_content_2)

# Criar FAQs
print_header("❓ CRIANDO FAQs")
faqs_content = """
## Perguntas Frequentes (FAQs)

### 1. O que é o Gerenciador de Projetos e Personas?

É um sistema para gerenciar projetos e personas, automatizando tarefas como rotação de personas, geração de relatórios e rastreamento de progresso.

### 2. Como configuro as personas para meu projeto?

Edite o arquivo `scripts/personas/config.json` e adicione as personas com seus respectivos nomes, funções e prioridades. Veja o exemplo fornecido para referência.

### 3. Como alterno entre personas durante o desenvolvimento?

Execute o script `rotate_personas.py` para alternar automaticamente entre personas com base nos intervalos configurados:
```
python scripts/rotate_personas.py
```

### 4. Como gero relatórios de progresso?

Use o script `generate_report.py` para criar relatórios para todas as personas ativas:
```
python scripts/generate_report.py
```

### 5. Posso integrar este sistema com ferramentas de controle de versão como Git?

Sim, use o script `git_integration.py` para commitar relatórios automaticamente com autoria das personas:
```
python scripts/git_integration.py
```

### 6. Como faço backup dos dados do sistema?

Execute o script `backup_system.py` para criar um backup de configurações e relatórios:
```
python scripts/backup_system.py
```

### 7. O que faço se encontrar um problema no sistema?

Execute o script de diagnóstico para identificar possíveis problemas:
```
python scripts/diagnostics.py
```
Entre em contato com a equipe de suporte ou abra uma issue no repositório do projeto.

### 8. Como testo se os scripts estão funcionando corretamente?

Use o script de testes de automação para verificar o funcionamento dos scripts principais:
```
python scripts/test_automation.py
```

### 9. Posso personalizar os intervalos de rotação e geração de relatórios?

Sim, edite os parâmetros no arquivo de configuração `scripts/personas/config.json` para ajustar os intervalos conforme necessário.

### 10. Onde encontro exemplos de uso do sistema?

Consulte o diretório `examples/` para ver projetos de exemplo com configurações e relatórios. Use-os como referência para configurar seu próprio projeto.
"""

create_faqs("faqs.md", "Perguntas Frequentes sobre o Gerenciador de Projetos e Personas", faqs_content)

# Criar exemplos de projetos
print_header("📂 CRIANDO EXEMPLOS DE PROJETOS")
example_config = {
    "personas": [
        {"name": "Alice", "role": "Gerente de Produto", "priority": "P0"},
        {"name": "Bob", "role": "Desenvolvedor Frontend", "priority": "P0"},
        {"name": "Charlie", "role": "Desenvolvedor Backend", "priority": "P1"}
    ],
    "rotation_interval": 900,
    "report_interval": 1800,
    "active_count": 2
}

example_tasks = {
    "tasks": [
        {"id": 1, "description": "Definir requisitos do projeto", "priority": "P0", "status": "Concluído", "assigned_to": "Alice"},
        {"id": 2, "description": "Desenvolver interface do usuário", "priority": "P0", "status": "Em Progresso", "assigned_to": "Bob"},
        {"id": 3, "description": "Implementar API backend", "priority": "P1", "status": "Pendente", "assigned_to": "Charlie"}
    ]
}

create_example_project("projeto_exemplo_web", "Exemplo de um projeto de desenvolvimento web", example_config, example_tasks)

# Resumo da finalização da documentação
print_header("✅ DOCUMENTAÇÃO FINALIZADA")
print(f"Tutoriais criados em: {TUTORIALS_DIR}")
print(f"FAQs criados em: {FAQS_DIR}")
print(f"Exemplos de projetos criados em: {EXAMPLES_DIR}")
print(f"Log de Documentação: {DOC_LOG_FILE}")

# Instruções para próximos passos
print_header("📋 PRÓXIMOS PASSOS")
print("1. Revise os tutoriais e FAQs gerados para adicionar detalhes específicos do seu projeto.")
print("2. Adicione mais exemplos de projetos no diretório 'examples/' conforme necessário.")
print("3. Publique a documentação atualizada junto com a versão estável do sistema.")

# Fim do script
log_action("Finalização da documentação concluída.")
exit(0)
