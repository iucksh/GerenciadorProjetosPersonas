# Guia de Contexto para Uso do Sistema de Personas no Desenvolvimento

Este guia fornece instruções sobre como utilizar o **Sistema de Personas** do Gerenciador de Projetos e Personas para orientar o desenvolvimento contínuo de projetos, incluindo o próprio sistema. Ele é projetado para garantir que o progresso seja feito de forma autônoma, com base nas perspectivas de diferentes papéis (personas), e que as atualizações sejam devidamente registradas.

## Objetivo do Sistema de Personas no Desenvolvimento

O sistema de personas foi criado para simular a colaboração de uma equipe diversificada, onde cada persona representa uma área de especialização ou responsabilidade dentro de um projeto. Ao usar este sistema para o desenvolvimento (incluindo o auto-desenvolvimento do próprio Gerenciador), o objetivo é:
- Garantir que múltiplas perspectivas sejam consideradas em cada etapa do desenvolvimento.
- Priorizar tarefas e decisões com base nas prioridades definidas para cada persona (P0, P1, P2).
- Manter um registro claro do progresso e dos desafios enfrentados por cada "membro da equipe" simulado.
- Permitir um fluxo de trabalho estruturado e autônomo, onde o sistema guia a si mesmo por meio de rotação de personas e relatórios.

## Passo 1: Entendendo as Personas Configuradas

As personas estão definidas no arquivo `scripts/personas/config.json`. Cada persona possui:
- **Nome**: Identificador único da persona.
- **Papel**: Função ou área de especialização (ex.: Gerente de Produto, Desenvolvedor Backend).
- **Prioridade**: Nível de importância (P0 para crítico, P1 para importante, P2 para desejável).
- **Descrição**: Resumo das responsabilidades.

Para o desenvolvimento do próprio Gerenciador de Projetos e Personas, as personas padrão incluem papéis como Gerente de Produto, Desenvolvedor de Software, Especialista em Automação, entre outros. Certifique-se de revisar este arquivo para entender quais papéis estão disponíveis e suas prioridades.

## Passo 2: Iniciando o Monitoramento para Orientação

Antes de começar qualquer sessão de desenvolvimento, execute o script de monitoramento para verificar o estado atual do sistema e quais personas estão ativas:

```bash
python scripts/monitor.py
```

A saída deste script indicará:
- Quais personas estão ativas no momento.
- Se é necessário realizar uma rotação de personas.
- Se relatórios de progresso precisam ser gerados.

Siga as instruções da saída para ativar novas personas ou atualizar relatórios, se necessário.

## Passo 3: Rotação de Personas para Perspectivas Diversas

Se o script de monitoramento indicar a necessidade de rotação, execute:

```bash
python scripts/rotate_personas.py
```

Isso garantirá que novas personas sejam ativadas, trazendo diferentes perspectivas para o desenvolvimento. Por exemplo:
- Uma persona de Gerente de Produto (P0) pode focar na priorização de tarefas e no roadmap.
- Uma persona de Desenvolvedor (P1) pode implementar funcionalidades específicas.
- Uma persona de QA (P2) pode revisar o código ou scripts para garantir qualidade.

Adote a mentalidade das personas ativas ao trabalhar nas tarefas. Por exemplo, se uma persona de automação estiver ativa, concentre-se em criar ou melhorar scripts de automação.

## Passo 4: Desenvolvimento com Base nas Personas Ativas

Com base nas personas ativas, siga estas diretrizes para o desenvolvimento autônomo:

1. **Consultar o Roadmap**: Verifique o arquivo `ROADMAP_TAREFAS.md` para identificar as próximas tarefas prioritárias (P0 primeiro, depois P1 e P2).
2. **Selecionar Tarefas Relevantes**: Escolha tarefas que se alinhem com as especialidades das personas ativas. Por exemplo, uma persona de Gerente de Produto pode atualizar a documentação ou o roadmap, enquanto uma persona de Desenvolvedor implementa novos scripts.
3. **Implementar e Documentar**: Realize as tarefas selecionadas, criando ou atualizando arquivos conforme necessário. Documente o progresso usando o sistema de relatórios (veja Passo 5).
4. **Priorizar Qualidade**: Certifique-se de que o trabalho segue as melhores práticas da área de especialização da persona ativa.

## Passo 5: Atualizando Relatórios de Progresso

Após completar uma tarefa ou periodicamente (conforme indicado pelo script de monitoramento), atualize os relatórios de progresso para cada persona ativa. Execute:

```bash
python scripts/generate_report.py
```

Isso gerará relatórios no diretório `scripts/reports/` para cada persona ativa, se ainda não existirem para a data atual. Em seguida, atualize campos específicos com detalhes do progresso:

```bash
python scripts/update_report.py <nome_persona> <campo> "<conteúdo>"
```

Exemplo:
```bash
python scripts/update_report.py Ana progress "Implementei o script de gerenciamento de tarefas hoje."
```

Campos disponíveis:
- **progress**: Progresso recente feito pela persona.
- **next_steps**: Próximos passos planejados.
- **blockers**: Desafios ou bloqueadores enfrentados.
- **notes**: Observações adicionais.

## Passo 6: Iteração Contínua

Repita os passos 2 a 5 em ciclos regulares (por exemplo, a cada 15-20 minutos ou após completar uma tarefa significativa):
- Verifique o status com `monitor.py`.
- Rotacione personas com `rotate_personas.py`, se necessário.
- Desenvolva com base nas personas ativas.
- Atualize relatórios com `generate_report.py` e `update_report.py`.

Esse ciclo garante que o desenvolvimento avance de forma estruturada, considerando múltiplas perspectivas e mantendo um registro claro do progresso.

## Passo 7: Atualizando a Documentação e o Roadmap

Periodicamente, com uma persona de liderança (como Gerente de Produto) ativa, revise e atualize a documentação e o roadmap:
- Adicione novas tarefas ao `ROADMAP_TAREFAS.md` conforme necessário.
- Atualize guias como `USO.md` ou `FLUXOS.md` para refletir novas funcionalidades ou mudanças nos scripts.

## Considerações para Desenvolvimento Autônomo

- **Priorização**: Sempre foque em tarefas P0 antes de P1 e P2, a menos que uma persona específica só possa trabalhar em tarefas de menor prioridade.
- **Flexibilidade**: Adapte os fluxos de trabalho conforme necessário, mas mantenha a estrutura de rotação e relatórios para garantir consistência.
- **Auto-Melhoria**: Use o sistema para melhorar o próprio Gerenciador, implementando novas funcionalidades (como ferramentas de tarefas ou notificações) conforme descrito no roadmap.

## Resolução de Problemas

- **Personas não rotacionam corretamente**: Verifique se o arquivo `config.json` está corretamente formatado e se o intervalo de rotação (`rotation_interval`) é razoável.
- **Relatórios não são gerados**: Confirme que o diretório `scripts/reports/` tem permissões de escrita e que há personas ativas.
- **Erros nos scripts**: Certifique-se de que o ambiente Python está configurado corretamente (consulte `INSTALACAO.md`).

## Conclusão

Este guia fornece o contexto necessário para usar o Sistema de Personas de forma autônoma no desenvolvimento de projetos, incluindo o próprio Gerenciador de Projetos e Personas. Ao seguir os passos descritos, você garantirá que o progresso seja feito de maneira estruturada, com múltiplas perspectivas consideradas e um registro claro de cada etapa. Consulte regularmente o roadmap e os relatórios de progresso para manter o foco nas prioridades do projeto.
