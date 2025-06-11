#!/usr/bin/env python3

# Script de Testes de Usabilidade - Gerenciador de Projetos e Personas
# Este script simula testes de usabilidade com personas para identificar pontos de melhoria
# no sistema, coletando feedback sobre a experiência do usuário.

import os
import json
import random
from pathlib import Path
from datetime import datetime

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
CONFIG_FILE = SCRIPTS_DIR / "personas" / "config.json"
LOGS_DIR = SCRIPTS_DIR / "logs"
USABILITY_LOG_FILE = LOGS_DIR / "usability_testing.log"
FEEDBACK_FILE = SCRIPTS_DIR / "usability_feedback.json"

# Função para exibir mensagens formatadas
def print_header(message):
    print("=" * 61)
    print(message)
    print("=" * 61)

# Função para registrar ação no log
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(USABILITY_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Ação registrada: {message}")

# Configurar diretórios e arquivos necessários
LOGS_DIR.mkdir(parents=True, exist_ok=True)
if not USABILITY_LOG_FILE.exists():
    with open(USABILITY_LOG_FILE, 'w') as f:
        f.write(f"Log de Testes de Usabilidade - Iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")

if not FEEDBACK_FILE.exists():
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump({"feedback": []}, f, indent=2)

# Função para carregar configurações de personas
def load_personas_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Arquivo de configuração de personas não encontrado em {CONFIG_FILE}")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Função para simular feedback de usabilidade de uma persona
def simulate_usability_feedback(persona_name, persona_role):
    feedback_categories = {
        "Facilidade de Uso": ["Muito fácil de usar", "Razoavelmente fácil", "Neutro", "Difícil de usar", "Muito difícil"],
        "Clareza da Interface": ["Muito clara", "Razoavelmente clara", "Neutro", "Confusa", "Muito confusa"],
        "Utilidade das Funcionalidades": ["Muito útil", "Razoavelmente útil", "Neutro", "Pouco útil", "Inútil"],
        "Velocidade de Resposta": ["Muito rápida", "Razoavelmente rápida", "Neutro", "Lenta", "Muito lenta"],
        "Satisfação Geral": ["Muito satisfeito", "Razoavelmente satisfeito", "Neutro", "Insatisfeito", "Muito insatisfeito"]
    }
    
    feedback = {
        "persona": persona_name,
        "role": persona_role,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ratings": {},
        "comments": []
    }
    
    # Simular avaliações para cada categoria
    for category, options in feedback_categories.items():
        feedback["ratings"][category] = random.choice(options)
    
    # Adicionar comentários simulados com base nas avaliações
    for category, rating in feedback["ratings"].items():
        if "Muito difícil" in rating or "Muito confusa" in rating or "Inútil" in rating or "Muito lenta" in rating or "Muito insatisfeito" in rating:
            feedback["comments"].append(f"{category}: Precisa de melhorias significativas. {rating}.")
        elif "Difícil" in rating or "Confusa" in rating or "Pouco útil" in rating or "Lenta" in rating or "Insatisfeito" in rating:
            feedback["comments"].append(f"{category}: Poderia ser mais intuitivo. {rating}.")
        else:
            feedback["comments"].append(f"{category}: Experiência aceitável. {rating}.")
    
    return feedback

# Função para salvar feedback
def save_feedback(feedback_data):
    with open(FEEDBACK_FILE, 'r') as f:
        feedback_collection = json.load(f)
    
    feedback_collection["feedback"].append(feedback_data)
    
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_collection, f, indent=2)
    
    log_action(f"Feedback de usabilidade salvo para {feedback_data['persona']}.")

# Iniciar testes de usabilidade
print_header("🧪 TESTES DE USABILIDADE")
print(f"Data/Hora Atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Carregar configurações de personas
config_data = load_personas_config()
personas = config_data["personas"]

# Simular feedback de usabilidade para cada persona
print_header("📊 SIMULANDO FEEDBACK DE USABILIDADE")
for persona in personas:
    persona_name = persona["name"]
    persona_role = persona["role"]
    print(f"Gerando feedback para {persona_name} ({persona_role})...")
    feedback = simulate_usability_feedback(persona_name, persona_role)
    save_feedback(feedback)

# Resumo dos feedbacks coletados
print_header("📋 RESUMO DOS FEEDBACKS")
with open(FEEDBACK_FILE, 'r') as f:
    feedback_collection = json.load(f)

feedback_list = feedback_collection["feedback"]
if feedback_list:
    for i, fb in enumerate(feedback_list, 1):
        print(f"{i}. {fb['persona']} ({fb['role']}) - {fb['timestamp']}")
        for category, rating in fb['ratings'].items():
            print(f"   - {category}: {rating}")
        for comment in fb['comments'][:2]:  # Mostrar apenas os dois primeiros comentários para brevidade
            print(f"     * {comment}")
        if len(fb['comments']) > 2:
            print(f"     * ... e mais {len(fb['comments']) - 2} comentários.")
else:
    print("Nenhum feedback coletado.")

# Análise de áreas de melhoria
print_header("🔍 ÁREAS DE MELHORIA IDENTIFICADAS")
improvement_areas = {}
for fb in feedback_list:
    for category, rating in fb['ratings'].items():
        if category not in improvement_areas:
            improvement_areas[category] = {"negative": 0, "total": 0}
        improvement_areas[category]["total"] += 1
        if "Difícil" in rating or "Confusa" in rating or "Inútil" in rating or "Lenta" in rating or "Insatisfeito" in rating:
            improvement_areas[category]["negative"] += 1

for category, stats in improvement_areas.items():
    negative_percentage = (stats["negative"] / stats["total"]) * 100
    if negative_percentage > 30:  # Threshold para destacar áreas problemáticas
        print(f"⚠️ {category}: {negative_percentage:.1f}% de feedback negativo ({stats['negative']}/{stats['total']})")
    else:
        print(f"✅ {category}: {negative_percentage:.1f}% de feedback negativo ({stats['negative']}/{stats['total']})")

# Instruções para testes reais
print_header("ℹ️ REALIZANDO TESTES DE USABILIDADE REAIS")
print("Este script simula feedback de usabilidade. Para testes reais:")
print("1. Convide usuários reais ou stakeholders para usar o sistema.")
print("2. Peça que realizem tarefas específicas (ex.: criar tarefas, gerar relatórios).")
print("3. Colete feedback por meio de formulários ou entrevistas.")
print("4. Registre manualmente o feedback no arquivo usability_feedback.json para análise.")
print(f"Arquivo de Feedback: {FEEDBACK_FILE}")
print(f"Log de Testes de Usabilidade: {USABILITY_LOG_FILE}")

# Fim do script
log_action("Testes de usabilidade concluídos.")
exit(0)
