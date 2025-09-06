# MCP-2025.2

Script em Python para coletar comentários de Pull Requests de um repositório no GitHub via API GraphQL e exportar para CSV.

---

## Pré-requisitos

- Python 3.9+ instalado
- [GitHub Personal Access Token](https://github.com/settings/tokens) com permissão de leitura em repositórios públicos

---

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
   ```

## Ambiente Virtual

Crie e ative um ambiente virtual para isolar as dependências:

Linux/Mac

Windows (PowerShell)

```bash
python -m venv venv
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

Após configurar tudo:

```bash
python main.py
```

O script vai gerar um arquivo:

```bash
pr_comments.csv
```

## Notas

- Não comite seu .env com o token.
