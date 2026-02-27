from typing import List, Union, Optional
from agno.os import AgentOS
import os
import sys
import logging
import atexit

from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from config import settings
from agno.guardrails.prompt_injection import PromptInjectionGuardrail
from agno.guardrails.base import BaseGuardrail
from agno.run.agent import RunInput
from agno.run.team import TeamRunInput
from agno.exceptions import InputCheckError
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agente_rag")

########## Observabilidade (AgentOS)

db = SqliteDb(db_file="tmp/agno_telemetry.db")

########## Funçaõ da base de conhecimento


def setup_knowledge() -> Knowledge:
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

    ########## Guardrails ##########

    ########## Proteção contra Prompt Injection ##########

    def check(self, run_input: Union[RunInput, TeamRunInput]) -> None:

        if any(
            keyword in run_input.input_content_string().lower()
            for keyword in self.injection_patterns
        ):
            raise InputCheckError(
                "Potential jailbreaking or prompt injection detected.",
                check_trigger=CheckTrigger.PROMPT_INJECTION,
            )


# a########## Função principal

knowledge_base = setup_knowledge()

agent = Agent(
    name="Agente RAG Production Ready",
    description="Agente especializado em responder perguntas de acordo com sua base de conhecimento.",
    instructions=[
        "Não tenha pressa, faça uma busca minuciosa e detalhada.",
        "Responda de maneira concisa e direta.",
        "Se não souber a resposta, responda que não sabe.",
        "Não utilize informações que não estejam na base de conhecimento.",
        "Você deve buscar informações em tudo que estiver na sua base de conhecimento.",
        "Para garantir uma busca ampla, utilize a ferramenta de busca múltiplas vezes com diferentes palavras-chaves antes de responder, se você não tiver certeza de que cobriu todos os PDFs sobre o assunto.",
    ],
    expected_output="Resposta estruturada em markdown com as páginas de referência.",
    model=Gemini(id=settings.model_id, api_key=settings.google_api_key),
    pre_hooks=[
        PromptInjectionGuardrail(injection_patterns=settings.injection_patterns)
    ],
    knowledge=knowledge_base,
    search_knowledge=True,
    markdown=True,
)

agent_os = AgentOS(
    name="Agente RAG Production Ready",
    description="Agente especializado em responder perguntas de acordo com sua base de conhecimento.",
    agents=[agent],
    tracing=True,
    db=db,
)

app = agent_os.get_app()


def main():
    if len(sys.argv) < 2:
        print('Uso: python code_agno_telemetry.py "Sua pergunta aqui" [--serve]')
        sys.exit(1)

    question = " ".join(arg for arg in sys.argv[1:] if arg != "--serve").strip()

    if question:
        try:
            logger.info(f"Pergunta: {question}")
            response = agent.run(question)
            agent.print_response(response.content)
        except Exception as e:
            logger.error(f"Erro durante execução: {e}")

    if "--serve" in sys.argv or not question:
        logger.info("Iniciando o servidor AgentOS UI...")
        agent_os.serve(
            app="code_agno_telemetry:app", host="0.0.0.0", port=7777, reload=True
        )


if __name__ == "__main__":
    main()
