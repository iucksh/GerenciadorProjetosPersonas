# Guia de Instalação - Gerenciador de Projetos e Personas

Este documento fornece instruções passo a passo para configurar o ambiente do **Gerenciador de Projetos e Personas**, permitindo que você comece a utilizar o sistema para desenvolver projetos completos e gerenciar personas de forma eficiente.

## Pré-requisitos

Antes de iniciar a instalação, certifique-se de que você tem os seguintes itens instalados no seu sistema:

- **Git**: Para controle de versão e clonagem do repositório.
- **Python 3.x**: Necessário para executar os scripts de automação do sistema.
- **Editor de Texto ou IDE**: Como VSCode, para edição de arquivos de configuração e scripts.

## Passos para Instalação

### 1. Clonar o Repositório

Se este projeto estiver hospedado em um repositório Git, clone-o para o seu ambiente local usando o comando abaixo:

```bash
git clone <URL_DO_REPOSITORIO>
cd GerenciadorProjetosPersonas
```

Caso contrário, certifique-se de que os arquivos do projeto estão em um diretório acessível no seu sistema.

### 2. Configurar o Ambiente

Por enquanto, não há dependências externas específicas a serem instaladas. Futuras atualizações podem incluir a necessidade de pacotes ou ferramentas adicionais. Verifique esta seção regularmente para atualizações.

### 3. Estrutura de Diretórios

Familiarize-se com a estrutura do projeto para entender onde encontrar os arquivos necessários:

- **docs/**: Documentação, incluindo este guia.
- **scripts/**: Scripts de automação para gerenciamento de personas e tarefas.
- **templates/**: Modelos para relatórios e outros documentos.
- **examples/**: Exemplos práticos de uso do sistema.

### 4. Configuração Inicial de Personas

Para adaptar o sistema às necessidades do seu projeto, edite o arquivo de configuração de personas:

1. Abra o arquivo `scripts/personas/config.json` em um editor de texto.
2. Adicione ou modifique as personas conforme necessário, definindo seus nomes, papéis e prioridades (P0, P1, P2).
3. Salve as alterações.

Um exemplo de configuração será fornecido na documentação futura ou no próprio arquivo de exemplo.

### 5. Testar a Instalação

Para verificar se o sistema está configurado corretamente, execute o script de monitoramento:

```bash
python scripts/monitor.py
```

Este comando exibirá o status atual do sistema, incluindo personas ativas e necessidades de relatórios.

## Resolução de Problemas

- **Permissões de Arquivo**: Se os scripts Python não executarem, verifique se o ambiente Python está corretamente configurado e se os arquivos estão acessíveis.
- **Dependências Faltantes**: Caso futuras atualizações exijam pacotes específicos, instale-os conforme indicado nesta documentação.

## Próximos Passos

Após a instalação, consulte os seguintes documentos para continuar:

- **Guia de Uso**: Em `docs/USO.md` (a ser criado), para aprender como gerenciar personas e projetos.
- **Definição de Fluxos de Trabalho**: Em `docs/FLUXOS.md` (a ser criado), para entender os processos recomendados.

Este guia será expandido com mais detalhes à medida que o projeto evolui. Mantenha-se atualizado com as mudanças no repositório.
