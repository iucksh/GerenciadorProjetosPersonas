# Guia Rápido - Sistema de Personas no Cursor

Este guia oferece instruções práticas para começar a usar o sistema de personas especializadas no Cursor imediatamente.

## Início Rápido

### 1. Consulta Direta a uma Persona

Para obter ajuda de um especialista específico, use a sintaxe:

```
@[Nome da Persona]: [Sua pergunta ou solicitação]
```

Exemplo:
```
@Ana: Como otimizar o armazenamento de estado neste contrato Solana?
```

### 2. Deixar a IA Escolher o Especialista

Para permitir que o sistema roteie sua pergunta para o especialista mais adequado:

```
[Sua pergunta ou solicitação]
```

O sistema analisará o contexto e encaminhará para a persona apropriada.

## Personas Disponíveis

| Prefixo | Especialista | Área de Atuação |
|---------|--------------|-----------------|
| `@Ana` | Ana Silva | Arquitetura blockchain Solana |
| `@Rafael` | Rafael Oliveira | Frontend Web3 e UX |
| `@Lucia` | Lucia Santos | Backend e APIs |
| `@Pedro` | Pedro Costa | Segurança Web3 |
| `@Carla` | Carla Mendes | Gestão de Produto DeFi |
| `@Gustavo` | Gustavo Ferreira | Tokenomics e incentivos |
| `@Marina` | Marina Alves | Compliance e regulação |
| `@Luiz` | Luiz Pereira | DevOps e infraestrutura |

## Comandos Avançados

### Consulta Multi-especialista
```
@multi [Ana, Pedro]: Como implementar pools com segurança?
```

### Consulta com Contexto de Arquivo
```
@Ana file:app/services/MeteoraService.ts: Otimize este código.
```

### Definir Contexto Persistente
```
@Ana context:set: Estamos trabalhando no módulo de staking
```

### Consulta com Tag de Contexto
```
@Rafael #ui-design: Melhore este componente de swap
```

## Dicas para Resultados Melhores

1. **Seja específico**: "Como implementar staking com bloqueio de 30 dias?" é melhor que "Como fazer staking?"

2. **Forneça contexto**: Mencione restrições, objetivos e detalhes relevantes

3. **Use a persona certa**: Escolha o especialista mais adequado para o problema específico

4. **Combine especialistas**: Para problemas complexos, use `@multi` para obter múltiplas perspectivas

5. **Dialogue continuamente**: Mantenha uma conversa com a mesma persona para desenvolver ideias

## Exemplo de Fluxo de Trabalho

1. **Questão inicial**:
   ```
   @Gustavo: Quais parâmetros econômicos considerar para nosso modelo de staking?
   ```

2. **Exploração técnica**:
   ```
   @Ana: Como implementar tecnicamente o modelo de staking sugerido pelo Gustavo?
   ```

3. **Implementação frontend**:
   ```
   @Rafael: Como criar uma UI intuitiva para este sistema de staking?
   ```

4. **Revisão de segurança**:
   ```
   @Pedro: Revise a implementação técnica da Ana para este sistema de staking.
   ```

5. **Integração final**:
   ```
   @multi [Ana, Rafael, Pedro]: Vamos revisitar o sistema completo e garantir que está coeso.
   ``` 