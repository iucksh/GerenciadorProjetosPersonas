# Gerenciador de Projetos e Personas

Bem-vindo ao **Gerenciador de Projetos e Personas**, um sistema projetado para auxiliar no desenvolvimento de projetos completos e funcionais, com um foco especial no gerenciamento de personas. Este projeto visa fornecer uma estrutura organizada para coordenação de equipes, documentação de progresso e automação de tarefas, garantindo que todas as perspectivas sejam consideradas durante o ciclo de vida do desenvolvimento.

## Objetivo

O objetivo principal deste sistema é criar um framework que:
- Facilite o desenvolvimento de projetos desde a concepção até a conclusão.
- Gerencie múltiplas personas, cada uma com papéis e responsabilidades específicas, para garantir uma abordagem colaborativa.
- Automatize processos como rotação de personas, geração de relatórios e monitoramento de progresso.
- Forneça documentação clara e acessível para orientar os membros da equipe.

## Estrutura do Projeto

O projeto está organizado nas seguintes pastas principais:

- **docs/**: Contém toda a documentação relevante, incluindo guias de uso, estrutura de personas e fluxos de trabalho.
- **scripts/**: Scripts de automação para gerenciamento de personas, relatórios e outras tarefas repetitivas.
- **templates/**: Modelos para relatórios, checklists e outros documentos úteis.
- **examples/**: Exemplos de projetos ou configurações que podem ser usados como referência.

## Instalação Rápida

```bash
# 1. Clone o repositório
$ git clone <url-do-projeto> && cd GerenciadorProjetosPersonas

# 2. Instale em modo editável (gera o comando `gpp`)
$ python -m pip install -e .

# 3. (Opcional) Instale o Gemini CLI para usar o subcomando de IA
$ npm install -g @google/gemini-cli

# 4. (Windows) Certifique-se de que a pasta Python Scripts está no PATH
# Exemplo:
setx PATH "%PATH%;%USERPROFILE%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Scripts"
```

### Verificando
```bash
$ gpp --help   # deve exibir a ajuda do CLI
```

## Uso Rápido do CLI `gpp`

| Comando              | Descrição |
|----------------------|-----------|
| `gpp monitor`        | Executa `monitor.py` e mostra status. |
| `gpp rotate`         | Rotaciona personas se necessário (use `--force` para forçar). |
| `gpp report`         | Gera relatórios de progresso. |
| `gpp ai "<prompt>"` | Envia prompt ao Gemini CLI. Use `-f <arquivo>` para incluir contexto (`@file`). |

Exemplo:
```bash
# Resumir o roadmap com IA
gpp ai "Resuma em 5 bullets" -f docs/ROADMAP_TAREFAS.md
```

---

## Próximos Passos

1. **Configuração Inicial**: Consulte o guia de instalação em `docs/INSTALACAO.md` para configurar o ambiente.
2. **Definição de Personas**: Edite a configuração de personas em `scripts/personas/config.json` para adaptar às necessidades do seu projeto.
3. **Automação**: Utilize os scripts em `scripts/` para iniciar o monitoramento e a rotação de personas.

Este projeto está em desenvolvimento inicial e será expandido com mais funcionalidades e documentação detalhada nas próximas etapas.
