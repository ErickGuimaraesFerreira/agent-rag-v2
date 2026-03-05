from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder
from config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agente_rag")


def setup_knowledge():
    vector_db = LanceDb(
        table_name=settings.table_name,
        uri=settings.lancedb_uri,
        embedder=GeminiEmbedder(api_key=settings.google_api_key),
    )

    knowledge_base = Knowledge(
        vector_db=vector_db,
        max_results=30,
    )

    pdf_files = list(settings.knowledge_dir.glob("*.pdf"))

    # Carrega documentos PDF existentes na pasta de conhecimento
    for pdf in settings.knowledge_dir.glob("*.pdf"):
        knowledge_base.add_content(path=str(pdf), skip_if_exists=True)

    if not pdf_files:
        logger.warning(f"Nenhum PDF encontrado em {settings.knowledge_dir}")
        return knowledge_base

    logger.info(f"Encontrados {len(pdf_files)} documentos. Iniciando indexação...")
    for pdf in pdf_files:
        try:
            knowledge_base.add_content(path=str(pdf), skip_if_exists=True)
            logger.info(f"Processado: {pdf.name}")
        except Exception as e:
            logger.error(f"Erro ao processar {pdf.name}: {e}")

    return knowledge_base
