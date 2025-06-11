#!/bin/bash

# Script de Geração de Relatórios - Gerenciador de Projetos e Personas
# Este script gera relatórios de progresso para as personas ativas,
# salvando-os no diretório de relatórios com a data atual.

# Definir o diretório base do projeto
BASE_DIR="$(dirname "$(dirname "$0")")"
CONFIG_FILE="$BASE_DIR/scripts/personas/config.json"
STATE_FILE="$BASE_DIR/scripts/state/agent_state.json"
REPORTS_DIR="$BASE_DIR/scripts/reports"
TEMPLATE_FILE="$BASE_DIR/scripts/report_template.md"

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
    # Criar subdiretórios para cada persona
    while IFS= read -r persona_name; do
        mkdir -p "$REPORTS_DIR/$persona_name"
    done < <(jq -r '.personas[].name' "$CONFIG_FILE")
}

# Verificar se os arquivos de configuração e estado existem
check_file "$CONFIG_FILE"
setup_directories
check_file "$STATE_FILE"

# Ler estado atual
ACTIVE_PERSONAS=$(jq -r '.active_personas' "$STATE_FILE")
LAST_REPORT=$(jq -r '.last_report' "$STATE_FILE")
REPORT_INTERVAL=$(jq -r '.report_interval' "$CONFIG_FILE")
CURRENT_TIME=$(date +%s)

# Calcular tempo desde o último relatório
TIME_SINCE_REPORT=$((CURRENT_TIME - LAST_REPORT))

# Verificar se a geração de relatórios é necessária
if [ "$TIME_SINCE_REPORT" -lt "$REPORT_INTERVAL" ]; then
    print_header "⏳ GERAÇÃO DE RELATÓRIOS NÃO NECESSÁRIA"
    echo "Tempo desde o último relatório: $TIME_SINCE_REPORT segundos."
    echo "Intervalo configurado: $REPORT_INTERVAL segundos."
    echo "Geração de relatórios não é necessária no momento."
    exit 0
fi

# Verificar se há personas ativas
if [ "$ACTIVE_PERSONAS" = "[]" ] || [ -z "$ACTIVE_PERSONAS" ]; then
    print_header "⚠️ NENHUMA PERSONA ATIVA"
    echo "Não há personas ativas para gerar relatórios."
    echo "Execute './scripts/rotate_personas.sh' para ativar novas personas."
    exit 0
fi

# Criar ou usar um modelo de relatório básico se o arquivo de template não existir
if [ ! -f "$TEMPLATE_FILE" ]; then
    cat <<EOT > "$TEMPLATE_FILE"
# Relatório de Progresso - {PERSONA_NAME}
**Data:** {DATE}

## Progresso Recente
- Ainda não atualizado.

## Próximos Passos
- Ainda não atualizado.

## Bloqueadores
- Ainda não atualizado.

## Notas
- Este é um relatório gerado automaticamente. Atualize os campos conforme necessário.
EOT
fi

# Obter a data atual para o nome do arquivo e conteúdo do relatório
CURRENT_DATE=$(date +%Y-%m-%d)
REPORT_COUNT=0

# Gerar relatório para cada persona ativa
while IFS= read -r persona_name; do
    # Remover aspas do nome da persona
    persona_name=$(echo "$persona_name" | tr -d '"')
    REPORT_FILE="$REPORTS_DIR/$persona_name/report_$CURRENT_DATE.md"
    
    # Verificar se o relatório já existe para evitar sobrescrever
    if [ -f "$REPORT_FILE" ]; then
        echo "Relatório para $persona_name já existe para a data $CURRENT_DATE. Pulando..."
    else
        # Substituir placeholders no template
        sed "s/{PERSONA_NAME}/$persona_name/g; s/{DATE}/$CURRENT_DATE/g" "$TEMPLATE_FILE" > "$REPORT_FILE"
        echo "Relatório gerado para $persona_name em $REPORT_FILE."
        ((REPORT_COUNT++))
    fi
done < <(echo "$ACTIVE_PERSONAS" | jq -r '.[]')

# Atualizar o estado com o timestamp do último relatório
NEW_STATE=$(jq -r ".last_report = $CURRENT_TIME" "$STATE_FILE")
echo "$NEW_STATE" > "$STATE_FILE"

# Exibir resultado da geração de relatórios
print_header "📝 RELATÓRIOS GERADOS"
echo "Número de relatórios gerados ou verificados: $REPORT_COUNT"
echo "Último relatório atualizado para: $(date -d "@$CURRENT_TIME")"
echo "Os relatórios estão disponíveis no diretório '$REPORTS_DIR'."
echo "Para atualizar campos específicos, use './scripts/update_report.sh <persona> <campo> <conteúdo>'."
echo "Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'."

# Fim do script
exit 0
