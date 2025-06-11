#!/bin/bash

# Script de Monitoramento - Gerenciador de Projetos e Personas
# Este script verifica o status atual do sistema, identifica personas ativas,
# verifica a necessidade de rotação de personas e geração de relatórios,
# e exibe o status geral do projeto.

# Definir o diretório base do projeto
BASE_DIR="$(dirname "$(dirname "$0")")"
CONFIG_FILE="$BASE_DIR/scripts/personas/config.json"
STATE_FILE="$BASE_DIR/scripts/state/agent_state.json"
REPORTS_DIR="$BASE_DIR/scripts/reports"

# Função para exibir mensagens formatadas
print_header() {
    echo "============================================================="
    echo "$1"
    echo "============================================================="
}

# Função para verificar se um arquivo existe e é legível
check_file() {
    if [ ! -f "$1" ] || [ ! -r "$1" ]; then
        echo "Erro: Arquivo $1 não encontrado ou não é legível."
        exit 1
    fi
}

# Função para criar diretórios necessários se não existirem
setup_directories() {
    mkdir -p "$REPORTS_DIR" "$BASE_DIR/scripts/state"
    if [ ! -f "$STATE_FILE" ]; then
        echo '{"active_personas":[],"last_rotation":0,"last_report":0}' > "$STATE_FILE"
    fi
}

# Verificar se os arquivos de configuração e estado existem
check_file "$CONFIG_FILE"
setup_directories
check_file "$STATE_FILE"

# Ler dados do arquivo de configuração
PERSONAS=$(jq -r '.personas' "$CONFIG_FILE")
ROTATION_INTERVAL=$(jq -r '.rotation_interval' "$CONFIG_FILE")
REPORT_INTERVAL=$(jq -r '.report_interval' "$CONFIG_FILE")

# Ler estado atual
ACTIVE_PERSONAS=$(jq -r '.active_personas' "$STATE_FILE")
LAST_ROTATION=$(jq -r '.last_rotation' "$STATE_FILE")
LAST_REPORT=$(jq -r '.last_report' "$STATE_FILE")

# Obter timestamp atual
CURRENT_TIME=$(date +%s)

# Calcular tempo desde a última rotação e último relatório
TIME_SINCE_ROTATION=$((CURRENT_TIME - LAST_ROTATION))
TIME_SINCE_REPORT=$((CURRENT_TIME - LAST_REPORT))

# Verificar necessidade de rotação de personas
NEED_ROTATION=false
if [ "$TIME_SINCE_ROTATION" -ge "$ROTATION_INTERVAL" ]; then
    NEED_ROTATION=true
fi

# Verificar necessidade de geração de relatórios
NEED_REPORT=false
if [ "$TIME_SINCE_REPORT" -ge "$REPORT_INTERVAL" ]; then
    NEED_REPORT=true
fi

# Exibir status atual
print_header "📊 STATUS DO PROJETO"
echo "Status do Projeto:"
echo "- Progresso geral: Ainda não implementado (aguardando script de status do projeto)."
echo "- Tarefas pendentes: Ainda não implementado (aguardando script de tarefas)."

# Exibir personas ativas ou necessidade de rotação
if [ "$NEED_ROTATION" = true ]; then
    print_header "📢 ALTERAÇÃO DE PERSONAS NECESSÁRIA"
    echo "PROMPT DE TRANSIÇÃO:"
    echo "- Necessidade de nova rotação de personas detectada."
    echo "- Execute './scripts/rotate_personas.sh' para alternar personas."
else
    print_header "👥 PERSONAS ATUAIS"
    if [ "$ACTIVE_PERSONAS" = "[]" ] || [ -z "$ACTIVE_PERSONAS" ]; then
        echo "Nenhuma persona ativa no momento. Execute './scripts/rotate_personas.sh' para iniciar."
    else
        echo "Personas ativas: $(echo "$ACTIVE_PERSONAS" | jq -r 'join(", ")')"
    fi
fi

# Exibir necessidade de relatórios
if [ "$NEED_REPORT" = true ]; then
    print_header "📝 RELATÓRIOS DE PROGRESSO NECESSÁRIOS"
    echo "Personas que precisam atualizar seus relatórios:"
    if [ "$ACTIVE_PERSONAS" = "[]" ] || [ -z "$ACTIVE_PERSONAS" ]; then
        echo "Nenhuma persona ativa para relatórios."
    else
        echo "$ACTIVE_PERSONAS" | jq -r '.[]'
    fi
fi

# Instruções finais
echo "============================================================="
echo "Para mais informações sobre os próximos passos, consulte os fluxos de trabalho em 'docs/FLUXOS.md'."
echo "============================================================="

# Fim do script
exit 0
