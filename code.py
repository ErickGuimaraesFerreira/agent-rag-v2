from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder
from dotenv import load_dotenv
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agente_rag")
logger.info("Agente RAG iniciado...")


def main():
    """
    Executa todo o pipeline do agente RAG, carregando documentos, criando base de conhecimento, criando agente e respondendo perguntas.
    """

    try:
        load_dotenv()
        api = os.getenv("GOOGLE_API_KEY")

        if not api:
            logger.error("GOOGLE_API_KEY não encontrada")
            sys.exit(1)

        vector_db = LanceDb(
            table_name="pdfs_local",
            uri="lancedb_data",
            embedder=GeminiEmbedder(api_key=api),
        )

        knowledge_base = Knowledge(vector_db=vector_db)

        knowledge_base.insert(path="knowledge/IA-Report_2025.pdf")
        logger.info("Base de conhecimento criada")

        agent = Agent(
            name="Agente MVP Rag",
            description="Agente especializado em responder as perguntas de maneira concisa de acordo com sua base de conhecimento.",
            instructions=[
                "Responda de maneira concisa e direta.",
                "Se não souber a resposta, responda que não sabe.",
                "Não utilize informações que não estejam na base de conhecimento.",
            ],
            expected_output="Resposta estruturada em markdown e especifique as páginas de onde você encontrou a informação.",
            model=Gemini(id="gemini-2.5-flash", api_key=api),
            knowledge=knowledge_base,
            search_knowledge=True,
            markdown=True,
        )
        logger.info("Agente criado")

        response1 = agent.run(
            "Quais os valores de investimento em IA ao longo dos anos?"
        )
        response2 = agent.run("Quais os principais setores que mais investem em IA?")

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
