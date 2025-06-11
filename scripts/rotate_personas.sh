#!/bin/bash

# Script de Rotação de Personas - Gerenciador de Projetos e Personas
# Este script realiza a rotação de personas com base nas prioridades e no intervalo
# configurado, garantindo que todas as perspectivas sejam consideradas regularmente.

# Definir o diretório base do projeto
BASE_DIR="$(dirname "$(dirname "$0")")"
CONFIG_FILE="$BASE_DIR/scripts/personas/config.json"
STATE_FILE="$BASE_DIR/scripts/state/agent_state.json"

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
    mkdir -p "$BASE_DIR/scripts/state"
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

# Ler estado atual
ACTIVE_PERSONAS=$(jq -r '.active_personas' "$STATE_FILE")
LAST_ROTATION=$(jq -r '.last_rotation' "$STATE_FILE")
CURRENT_TIME=$(date +%s)

# Calcular tempo desde a última rotação
TIME_SINCE_ROTATION=$((CURRENT_TIME - LAST_ROTATION))

# Verificar se a rotação é necessária
if [ "$TIME_SINCE_ROTATION" -lt "$ROTATION_INTERVAL" ]; then
    print_header "⏳ ROTAÇÃO NÃO NECESSÁRIA"
    echo "Tempo desde a última rotação: $TIME_SINCE_ROTATION segundos."
    echo "Intervalo configurado: $ROTATION_INTERVAL segundos."
    echo "Rotação não é necessária no momento."
    echo "Personas ativas: $(echo "$ACTIVE_PERSONAS" | jq -r 'join(", ")')"
    exit 0
fi

# Lógica de rotação de personas
# Selecionar novas personas com base na prioridade (P0 tem maior peso)
# Este é um exemplo simplificado: seleciona 3 personas, priorizando P0, depois P1, depois P2
P0_PERSONAS=$(echo "$PERSONAS" | jq -r '[.[] | select(.priority == "P0")].name')
P1_PERSONAS=$(echo "$PERSONAS" | jq -r '[.[] | select(.priority == "P1")].name')
P2_PERSONAS=$(echo "$PERSONAS" | jq -r '[.[] | select(.priority == "P2")].name')

# Contar o número de personas em cada prioridade
P0_COUNT=$(echo "$P0_PERSONAS" | jq -r 'length')
P1_COUNT=$(echo "$P1_PERSONAS" | jq -r 'length')
P2_COUNT=$(echo "$P2_PERSONAS" | jq -r 'length')

# Inicializar nova lista de personas ativas
NEW_ACTIVE_PERSONAS="[]"

# Selecionar pelo menos uma persona P0 se disponível
if [ "$P0_COUNT" -gt 0 ]; then
    # Selecionar uma persona P0 aleatoriamente
    P0_INDEX=$((RANDOM % P0_COUNT))
    SELECTED_P0=$(echo "$P0_PERSONAS" | jq -r ".[$P0_INDEX]")
    NEW_ACTIVE_PERSONAS=$(echo "$NEW_ACTIVE_PERSONAS" | jq -r ". + [\"$SELECTED_P0\"]")
fi

# Preencher até 3 personas, priorizando P0, depois P1, depois P2
for i in $(seq 1 2); do
    if [ "$P0_COUNT" -gt "$i" ]; then
        P0_INDEX=$((RANDOM % P0_COUNT))
        SELECTED_P0=$(echo "$P0_PERSONAS" | jq -r ".[$P0_INDEX]")
        if ! echo "$NEW_ACTIVE_PERSONAS" | grep -q "$SELECTED_P0"; then
            NEW_ACTIVE_PERSONAS=$(echo "$NEW_ACTIVE_PERSONAS" | jq -r ". + [\"$SELECTED_P0\"]")
        fi
    elif [ "$P1_COUNT" -gt 0 ]; then
        P1_INDEX=$((RANDOM % P1_COUNT))
        SELECTED_P1=$(echo "$P1_PERSONAS" | jq -r ".[$P1_INDEX]")
        if ! echo "$NEW_ACTIVE_PERSONAS" | grep -q "$SELECTED_P1"; then
            NEW_ACTIVE_PERSONAS=$(echo "$NEW_ACTIVE_PERSONAS" | jq -r ". + [\"$SELECTED_P1\"]")
        fi
    elif [ "$P2_COUNT" -gt 0 ]; then
        P2_INDEX=$((RANDOM % P2_COUNT))
        SELECTED_P2=$(echo "$P2_PERSONAS" | jq -r ".[$P2_INDEX]")
        if ! echo "$NEW_ACTIVE_PERSONAS" | grep -q "$SELECTED_P2"; then
            NEW_ACTIVE_PERSONAS=$(echo "$NEW_ACTIVE_PERSONAS" | jq -r ". + [\"$SELECTED_P2\"]")
        fi
    fi
done

# Atualizar o estado com as novas personas ativas e o timestamp da rotação
NEW_STATE=$(jq -r ".active_personas = $NEW_ACTIVE_PERSONAS | .last_rotation = $CURRENT_TIME" "$STATE_FILE")
echo "$NEW_STATE" > "$STATE_FILE"

# Exibir resultado da rotação
print_header "🔄 ROTAÇÃO DE PERSONAS REALIZADA"
echo "Novas personas ativas: $(echo "$NEW_ACTIVE_PERSONAS" | jq -r 'join(", ")')"
echo "Última rotação atualizada para: $(date -d "@$CURRENT_TIME")"
echo "Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'."

# Fim do script
exit 0
