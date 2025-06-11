# Integração do Router de IA com Cursor

Este guia explica como integrar o sistema de personas especialistas com o Cursor para uso diário no projeto.

## Configuração no Cursor

Para melhor uso das personas no Cursor, recomendamos as seguintes práticas:

### 1. Adicionar as Personas como Contexto

No Cursor, quando trabalhar com arquivos relevantes, adicione as personas relevantes como contexto:

1. Selecione a função "Add File as Context" no Cursor
2. Adicione os arquivos de personas relevantes para o contexto atual
   - Para trabalho em smart contracts: `prompts/personas/01-ana-blockchain-architect.md`
   - Para trabalho em frontend: `prompts/personas/02-rafael-frontend-expert.md`
   - E assim por diante...

### 2. Usar o Custom Command do Cursor

Crie um custom command no Cursor para facilitar o acesso ao roteador:

1. Vá para Configurações > Custom Commands
2. Adicione um novo comando chamado "Consultar Especialista"
3. Use o template: `@{persona}: {query}` 

## Fluxo de Trabalho Diário

### Consulta Explícita

Quando precisar de ajuda especializada e souber qual persona consultar:

```
@Ana: Como posso otimizar o custo de gas neste contrato Solana?
```

### Consulta Implícita

Quando quiser que o sistema decida qual especialista deve responder:

```
Como podemos melhorar a performance desta função que busca dados do RPC node?
```

## Comandos Especiais

### Consulta Multi-Especialista

Para problemas complexos que exigem múltiplas perspectivas:

```
@multi [Ana, Pedro]: Como implementar uma função de swap segura e otimizada?
```

### Consulta com Contexto de Arquivo

Para análise de código específico:

```
@Ana file:app/services/MeteoraService.ts: Revise este serviço para identificar otimizações possíveis.
```

### Consulta em Modo Projeto

Para questões estratégicas de alto nível:

```
@projeto: Qual a melhor abordagem para implementar o módulo de staking considerando nosso roadmap atual?
```

## Dicas para Obter Melhores Respostas

1. **Seja específico**: Quanto mais detalhada sua pergunta, melhor será a resposta
2. **Forneça contexto**: Inclua informações relevantes sobre o problema
3. **Indique restrições**: Mencione limitações técnicas ou de negócio
4. **Especifique o formato**: Se precisar de código, diagrama ou explicação conceitual
5. **Use a persona certa**: Escolha a persona com a expertise mais relevante para o problema

## Exemplos de Prompts Eficazes

### Para Ana (Blockchain)
```
@Ana: Revise esta implementação de pool de liquidez concentrada. Estou preocupado com a eficiência do armazenamento de estado e possíveis race conditions durante o swap.
```

### Para Lucia (Backend)
```
@Lucia: Nossa API de preços está lenta sob carga. Estamos fazendo 200 requisições/segundo para o RPC node. Como podemos implementar um sistema de cache eficiente?
```

### Para Pedro (Segurança)
```
@Pedro: Implementamos este fluxo de aprovação de transações. Pode identificar possíveis vetores de ataque e sugerir mitigações?
``` 