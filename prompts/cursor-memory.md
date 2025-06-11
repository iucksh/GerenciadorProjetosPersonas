# Memória e Contexto para Personas no Cursor

Este documento define como o sistema de IA no Cursor mantém o contexto das interações com diferentes personas, permitindo conversas contínuas e coerentes.

## Princípios de Memória Contextual

### Identificação de Contexto

O sistema identificará automaticamente:
- Qual persona está sendo consultada
- Histórico de interações recentes com esta persona
- Arquivos relevantes para a consulta atual
- Contexto do projeto e requisitos relacionados

### Armazenamento de Memória

Para cada persona, o sistema mantém:

1. **Memória de Curto Prazo**:
   - Últimas 5-10 interações com a persona
   - Contexto das perguntas e respostas
   - Arquivos e código relevantes discutidos

2. **Memória de Longo Prazo**:
   - Decisões arquiteturais importantes
   - Padrões estabelecidos com a persona
   - Preferências do usuário identificadas

## Comandos de Contexto

### Referenciar Conversas Anteriores

Para referenciar uma conversa anterior com uma persona:

```
@Ana recall:[tópico ou data]: Como aplicar aquela otimização de PDAs que discutimos ontem?
```

### Definir Contexto Persistente

Para estabelecer um contexto que permanecerá em todas as conversas com uma persona:

```
@Ana context:set: Estamos trabalhando no módulo de staking com suporte para liquid staking e queremos otimizar para baixo custo de transação
```

### Limpar Contexto

Para reiniciar o contexto de uma persona:

```
@Ana context:clear
```

## Tags de Contexto Automático

Use tags específicas para ativar contextos automáticos:

- `#token-launch` - Ativa contexto de lançamento de tokens
- `#security-review` - Ativa contexto de revisão de segurança
- `#performance` - Ativa contexto de otimização de performance
- `#ui-design` - Ativa contexto de design de interface
- `#architecture` - Ativa contexto de decisões arquiteturais

Exemplo:
```
@Rafael #ui-design: Como podemos melhorar este componente de swap?
```

## Transição entre Personas

Para transferir contexto entre personas:

```
@Ana to @Pedro: Pode revisar esta implementação de pool sob perspectiva de segurança?
```

O sistema transferirá automaticamente o contexto relevante da conversa com Ana para Pedro.

## Implementação Técnica no Cursor

Para que este sistema funcione no Cursor, recomendamos:

1. **Adicionar Arquivos de Contexto**: Manter um arquivo de contexto para cada persona que é atualizado automaticamente
2. **Utilizar Custom Storage**: Usar a funcionalidade de armazenamento do Cursor para manter o histórico de interações
3. **Configurar Templates de Prompts**: Criar templates para diferentes tipos de interações com as personas

### Estrutura dos Arquivos de Contexto

```
/prompts/contexts/ana-context.md
/prompts/contexts/rafael-context.md
...
```

Cada arquivo de contexto deve conter:
- Interações recentes
- Decisões importantes
- Referências a código ou documentação
- Preferências e padrões estabelecidos 