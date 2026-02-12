from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder
from dotenv import load_dotenv
import logging
import os
import sys

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agente_rag")
logger.info("Agente RAG iniciado...")


def setup_knowledge() -> Knowledge:

    vector_db = LanceDb(
        table_name=settings.table_name,
        uri=settings.lancedb_uri,
        embedder=GeminiEmbedder(api_key=settings.google_api_key),
    )

    knowledge_base = Knowledge(vector_db=vector_db)

    pdf_files = list(settings.knowledge_dir.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"Nenhum PDF encontrado em {settings.knowledge_dir}")
        return knowledge_base

    logger.info(f"Encontrados {len(pdf_files)} documentos. Iniciando indexação...")

    for pdf in pdf_files:
        try:
            knowledge_base.insert(path=str(pdf), skip_if_exists=True)
            logger.info(f"Processado o {pdf.name}")
        except Exception as e:
            logger.error(f"Erro ao processar {pdf.name}: {e}")
    return knowledge_base


def main():
    """
    Executa todo o pipeline do agente RAG, carregando documentos, criando base de conhecimento, criando agente e respondendo perguntas.
    """

    try:

        knowledge_base = setup_knowledge()

        agent = Agent(
            name="Agente MVP Rag",
            description="Agente especializado em responder as perguntas de maneira concisa de acordo com sua base de conhecimento.",
            instructions=[
                "Responda de maneira concisa e direta.",
                "Se não souber a resposta, responda que não sabe.",
                "Não utilize informações que não estejam na base de conhecimento.",
            ],
            expected_output="Resposta estruturada em markdown e especifique as páginas de onde você encontrou a informação.",
            model=Gemini(id=settings.model_id, api_key=settings.google_api_key),
            knowledge=knowledge_base,
            search_knowledge=True,
            markdown=True,
        )
        logger.info("Agente criado")

        response1 = agent.run("Quais os principais players do mercado de IA?")
        response2 = agent.run("Como esse players estão se posicionando no mercado?")

        response = response1.content + response2.content
        agent.print_response(response)

        with open("response_investimentos.md", "w") as f:
            f.write(response)
        logger.info("Relatório salvo em response_investimentos.md")

    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
