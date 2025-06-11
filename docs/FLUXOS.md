# Definição de Fluxos de Trabalho - Gerenciador de Projetos e Personas

Este documento descreve os fluxos de trabalho recomendados para utilizar o **Gerenciador de Projetos e Personas** no desenvolvimento de projetos completos e no gerenciamento de personas. Esses fluxos são projetados para maximizar a eficiência, garantir colaboração entre diferentes papéis e manter o progresso do projeto bem documentado e rastreável.

## Objetivo dos Fluxos de Trabalho

Os fluxos de trabalho aqui definidos têm como objetivo:
- Estabelecer processos claros para o ciclo de vida de um projeto, desde a concepção até a conclusão.
- Garantir que todas as personas sejam envolvidas de forma equilibrada e regular por meio de rotação automatizada.
- Facilitar a geração de relatórios de progresso para manter todos os envolvidos atualizados.
- Permitir o rastreamento de tarefas e a priorização de atividades críticas.

## Fluxo 1: Início de um Novo Projeto

Este fluxo descreve como iniciar um novo projeto usando o sistema.

1. **Definição de Objetivos e Escopo**:
   - Reúna os stakeholders (ou personas simuladas) para definir os objetivos do projeto, entregáveis principais e cronograma.
   - Documente essas informações em um arquivo de visão geral do projeto (pode ser criado manualmente ou usando um modelo futuro em `templates/`).

2. **Configuração de Personas**:
   - Edite o arquivo `scripts/personas/config.json` para incluir todas as personas relevantes para o projeto, definindo seus papéis, prioridades (P0, P1, P2) e descrições.
   - Ajuste os intervalos de rotação e relatórios conforme necessário (ex.: rotação a cada 15 minutos, relatórios a cada 30 minutos).

3. **Planejamento Inicial de Tarefas**:
   - Crie uma lista de tarefas iniciais com prioridades claras (P0 para crítico, P1 para importante, P2 para desejável).
   - Atribua responsáveis (personas) para cada tarefa, garantindo que as prioridades correspondam às das personas.
   - Documente isso em um checklist priorizado (futuro modelo em `templates/checklist.md` ou manualmente por enquanto).

4. **Iniciar Monitoramento**:
   - Execute o script de monitoramento (quando disponível) para começar a rastrear personas ativas e progresso:
     ```bash
     ./scripts/monitor.sh
     ```
   - Isso garantirá que o sistema esteja ativo e pronto para gerenciar rotação e relatórios.

## Fluxo 2: Ciclo Diário de Trabalho com Personas

Este fluxo descreve como gerenciar o trabalho diário com rotação de personas.

1. **Verificação Inicial do Dia**:
   - No início de cada sessão de trabalho, execute o script de monitoramento para verificar quais personas estão ativas e o status do projeto:
     ```bash
     ./scripts/monitor.sh
     ```
   - Analise a saída para entender quais personas estão trabalhando e se há necessidade de rotação ou relatórios.

2. **Adoção da Perspectiva das Personas Ativas**:
   - Adote a mentalidade das personas ativas (ex.: se uma persona de frontend está ativa, foque em tarefas de interface).
   - Consulte os relatórios mais recentes de cada persona ativa (futuro diretório `scripts/reports/`) para entender o contexto atual do trabalho.

3. **Execução de Tarefas**:
   - Trabalhe nas tarefas atribuídas às personas ativas, priorizando as de maior importância (P0 primeiro).
   - Documente o progresso manualmente ou por meio de atualizações de relatórios (quando o script estiver disponível):
     ```bash
     ./scripts/update_report.sh <nome_persona> progress "<descrição do progresso>"
     ```

4. **Rotação de Personas**:
   - Se o sistema indicar a necessidade de rotação (ou após o intervalo configurado), execute o script de rotação (futuro):
     ```bash
     ./scripts/rotate_personas.sh
     ```
   - Alternativamente, o sistema pode ser configurado para rotacionar automaticamente em intervalos regulares.

5. **Verificações Periódicas**:
   - A cada 15-20 minutos, ou conforme necessário, execute novamente o script de monitoramento para atualizar o status:
     ```bash
     ./scripts/monitor.sh
     ```
   - Isso ajuda a manter o foco nas prioridades e ajustar o trabalho conforme novas personas são ativadas.

## Fluxo 3: Geração e Revisão de Relatórios de Progresso

Este fluxo garante que o progresso seja documentado e revisado regularmente.

1. **Verificação de Necessidade de Relatórios**:
   - Durante a execução do script de monitoramento, verifique se há indicação de que relatórios precisam ser gerados para certas personas.
   - Isso geralmente ocorre a cada 30 minutos (ou conforme configurado no `report_interval`).

2. **Geração de Relatórios**:
   - Execute o script de geração de relatórios (quando disponível) para criar relatórios atualizados para todas as personas ativas:
     ```bash
     ./scripts/generate_report.sh
     ```
   - Os relatórios serão salvos no diretório `scripts/reports/` com base em um modelo padrão.

3. **Atualização Manual de Relatórios**:
   - Se precisar atualizar campos específicos (progresso, próximos passos, bloqueadores, notas), use o script de atualização (futuro):
     ```bash
     ./scripts/update_report.sh <nome_persona> <campo> "<conteúdo>"
     ```
     Exemplo:
     ```bash
     ./scripts/update_report.sh Maria next_steps "Planejo implementar o login na próxima sessão."
     ```

4. **Revisão de Relatórios**:
   - Periodicamente, revise os relatórios gerados para garantir que todas as personas estejam alinhadas com os objetivos do projeto.
   - Use essas informações para ajustar prioridades ou reatribuir tarefas, se necessário.

## Fluxo 4: Gerenciamento de Tarefas e Priorização

Este fluxo descreve como gerenciar tarefas usando a ferramenta de gerenciamento de tarefas integrada ao sistema. Ele ajuda a adicionar, rastrear e priorizar tarefas para garantir que o projeto avance de forma organizada.

1. **Adição de Novas Tarefas**:
   - Adicione novas tarefas ao projeto usando o script `task_manager.py` com o comando `add`:
     ```bash
     python scripts/task_manager.py add "Implementar login de usuário" P0 "João"
     ```
     - Substitua `"Implementar login de usuário"` pela descrição da tarefa.
     - Use `P0`, `P1` ou `P2` para definir a prioridade (P0 é a mais alta).
     - Substitua `"João"` pelo nome da persona responsável (deve estar listada em `config.json`).
   - Certifique-se de alinhar a prioridade da tarefa com a prioridade da persona responsável, quando possível.

2. **Rastreamento de Progresso**:
   - Liste todas as tarefas ou aplique filtros para monitorar o progresso geral e tarefas pendentes:
     ```bash
     python scripts/task_manager.py list
     ```
     Use filtros para focar em tarefas específicas:
     ```bash
     python scripts/task_manager.py list --status "Pendente" --priority "P0"
     ```
   - Atualize o status de tarefas à medida que o trabalho avança:
     ```bash
     python scripts/task_manager.py update 1 "Em Progresso"
     ```
     - Substitua `1` pelo ID da tarefa e use um status válido (`Pendente`, `Em Progresso`, `Concluída`).

3. **Re-priorização e Edição**:
   - Periodicamente, revise as prioridades das tarefas com base no progresso e nas necessidades do projeto:
     ```bash
     python scripts/task_manager.py list --status "Pendente"
     ```
   - Ajuste prioridades ou responsáveis conforme necessário:
     ```bash
     python scripts/task_manager.py edit 1 --priority "P1" --assignee "Maria"
     ```
     - Substitua `1` pelo ID da tarefa e atualize os campos desejados.
   - Garanta que tarefas críticas (P0) sejam tratadas por personas de alta prioridade, reatribuindo se necessário.
>>>>>>> REPLACE

## Fluxo 5: Conclusão de uma Sessão de Trabalho

Este fluxo descreve como finalizar uma sessão de trabalho de forma organizada.

1. **Atualização Final de Relatórios**:
   - Antes de encerrar a sessão, execute o script de geração de relatórios para garantir que todo o progresso seja documentado:
     ```bash
     ./scripts/generate_report.sh
     ```
   - Verifique se não há atualizações pendentes para as personas ativas.

2. **Verificação de Status do Projeto**:
   - Execute o script de monitoramento uma última vez para revisar o status atual:
     ```bash
     ./scripts/monitor.sh
     ```
   - Anote quaisquer tarefas ou questões pendentes para a próxima sessão.

3. **Planejamento da Próxima Sessão**:
   - Com base nos relatórios e no status, defina as prioridades para a próxima sessão de trabalho.
   - Documente isso manualmente ou em um futuro sistema de planejamento.

## Considerações Importantes

- **Flexibilidade**: Os fluxos de trabalho são recomendações e podem ser adaptados às necessidades específicas do seu projeto.
- **Automação**: À medida que os scripts de automação forem implementados, muitos desses passos serão simplificados ou executados automaticamente.
- **Colaboração**: Mantenha uma persona de liderança (como um Gerente de Produto) sempre informada sobre decisões importantes, mesmo durante rotações.

## Próximos Passos

Este documento será atualizado com mais detalhes à medida que novas ferramentas e scripts forem desenvolvidos. Consulte o roadmap em `ROADMAP_TAREFAS.md` para acompanhar o progresso na implementação de funcionalidades que suportam esses fluxos de trabalho.
