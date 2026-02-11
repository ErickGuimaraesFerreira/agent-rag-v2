# 🤖 Agente RAG Empresarial

Agente de IA com RAG (Retrieval-Augmented Generation) para análise automatizada de documentos PDF corporativos, gerando relatórios estruturados com insights estratégicos.

## 🚀 Features

- **RAG Avançado**: Busca vetorial com LanceDB + Google Gemini embeddings
- **Instruções Customizadas**: Agente configurado com papel, tom e output definidos
- **Logging Estruturado**: Rastreabilidade completa com logs em console e arquivo
- **Error Handling**: Tratamento robusto de erros com fallbacks
- **Relatórios Profissionais**: Geração automática de análises em Markdown

## 📦 Stack

- **Framework**: [Agno](https://github.com/agno-agi/agno)
- **LLM**: Google Gemini 2.5 Flash
- **Vector DB**: LanceDB
- **Embeddings**: Google Gemini Embeddings

## 🛠️ Instalação

### Pré-requisitos

- Python 3.12+
- UV package manager (ou pip)

### Setup

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USERNAME/agno-rag-1.git
cd agno-rag-1
```

2. Crie ambiente virtual e instale dependências:
```bash
# Com UV (recomendado)
uv venv
source .venv/bin/activate  # Linux/Mac
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

### Versão Básica (`code.py`)
```bash
python code.py
```

Features:
- Logging estruturado
- Instruções customizadas do agente
- Error handling com try/except
- Relatório salvo em `response_investimentos.md`

### Versão Enterprise (`code_v2.py`)
```bash
python code_v2.py
```

Features adicionais:
- Configuração centralizada com dataclass
- Carregamento dinâmico de todos os PDFs
- Reasoning habilitado (2-8 steps)
- Retries com exponential backoff
- Relatórios com metadata e disclaimers
- Logs salvos em `logs/agent.log`

## 📁 Estrutura do Projeto

```
agno-rag-1/
├── code.py              # Versão MVP com melhorias
├── code_v2.py           # Versão enterprise completa
├── knowledge/           # PDFs para indexação
├── .env                 # Variáveis de ambiente (não commitar)
├── pyproject.toml       # Dependências
└── README.md
```

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

Para obter uma chave: https://ai.google.dev/

## 📊 Exemplo de Output

O agente responde perguntas sobre os documentos analisados:
- Resumos executivos
- Tendências de investimento
- Análise de setores
- Tecnologias emergentes
- Recomendações estratégicas

Resultados salvos em:
- `response_investimentos.md` (versão básica)
- `reports/relatorio_analise_YYYY-MM-DD.md` (versão enterprise)

## 🧪 Desenvolvimento

### Estrutura do Código

**`code.py`** — MVP aprimorado para portfólio:
- Função `main()` com entry point
- Logging básico mas profissional
- Agent instructions + expected output
- Try/except para resiliência

**`code_v2.py`** — Versão production-ready:
- Config dataclass com validação
- Setup de logging modular
- Múltiplas perguntas de análise
- Geração de relatórios corporativos

## 📝 Licença

MIT

## 👤 Autor

**Erick Guimarães Ferreira**

- GitHub: [@ErickGuimaraesFerreira](https://github.com/ErickGuimaraesFerreira)
- LinkedIn: [Seu LinkedIn]

---

⭐ Se este projeto foi útil, dê uma estrela!
