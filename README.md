# Agente RAG com Google Gemini

Sistema de RAG (Retrieval-Augmented Generation) para análise de documentos PDF usando Agno framework, Google Gemini e LanceDB como vector store.

## Stack

- **Agno** - Framework de agentes
- **Google Gemini 2.5 Flash** - LLM + embeddings
- **LanceDB** - Vector database
- **Python 3.12+**

## Features

- Busca vetorial em documentos PDF
- Instruções customizadas para controle de comportamento do agente
- Logging estruturado com timestamps
- Error handling básico
- Output em Markdown

## Setup

Clone e instale as dependências:

```bash
git clone https://github.com/ErickGuimaraesFerreira/agent-rag-v2.git
cd agent-rag-v2

# Com UV
uv venv && source .venv/bin/activate
uv pip install -e .

# Ou com pip
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Configure a API key:

```bash
cp .env.example .env
# Adicione sua GOOGLE_API_KEY no arquivo .env
```

Obtenha a key em: https://ai.google.dev/

## Uso

Adicione seus PDFs em `knowledge/` e execute:

```bash
python code.py
```

O script indexa os documentos, processa as perguntas definidas no código e salva o resultado em `response_investimentos.md`.

### Customização

Edite as queries nas linhas 60-61 do `code.py`:

```python
response1 = agent.run("Sua pergunta aqui")
response2 = agent.run("Outra pergunta")
```

Ajuste as instruções do agente nas linhas 47-51:

```python
instructions=[
    "Responda de maneira concisa e direta.",
    "Se não souber a resposta, responda que não sabe.",
    "Não utilize informações que não estejam na base de conhecimento.",
],
```

## Estrutura

```
├── code.py              # Script principal
├── knowledge/           # PDFs para indexação
├── .env                 # API keys (não commitado)
├── pyproject.toml       # Dependências
└── README.md
```

## Implementação

O código segue uma estrutura simples:

1. **Configuração** - Logging e carregamento de env vars
2. **Vector DB** - Inicializa LanceDB com Gemini embeddings
3. **Knowledge Base** - Indexa PDFs do diretório `knowledge/`
4. **Agent** - Configura o agente com instructions e expected output
5. **Execução** - Processa queries e salva resultado

Principais componentes:

- `main()` - Entry point com error handling
- `logging` - Console output com timestamps
- `Agent.run()` - Executa queries com RAG
- Try/except - Captura erros durante execução

## Output

Exemplo de execução:

```
2026-02-10 22:00:00 | INFO     | Agente RAG iniciado...
2026-02-10 22:00:05 | INFO     | Base de conhecimento criada
2026-02-10 22:00:06 | INFO     | Agente criado
2026-02-10 22:00:15 | INFO     | Relatório salvo em response_investimentos.md
```

## Licença

MIT

---

**Erick Guimarães Ferreira** | [GitHub](https://github.com/ErickGuimaraesFerreira)
