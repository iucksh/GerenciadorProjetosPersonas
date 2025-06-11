#!/bin/bash

# Script de Atualização de Relatórios - Gerenciador de Projetos e Personas
# Este script atualiza campos específicos nos relatórios de progresso de uma persona,
# permitindo adicionar informações sobre progresso, próximos passos, bloqueadores e notas.

# Definir o diretório base do projeto
BASE_DIR="$(dirname "$(dirname "$0")")"
CONFIG_FILE="$BASE_DIR/scripts/personas/config.json"
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
    mkdir -p "$REPORTS_DIR"
    # Criar subdiretórios para cada persona
    while IFS= read -r persona_name; do
        mkdir -p "$REPORTS_DIR/$persona_name"
    done < <(jq -r '.personas[].name' "$CONFIG_FILE")
}

# Verificar se o arquivo de configuração existe
check_file "$CONFIG_FILE"
setup_directories

# Verificar parâmetros de entrada
if [ $# -lt 3 ]; then
    print_header "❌ ERRO DE USO"
    echo "Uso: $0 <nome_persona> <campo> \"<conteúdo>\""
    echo "Campos disponíveis: progress, next_steps, blockers, notes"
    echo "Exemplo: $0 João progress \"Implementei a API de autenticação hoje.\""
    exit 1
fi

PERSONA_NAME="$1"
FIELD="$2"
CONTENT="$3"

# Verificar se a persona existe no arquivo de configuração
PERSONA_EXISTS=$(jq -r ".personas[] | select(.name == \"$PERSONA_NAME\")" "$CONFIG_FILE")
if [ -z "$PERSONA_EXISTS" ]; then
    print_header "❌ PERSONA NÃO ENCONTRADA"
    echo "A persona '$PERSONA_NAME' não foi encontrada no arquivo de configuração."
    echo "Verifique o arquivo 'scripts/personas/config.json' e tente novamente."
    exit 1
fi

# Verificar se o campo é válido
case "$FIELD" in
    progress|next_steps|blockers|notes)
        ;;
    *)
        print_header "❌ CAMPO INVÁLIDO"
        echo "Campo '$FIELD' não é válido. Campos disponíveis: progress, next_steps, blockers, notes"
        exit 1
        ;;
esac

# Obter a data atual para encontrar o relatório mais recente
CURRENT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="$REPORTS_DIR/$PERSONA_NAME/report_$CURRENT_DATE.md"

# Verificar se o relatório existe; se não, criar um básico
if [ ! -f "$REPORT_FILE" ]; then
    echo "Relatório para $PERSONA_NAME não encontrado para $CURRENT_DATE. Criando um novo..."
    cat <<EOT > "$REPORT_FILE"
# Relatório de Progresso - $PERSONA_NAME
**Data:** $CURRENT_DATE

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

# Mapear o campo para o título correspondente no relatório
case "$FIELD" in
    progress)
        SECTION="Progresso Recente"
        ;;
    next_steps)
        SECTION="Próximos Passos"
        ;;
    blockers)
        SECTION="Bloqueadores"
        ;;
    notes)
        SECTION="Notas"
        ;;
esac

# Ler o conteúdo atual do relatório
REPORT_CONTENT=$(cat "$REPORT_FILE")

# Verificar se a seção existe no relatório
if ! echo "$REPORT_CONTENT" | grep -q "## $SECTION"; then
    echo "Seção '$SECTION' não encontrada no relatório. Adicionando..."
    echo -e "\n## $SECTION\n- Ainda não atualizado." >> "$REPORT_FILE"
    REPORT_CONTENT=$(cat "$REPORT_FILE")
fi

# Atualizar o campo no relatório
# Primeiro, remover o conteúdo antigo da seção (entre "## $SECTION" e a próxima seção ou fim do arquivo)
NEW_CONTENT=$(echo "$REPORT_CONTENT" | sed -e "/## $SECTION/,/## /{ /## $SECTION/!d; /## $SECTION/a\\
- $CONTENT
}" -e "/## $SECTION/,/## /!b" -e "/## $SECTION/a\\
- $CONTENT
" -e "/## $SECTION/,/## /d")

# Se não houver próxima seção, adicionar o conteúdo no final da seção
if echo "$NEW_CONTENT" | grep -q "## $SECTION"; then
    echo "$NEW_CONTENT" > "$REPORT_FILE"
else
    echo "$REPORT_CONTENT" | sed -e "/## $SECTION/a\\
- $CONTENT
" > "$REPORT_FILE"
fi

# Exibir resultado da atualização
print_header "✅ RELATÓRIO ATUALIZADO"
echo "Campo '$FIELD' atualizado para a persona '$PERSONA_NAME'."
echo "Relatório: $REPORT_FILE"
echo "Conteúdo adicionado: - $CONTENT"
echo "Para mais detalhes, consulte os fluxos de trabalho em 'docs/FLUXOS.md'."

# Fim do script
exit 0
