#!/usr/bin/env python3

# Script de Testes de Automação - Gerenciador de Projetos e Personas
# Este script executa casos de teste para verificar o funcionamento dos scripts de automação,
# incluindo rotação de personas, geração de relatórios e gerenciamento de tarefas.

import os
import json
import sys
import unittest
from pathlib import Path
from datetime import datetime
import subprocess
import time

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
STATE_FILE = SCRIPTS_DIR / "state" / "agent_state.json"
CONFIG_FILE = SCRIPTS_DIR / "personas" / "config.json"
TASKS_FILE = SCRIPTS_DIR / "tasks" / "tasks.json"
REPORTS_DIR = SCRIPTS_DIR / "reports"
LOGS_DIR = SCRIPTS_DIR / "logs"
TEST_LOG_FILE = LOGS_DIR / "test_automation.log"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(TEST_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
LOGS_DIR.mkdir(parents=True, exist_ok=True)
if not TEST_LOG_FILE.exists():
    with open(TEST_LOG_FILE, 'w') as f:
        f.write(f"Log de Testes de Automação - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")

# Classe de testes
class TestAutomationScripts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para os testes."""
        print_header("🔧 CONFIGURAÇÃO INICIAL DOS TESTES")
        log_action("Iniciando configuração para testes de automação.")
        
        # Verificar se os arquivos de configuração existem
        if not CONFIG_FILE.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado em {CONFIG_FILE}")
        if not STATE_FILE.exists():
            # Inicializar estado se não existir
            with open(STATE_FILE, 'w') as f:
                json.dump({
                    "active_personas": [],
                    "last_rotation": 0,
                    "last_report": 0
                }, f, indent=2)
            log_action("Arquivo de estado inicializado.")
        
        # Criar diretórios necessários
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        TASKS_DIR = SCRIPTS_DIR / "tasks"
        TASKS_DIR.mkdir(parents=True, exist_ok=True)
        if not TASKS_FILE.exists():
            with open(TASKS_FILE, 'w') as f:
                json.dump({"tasks": []}, f, indent=2)
            log_action("Arquivo de tarefas inicializado.")

    def setUp(self):
        """Configuração antes de cada teste."""
        self.start_time = datetime.now()
        log_action(f"Iniciando teste: {self._testMethodName}")

    def tearDown(self):
        """Limpeza após cada teste."""
        duration = datetime.now() - self.start_time
        log_action(f"Teste concluído: {self._testMethodName} (Duração: {duration.total_seconds():.2f} segundos)")

    def test_monitor_script(self):
        """Teste para verificar o script de monitoramento."""
        print_header("🖥️ TESTE: SCRIPT DE MONITORAMENTO")
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "monitor.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar monitor.py: {result.stderr}")
        self.assertIn("STATUS DO SISTEMA", result.stdout, "Saída do monitor.py não contém o status esperado.")
        log_action("Teste de script de monitoramento: PASSOU")

    def test_rotate_personas_script(self):
        """Teste para verificar o script de rotação de personas."""
        print_header("🔄 TESTE: SCRIPT DE ROTAÇÃO DE PERSONAS")
        # Obter estado inicial
        with open(STATE_FILE, 'r') as f:
            initial_state = json.load(f)
        initial_personas = initial_state["active_personas"]
        
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "rotate_personas.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar rotate_personas.py: {result.stderr}")
        
        # Verificar se houve alteração nas personas ativas
        with open(STATE_FILE, 'r') as f:
            updated_state = json.load(f)
        updated_personas = updated_state["active_personas"]
        updated_rotation_time = updated_state["last_rotation"]
        
        self.assertNotEqual(initial_personas, updated_personas, "Personas ativas não foram alteradas após rotação.")
        self.assertGreater(updated_rotation_time, initial_state["last_rotation"], "Tempo de última rotação não foi atualizado.")
        log_action("Teste de script de rotação de personas: PASSOU")

    def test_generate_report_script(self):
        """Teste para verificar o script de geração de relatórios."""
        print_header("📝 TESTE: SCRIPT DE GERAÇÃO DE RELATÓRIOS")
        # Garantir que haja pelo menos uma persona ativa
        with open(STATE_FILE, 'r') as f:
            state_data = json.load(f)
        if not state_data["active_personas"]:
            with open(CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
            state_data["active_personas"] = [config_data["personas"][0]["name"]]
            with open(STATE_FILE, 'w') as f:
                json.dump(state_data, f, indent=2)
        
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "generate_report.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar generate_report.py: {result.stderr}")
        
        # Verificar se relatórios foram gerados
        persona = state_data["active_personas"][0]
        report_dir = REPORTS_DIR / persona
        report_files = list(report_dir.glob("report_*.md"))
        self.assertGreater(len(report_files), 0, f"Nenhum relatório gerado para a persona {persona}.")
        log_action("Teste de script de geração de relatórios: PASSOU")

    def test_update_report_script(self):
        """Teste para verificar o script de atualização de relatórios."""
        print_header("✏️ TESTE: SCRIPT DE ATUALIZAÇÃO DE RELATÓRIOS")
        # Garantir que haja um relatório para atualizar
        with open(STATE_FILE, 'r') as f:
            state_data = json.load(f)
        if not state_data["active_personas"]:
            with open(CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
            state_data["active_personas"] = [config_data["personas"][0]["name"]]
            with open(STATE_FILE, 'w') as f:
                json.dump(state_data, f, indent=2)
        
        persona = state_data["active_personas"][0]
        result_gen = subprocess.run([sys.executable, str(SCRIPTS_DIR / "generate_report.py")], capture_output=True, text=True)
        self.assertEqual(result_gen.returncode, 0, f"Erro ao gerar relatório para teste: {result_gen.stderr}")
        
        # Atualizar relatório
        test_progress = "Progresso de teste atualizado via script de automação."
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "update_report.py"), persona, "progress", test_progress], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar update_report.py: {result.stderr}")
        
        # Verificar se o relatório foi atualizado
        report_dir = REPORTS_DIR / persona
        latest_report = max(report_dir.glob("report_*.md"), key=os.path.getmtime, default=None)
        self.assertIsNotNone(latest_report, f"Nenhum relatório encontrado para {persona}.")
        with open(latest_report, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn(test_progress, content, "Conteúdo do relatório não foi atualizado.")
        log_action("Teste de script de atualização de relatórios: PASSOU")

    def test_task_manager_script(self):
        """Teste para verificar o script de gerenciamento de tarefas."""
        print_header("📋 TESTE: SCRIPT DE GERENCIAMENTO DE TAREFAS")
        # Adicionar uma tarefa de teste
        test_task_desc = "Tarefa de teste criada por test_automation.py"
        result_add = subprocess.run([sys.executable, str(SCRIPTS_DIR / "task_manager.py"), "add", test_task_desc, "P2"], capture_output=True, text=True)
        self.assertEqual(result_add.returncode, 0, f"Erro ao adicionar tarefa: {result_add.stderr}")
        
        # Verificar se a tarefa foi adicionada
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
        tasks_list = tasks_data.get("tasks", [])
        self.assertGreater(len(tasks_list), 0, "Nenhuma tarefa encontrada no arquivo.")
        self.assertTrue(any(task["description"] == test_task_desc for task in tasks_list), "Tarefa de teste não encontrada.")
        log_action("Teste de script de gerenciamento de tarefas (adicionar): PASSOU")
        
        # Atualizar status da tarefa
        task_id = next((task["id"] for task in tasks_list if task["description"] == test_task_desc), None)
        self.assertIsNotNone(task_id, "ID da tarefa de teste não encontrado.")
        result_update = subprocess.run([sys.executable, str(SCRIPTS_DIR / "task_manager.py"), "update", str(task_id), "Em Progresso"], capture_output=True, text=True)
        self.assertEqual(result_update.returncode, 0, f"Erro ao atualizar tarefa: {result_update.stderr}")
        
        # Verificar atualização
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
        updated_task = next((task for task in tasks_data["tasks"] if task["id"] == task_id), None)
        self.assertIsNotNone(updated_task, "Tarefa atualizada não encontrada.")
        self.assertEqual(updated_task["status"], "Em Progresso", "Status da tarefa não foi atualizado.")
        log_action("Teste de script de gerenciamento de tarefas (atualizar): PASSOU")

    def test_project_status_script(self):
        """Teste para verificar o script de status do projeto."""
        print_header("📊 TESTE: SCRIPT DE STATUS DO PROJETO")
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "project_status.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar project_status.py: {result.stderr}")
        self.assertIn("STATUS DO PROJETO", result.stdout, "Saída do project_status.py não contém o status esperado.")
        log_action("Teste de script de status do projeto: PASSOU")

    def test_notify_script(self):
        """Teste para verificar o script de notificações."""
        print_header("🔔 TESTE: SCRIPT DE NOTIFICAÇÕES")
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "notify.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erro ao executar notify.py: {result.stderr}")
        self.assertIn("STATUS DAS NOTIFICAÇÕES", result.stdout, "Saída do notify.py não contém o status esperado.")
        log_action("Teste de script de notificações: PASSOU")

if __name__ == '__main__':
    print_header("🚀 INICIANDO TESTES DE AUTOMAÇÃO")
    log_action("Iniciando execução de testes de automação.")
    unittest.main(verbosity=2)
