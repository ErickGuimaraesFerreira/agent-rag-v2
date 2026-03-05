from typing import List, Union, Optional
from agno.os import AgentOS
import os
import sys
import logging
import atexit

from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from config import settings
from agno.guardrails.prompt_injection import PromptInjectionGuardrail
from agno.guardrails.base import BaseGuardrail
from agno.run.agent import RunInput
from agno.run.team import TeamRunInput
from agno.exceptions import InputCheckError
from knowledge import setup_knowledge
from security import protection_guardrail
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

# a########## Função principal

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
    pre_hooks=[protection_guardrail],
    knowledge=setup_knowledge(),
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
