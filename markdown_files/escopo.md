from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb

# 1. Configura o Banco de Dados Vetorial local (salva na pasta 'lancedb_data')
vector_db = LanceDb(
    table_name="docs_local",
    uri="lancedb_data",
)

# 2. Cria a base de conhecimento a partir de uma pasta com PDFs
knowledge_base = PDFKnowledgeBase(
    path="meus_pdfs/", # Pasta onde estão seus arquivos
    vector_db=vector_db
)

# Carrega os documentos (faz o embedding e salva no LanceDB)
knowledge_base.load(recreate=True)

# 3. Cria o Agente
agent = Agent(
    name="Assistente PDF",
    knowledge=knowledge_base,
    search_knowledge=True,
    markdown=True
)

agent.print_response("Qual o resumo dos documentos?")