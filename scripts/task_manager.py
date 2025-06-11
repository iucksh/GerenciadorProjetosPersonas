#!/usr/bin/env python3

# Script de Gerenciamento de Tarefas - Gerenciador de Projetos e Personas
# Este script permite criar, listar, atualizar e marcar tarefas como concluídas,
# ajudando no rastreamento do progresso do projeto com base em prioridades.

import os
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
TASKS_FILE = BASE_DIR / "scripts" / "tasks" / "tasks.json"
CONFIG_FILE = BASE_DIR / "scripts" / "personas" / "config.json"

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
    TASKS_DIR = BASE_DIR / "scripts" / "tasks"
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        with open(TASKS_FILE, 'w') as f:
            json.dump({"tasks": []}, f)

# Verificar se o arquivo de configuração existe
check_file(CONFIG_FILE)
setup_directories()

# Ler personas do arquivo de configuração para validação de responsáveis
with open(CONFIG_FILE, 'r') as f:
    config_data = json.load(f)
    PERSONAS = [p["name"] for p in config_data["personas"]]

# Função para ler tarefas do arquivo
def read_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)["tasks"]

# Função para salvar tarefas no arquivo
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump({"tasks": tasks}, f, indent=2)

# Função para adicionar uma nova tarefa
def add_task(description, priority, assignee):
    tasks = read_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "priority": priority,
        "assignee": assignee,
        "status": "Pendente",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": ""
    }
    tasks.append(task)
    save_tasks(tasks)
    print_header("✅ TAREFA ADICIONADA")
    print(f"Tarefa ID {task_id} adicionada com sucesso.")
    print(f"Descrição: {description}")
    print(f"Prioridade: {priority}")
    print(f"Responsável: {assignee}")

# Função para listar tarefas
def list_tasks(status_filter=None, priority_filter=None, assignee_filter=None):
    tasks = read_tasks()
    filtered_tasks = tasks
    
    if status_filter:
        filtered_tasks = [t for t in filtered_tasks if t["status"].lower() == status_filter.lower()]
    if priority_filter:
        filtered_tasks = [t for t in filtered_tasks if t["priority"].lower() == priority_filter.lower()]
    if assignee_filter:
        filtered_tasks = [t for t in filtered_tasks if t["assignee"].lower() == assignee_filter.lower()]
    
    print_header("📋 LISTA DE TAREFAS")
    if not filtered_tasks:
        print("Nenhuma tarefa encontrada com os filtros aplicados.")
    else:
        for task in filtered_tasks:
            print(f"ID: {task['id']}")
            print(f"Descrição: {task['description']}")
            print(f"Prioridade: {task['priority']}")
            print(f"Responsável: {task['assignee']}")
            print(f"Status: {task['status']}")
            print(f"Criada em: {task['created']}")
            if task['completed']:
                print(f"Concluída em: {task['completed']}")
            print("-" * 30)

# Função para atualizar o status de uma tarefa
def update_task(task_id, status):
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            if status == "Concluída":
                task["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                task["completed"] = ""
            save_tasks(tasks)
            print_header("✅ TAREFA ATUALIZADA")
            print(f"Tarefa ID {task_id} atualizada para status '{status}'.")
            return
    print_header("❌ TAREFA NÃO ENCONTRADA")
    print(f"Tarefa ID {task_id} não encontrada.")

# Função para editar descrição, prioridade ou responsável de uma tarefa
def edit_task(task_id, description=None, priority=None, assignee=None):
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if description:
                task["description"] = description
            if priority:
                task["priority"] = priority
            if assignee:
                task["assignee"] = assignee
            save_tasks(tasks)
            print_header("✅ TAREFA EDITADA")
            print(f"Tarefa ID {task_id} editada com sucesso.")
            if description:
                print(f"Nova descrição: {description}")
            if priority:
                print(f"Nova prioridade: {priority}")
            if assignee:
                print(f"Novo responsável: {assignee}")
            return
    print_header("❌ TAREFA NÃO ENCONTRADA")
    print(f"Tarefa ID {task_id} não encontrada.")

# Configurar o parser de argumentos
parser = argparse.ArgumentParser(description="Gerenciador de Tarefas para Projetos e Personas")
subparsers = parser.add_subparsers(dest="command")

# Parser para adicionar tarefa
add_parser = subparsers.add_parser("add", help="Adicionar uma nova tarefa")
add_parser.add_argument("description", type=str, help="Descrição da tarefa")
add_parser.add_argument("priority", type=str, choices=["P0", "P1", "P2"], help="Prioridade da tarefa (P0, P1, P2)")
add_parser.add_argument("assignee", type=str, help="Responsável pela tarefa")

# Parser para listar tarefas
list_parser = subparsers.add_parser("list", help="Listar tarefas")
list_parser.add_argument("--status", type=str, help="Filtrar por status (ex.: Pendente, Concluída)")
list_parser.add_argument("--priority", type=str, choices=["P0", "P1", "P2"], help="Filtrar por prioridade")
list_parser.add_argument("--assignee", type=str, help="Filtrar por responsável")

# Parser para atualizar status de tarefa
update_parser = subparsers.add_parser("update", help="Atualizar status de uma tarefa")
update_parser.add_argument("id", type=int, help="ID da tarefa")
update_parser.add_argument("status", type=str, choices=["Pendente", "Em Progresso", "Concluída"], help="Novo status da tarefa")

# Parser para editar tarefa
edit_parser = subparsers.add_parser("edit", help="Editar descrição, prioridade ou responsável de uma tarefa")
edit_parser.add_argument("id", type=int, help="ID da tarefa")
edit_parser.add_argument("--description", type=str, help="Nova descrição da tarefa")
edit_parser.add_argument("--priority", type=str, choices=["P0", "P1", "P2"], help="Nova prioridade da tarefa")
edit_parser.add_argument("--assignee", type=str, help="Novo responsável pela tarefa")

args = parser.parse_args()

# Validar e executar comandos
if args.command == "add":
    if args.assignee not in PERSONAS:
        print_header("❌ RESPONSÁVEL INVÁLIDO")
        print(f"Responsável '{args.assignee}' não encontrado nas personas configuradas.")
        print(f"Personas disponíveis: {', '.join(PERSONAS)}")
        exit(1)
    add_task(args.description, args.priority, args.assignee)
elif args.command == "list":
    list_tasks(args.status, args.priority, args.assignee)
elif args.command == "update":
    update_task(args.id, args.status)
elif args.command == "edit":
    if not any([args.description, args.priority, args.assignee]):
        print_header("❌ NENHUMA ALTERAÇÃO FORNECIDA")
        print("Forneça pelo menos um campo para editar (descrição, prioridade ou responsável).")
        exit(1)
    if args.assignee and args.assignee not in PERSONAS:
        print_header("❌ RESPONSÁVEL INVÁLIDO")
        print(f"Responsável '{args.assignee}' não encontrado nas personas configuradas.")
        print(f"Personas disponíveis: {', '.join(PERSONAS)}")
        exit(1)
    edit_task(args.id, args.description, args.priority, args.assignee)
else:
    print_header("❌ COMANDO INVÁLIDO")
    parser.print_help()
    exit(1)

# Fim do script
exit(0)
