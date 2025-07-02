# Guia de Uso - Gerenciador de Projetos e Personas

Este guia fornece instruções práticas sobre como utilizar o **Gerenciador de Projetos e Personas** para coordenar o desenvolvimento de projetos e gerenciar personas de forma eficiente. O sistema foi projetado para ajudar equipes a manterem o foco no progresso do projeto, garantindo que todas as perspectivas sejam consideradas por meio de um sistema estruturado de personas.

## Introdução

O **Gerenciador de Projetos e Personas** é uma ferramenta que combina automação e organização para facilitar o desenvolvimento de projetos completos. Ele permite:
- Definir e gerenciar personas com papéis e prioridades específicas.
- Automatizar a rotação de personas para garantir envolvimento equilibrado.
- Gerar relatórios de progresso para cada persona.
- Rastrear tarefas e monitorar o status geral do projeto.

Este guia cobre os passos básicos para começar a usar o sistema. Funcionalidades mais avançadas serão adicionadas à medida que o projeto evoluir.

## Passo 0: Instalação Rápida e CLI

Instale o projeto em modo editável – isto disponibiliza o comando `gpp`:

```bash
python -m pip install -e .
```

Verifique a instalação:
```bash
gpp --help
```

### Subcomando `ai`
Para utilizar recursos de IA (Gemini), instale o Gemini CLI:
```bash
npm install -g @google/gemini-cli
```
Depois:
```bash
gpp ai "Resuma o roadmap" -f docs/ROADMAP_TAREFAS.md
```

---

## Passo 1: Configuração Inicial

Antes de usar o sistema, certifique-se de que ele está configurado corretamente. Siga o guia de instalação em `INSTALACAO.md` para preparar o ambiente. Os passos principais incluem:
- Clonar ou baixar os arquivos do projeto.
- Configurar as personas no arquivo `scripts/personas/config.json`.

## Passo 2: Definindo Personas

As personas representam diferentes papéis ou áreas de especialização dentro do projeto. Para configurar as personas do seu projeto:

1. Abra o arquivo `scripts/personas/config.json` em um editor de texto.
2. Modifique a lista de personas, adicionando ou removendo entradas conforme necessário. Cada persona deve ter:
   - **name**: Nome da persona (ex.: "João").
   - **role**: Papel ou função (ex.: "Desenvolvedor Backend").
   - **priority**: Prioridade (P0 para crítico, P1 para importante, P2 para desejável).
   - **description**: Breve descrição das responsabilidades.
3. Ajuste os intervalos de rotação (`rotation_interval`) e geração de relatórios (`report_interval`) em segundos, se necessário.
4. Salve o arquivo.

Exemplo de entrada no `config.json`:
```json
{
  "name": "João",
  "role": "Desenvolvedor Backend",
  "priority": "P1",
  "description": "Responsável pela lógica do servidor e integrações com banco de dados."
}
```

## Passo 3: Iniciando o Monitoramento

Uma vez que as personas estão configuradas, você pode iniciar o sistema de monitoramento para gerenciar a rotação e relatórios:

1. Execute o script de monitoramento:
   ```bash
   python scripts/monitor.py
   ```
   Este script verifica o status atual do sistema, identifica quais personas estão ativas e sinaliza se é necessário alternar personas ou gerar relatórios.

2. Verifique a saída do script para entender o estado do projeto:
   - Personas ativas no momento.
   - Progresso geral do projeto (quando implementado).
   - Necessidade de rotação ou atualização de relatórios.

## Passo 4: Rotação de Personas

A rotação de personas garante que diferentes perspectivas sejam consideradas regularmente. Você pode executar o script de rotação manualmente ou configurá-lo para rodar automaticamente:

1. Execute o script de rotação:
   ```bash
   python scripts/rotate_personas.py
   ```
2. O sistema selecionará novas personas com base nas prioridades e no intervalo configurado, garantindo que todas sejam envolvidas ao longo do tempo.

## Passo 5: Gerando e Atualizando Relatórios

Relatórios de progresso ajudam a rastrear o que cada persona está fazendo. Siga estes passos:

1. Gere relatórios para todas as personas ativas:
   ```bash
   python scripts/generate_report.py
   ```
   Isso criará arquivos de relatório no diretório `scripts/reports/` para cada persona, com base em um modelo padrão.

2. Atualize campos específicos de um relatório manualmente, se necessário:
   ```bash
   python scripts/update_report.py <nome_persona> <campo> "<conteúdo>"
   ```
   Exemplo:
   ```bash
   python scripts/update_report.py João progress "Implementei a API de autenticação hoje."
   ```
   Campos disponíveis incluem `progress`, `next_steps`, `blockers` e `notes`.

## Passo 6: Gerenciamento de Tarefas e Projetos

O sistema agora inclui uma ferramenta de gerenciamento de tarefas que permite criar, listar, atualizar e editar tarefas para o projeto. Siga estas instruções para usar a ferramenta:

1. **Adicionar uma Nova Tarefa**:
   Execute o script `task_manager.py` com o comando `add` para criar uma nova tarefa:
   ```bash
   python scripts/task_manager.py add "Implementar login de usuário" P0 "João"
   ```
   - Substitua `"Implementar login de usuário"` pela descrição da tarefa.
   - Use `P0`, `P1` ou `P2` para definir a prioridade (P0 é a mais alta).
   - Substitua `"João"` pelo nome da persona responsável (deve estar listada em `config.json`).

2. **Listar Tarefas**:
   Liste todas as tarefas ou aplique filtros para visualizar apenas as relevantes:
   ```bash
   python scripts/task_manager.py list
   ```
   Use filtros opcionais para refinar a lista:
   ```bash
   python scripts/task_manager.py list --status "Pendente" --priority "P0" --assignee "João"
   ```

3. **Atualizar Status de uma Tarefa**:
   Atualize o status de uma tarefa existente para "Pendente", "Em Progresso" ou "Concluída":
   ```bash
   python scripts/task_manager.py update 1 "Em Progresso"
   ```
   - Substitua `1` pelo ID da tarefa.
   - Use um dos status válidos: `Pendente`, `Em Progresso`, `Concluída`.

4. **Editar uma Tarefa**:
   Edite a descrição, prioridade ou responsável de uma tarefa existente:
   ```bash
   python scripts/task_manager.py edit 1 --description "Implementar autenticação OAuth" --priority "P1" --assignee "Maria"
   ```
   - Substitua `1` pelo ID da tarefa.
   - Use os argumentos opcionais `--description`, `--priority` ou `--assignee` para atualizar os campos desejados.

As tarefas são armazenadas em `scripts/tasks/tasks.json` e podem ser revisadas a qualquer momento usando o comando `list`. Esta ferramenta ajuda a monitorar o progresso geral e as tarefas pendentes, alinhando-se com as prioridades definidas no roadmap (`ROADMAP_TAREFAS.md`).
>>>>>>> REPLACE

## Passo 7: Personalização e Expansão

O sistema é projetado para ser flexível. Você pode:
- Adicionar novas personas ou ajustar prioridades conforme o projeto cresce.
- Modificar intervalos de rotação e relatórios no `config.json`.
- Criar modelos personalizados para relatórios ou checklists no diretório `templates/` (a ser criado).

## Resolução de Problemas

- **Personas não aparecem corretamente**: Verifique se o arquivo `config.json` está formatado corretamente como JSON válido.
- **Scripts não executam**: Certifique-se de que o ambiente Python está corretamente configurado e que os arquivos estão acessíveis.
- **Relatórios não são gerados**: Confirme que o diretório `scripts/reports/` existe e tem permissões de escrita.

## Próximos Passos

À medida que o sistema evolui, mais funcionalidades serão adicionadas, como automação avançada, integração com Git e notificações. Consulte regularmente a documentação atualizada e o roadmap em `ROADMAP_TAREFAS.md` para acompanhar o progresso.

Este guia será expandido com exemplos práticos e instruções mais detalhadas nas próximas versões do projeto.
