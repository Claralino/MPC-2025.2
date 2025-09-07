# Analisador de Comentários de PR (GitHub GraphQL)

Ferramenta em Python para coletar comentários dos 50 primeiros Pull Requests de um repositório no GitHub via API GraphQL, gerar um CSV estruturado e um PDF com estatísticas e respostas pedidas.

## Funcionalidades

- Coleta comentários de PRs de forma paginada via GraphQL
- Gera `pr_comments.csv` (seguro contra vírgulas e quebras de linha nos comentários)
- Calcula métricas como:

  - Total de comentários
  - Média de comentários por PR
  - Tamanho médio dos comentários (caracteres e palavras)
  - Quantos comentários contêm agradecimentos (e.g. thanks, obrigado, etc.)

- Gera report.pdf com todas as respostas organizadas

## Pré-requisitos

- Python 3.9+ instalado
- [GitHub Personal Access Token](https://github.com/settings/tokens) com permissão de leitura em repositórios públicos

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/Claralino/MPC-2025.2
   cd MPC-2025.2
   ```

2. Crie o arquivo .env a partir do exemplo:

   ```bash
   cp .env.example .env
   ```

3. Edite o arquivo .env e insira seu token:

   ```bash
   GITHUB_TOKEN=seu_token_aqui
   GROUP_NUMBER=XX
   PARTICIPANTS=Nome1; Nome2; Nome3
   ```

## Ambiente Virtual

1. Crie um ambiente virtual para isolar as dependências:

```bash
python -m venv .venv
```

2. Ative o ambiente virtual:

Linux/Mac:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```bash
venv\Scripts\Activate
```

## Dependências

Instale as dependências listadas em requirements.txt:

```bash
pip install -r requirements.txt
```

Se adicionar novas bibliotecas, salve-as no arquivo:

```bash
pip freeze > requirements.txt
```

## Como rodar

Execute o programa:

```bash
python -m src.main --owner TheAlgorithms --repo Python --limit 50 --outdir data/outputs
```

Saídas geradas:

- `data/outputs/pr_comments.csv`
- `data/outputs/report.pdf`

## Testes Unitários

Para executar os testes unitários, utilize:

```bash
pytest -v
```

## Notas

- Nunca comite o `.env` com o token real.
