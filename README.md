# 🤖 Agente RAG com Google Gemini

Agente de IA para análise automatizada de documentos PDF usando RAG (Retrieval-Augmented Generation).

## 🚀 Funcionalidades

- **RAG**: Busca vetorial com LanceDB + Google Gemini embeddings
- **Instruções Customizadas**: Agente configurado com papel, tom e formato de resposta definidos
- **Logging Estruturado**: Rastreamento completo da execução
- **Tratamento de Erros**: Error handling com try/except

## 📦 Stack

- **Framework**: [Agno](https://github.com/agno-agi/agno)
- **LLM**: Google Gemini 2.5 Flash
- **Vector DB**: LanceDB
- **Embeddings**: Google Gemini Embeddings

## 🛠️ Instalação

### Pré-requisitos

- Python 3.12+
- Google API Key ([obter aqui](https://ai.google.dev/))

### Setup

1. Clone o repositório:
```bash
<<<<<<< HEAD
git clone https://github.com/ErickGuimaraesFerreira/agent-rag-v2
cd agno-rag-1
=======
git clone https://github.com/ErickGuimaraesFerreira/agent-rag-v2.git
cd agent-rag-v2
>>>>>>> 2236f4b (atualização Readme)
```

2. Crie ambiente virtual e instale dependências:
```bash
# Com UV (recomendado)
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
uv pip install -e .

# OU com pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY
```

4. Adicione seus PDFs no diretório `knowledge/`

## 🎯 Uso

```bash
python code.py
```

O agente irá:
1. Indexar os PDFs do diretório `knowledge/`
2. Processar as perguntas definidas no código
3. Gerar um relatório em `response_investimentos.md`

### Personalizando as Perguntas

Edite as linhas 60-61 do `code.py` para fazer suas próprias perguntas:

```python
response1 = agent.run("Sua pergunta aqui")
response2 = agent.run("Outra pergunta")
```

## 📁 Estrutura do Projeto

```
agent-rag-v2/
├── code.py              # Script principal
├── knowledge/           # PDFs para indexação
├── .env                 # Variáveis de ambiente (não commitado)
├── .env.example         # Template de .env
├── pyproject.toml       # Dependências
└── README.md
```

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

## 📊 Exemplo de Output

```
2026-02-10 22:00:00 | INFO     | Agente RAG iniciado...
2026-02-10 22:00:05 | INFO     | Base de conhecimento criada
2026-02-10 22:00:06 | INFO     | Agente criado
2026-02-10 22:00:15 | INFO     | Relatório salvo em response_investimentos.md
```

## 🔧 Features Técnicas

- **Função `main()`**: Código estruturado com entry point adequado
- **Logging**: Timestamps e níveis de log profissionais
- **Agent Instructions**: Lista de regras de comportamento
- **Expected Output**: Formato de resposta definido
- **Error Handling**: Try/except para captura de erros

## 📝 Licença

MIT

## 👤 Autor

**Erick Guimarães Ferreira**

- GitHub: [@ErickGuimaraesFerreira](https://github.com/ErickGuimaraesFerreira)

---

⭐ Se este projeto foi útil, dê uma estrela!
