# Agente RAG com Google Gemini

Sistema de RAG (Retrieval-Augmented Generation) para análise de documentos PDF usando Agno framework, Google Gemini e LanceDB como vector store.

```
        @@@@@@@@@@@@@@@@                                                                            
        @##############@                                                                            
         @@@@@@@@@@@####@                                                                           
                    @####@              @@@@####@@@#@        #@@@@@@@@@#               @@@@@@
                     @####@           @@@######@@@@###@   @###@@@########@@        @@@########@@@
                      @####@        @@###@@@ @@@######@   @###@#@@@ @@@####@     @####@@@ @@@@###@
                       @####@      @####@        @####@   @####@       @####    @###@@        @###@ 
                        @####@     @###@          ####@   @###@        @####@  @####@          @###@
                        @#####@    ####@          @###@   @###@        @####@  @###@           @####
                         @#####@   @###@          ####@   @###@        @####@  @####@          @###@
                          @#####@  @####@        @####@   @###@        @####@   @###@         @####@
@@@@@@@@@@@@@@@            @####@   @####@@@@@@@##@###@   @###@        @####@    @###@@     @@###@@ 
@##############             @####@    @@#######@@ @###@   @####        @####@     @@@##########@@   
@@@@@@@@@@@@@@@              @@@@@@      @@@@@    ####@   @@@@@         @@@@         @@@@@@@@@      
                                   @@@@@@        @####@
                                    @@###@@@@@@@####@
                                       @@@@####@@@@

```
## Stack

- **Agno** - Framework de agentes
- **Google Gemini 2.5 Flash** - LLM + embeddings
- **LanceDB** - Vector database
- **Pydantic Settings** - Gerenciamento de configurações
- **Python 3.12+**

## Features

- Busca vetorial em documentos PDF
- Instruções customizadas para controle de comportamento do agente
- Logging estruturado com timestamps
- Error handling robusto com `try/except` granular
- Output em Markdown

### Novas Features (v2)

- **Módulo de configuração centralizado (`config.py`)** — Todas as configurações do projeto (API keys, model ID, diretórios, nomes de tabela) são gerenciadas via `Pydantic BaseSettings`, permitindo fácil customização via variáveis de ambiente ou `.env`
- **Indexação automática de múltiplos PDFs** — O sistema agora escaneia automaticamente o diretório `knowledge/` e indexa todos os PDFs encontrados, com `skip_if_exists=True` para evitar reprocessamento
- **Função `setup_knowledge()` dedicada** — A lógica de criação da knowledge base foi extraída para uma função própria com type hints, melhorando a modularidade e testabilidade do código
- **Error handling por documento** — Erros durante a indexação de PDFs individuais são capturados e logados sem interromper o processamento dos demais documentos
- **Configurações externalizadas** — Model ID, diretório de knowledge, URI do LanceDB e nome da tabela são configuráveis sem alterar o código-fonte
- **Base de conhecimento expandida** — Novos documentos PDF adicionados à knowledge base para consultas mais abrangentes

## Base de Conhecimento

Documentos PDF indexados pelo agente (**4 documentos, 2.347 páginas no total**):

| Documento | Páginas |
|-----------|---------|
| `CanalSysAuto2.pdf` | 240 |
| `IA-Report-2025.pdf` | 457 |
| `Inteligência Artificial (Peter Norvig, Stuart Russell).pdf` | 1.324 |
| `Manual-de-Inteligencia-Artificial.pdf` | 326 |

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

O script indexa automaticamente todos os documentos PDF do diretório, processa as perguntas definidas no código e salva o resultado em `response_investimentos.md`.

### Customização

Edite as queries no `code.py`:

```python
response1 = agent.run("Sua pergunta aqui")
response2 = agent.run("Outra pergunta")
```

Ajuste as configurações no `.env` ou diretamente no `config.py`:

```python
# config.py - valores padrão
model_id: str = "gemini-2.5-flash"
knowledge_dir: Path = Path("knowledge")
lancedb_uri: str = "lancedb_data"
table_name: str = "pdfs_local"
```

Ajuste as instruções do agente no `code.py`:

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
├── config.py            # Configurações centralizadas (Pydantic Settings)
├── knowledge/           # PDFs para indexação (auto-descoberta)
├── .env                 # API keys (não commitado)
├── pyproject.toml       # Dependências
└── README.md
```

## Implementação

O código segue uma arquitetura modular:

1. **Configuração (`config.py`)** — Pydantic BaseSettings carrega variáveis do `.env` com valores padrão
2. **Setup Knowledge** — Função dedicada que inicializa LanceDB, escaneia PDFs e indexa com error handling individual
3. **Agent** — Configura o agente com instructions, expected output e knowledge base
4. **Execução (`main()`)** — Entry point com error handling e `sys.exit(1)` em caso de falha

Principais componentes:

- `Settings` (Pydantic) — Validação e carregamento de configurações
- `setup_knowledge()` — Inicializa vector DB e indexa PDFs
- `main()` — Entry point com error handling
- `logging` — Console output com timestamps
- `Agent.run()` — Executa queries com RAG

## Output

Exemplo de execução:

```
2026-02-11 22:00:00 | INFO | Agente RAG iniciado...
2026-02-11 22:00:02 | INFO | Encontrados 4 documentos. Iniciando indexação...
2026-02-11 22:00:05 | INFO | Processado o IA-Report-2025.pdf
2026-02-11 22:00:08 | INFO | Processado o Manual-de-Inteligencia-Artificial.pdf
2026-02-11 22:00:10 | INFO | Agente criado
2026-02-11 22:00:15 | INFO | Relatório salvo em response_investimentos.md
```

## Licença

MIT

---

**Erick Guimarães Ferreira** | [GitHub](https://github.com/ErickGuimaraesFerreira)
