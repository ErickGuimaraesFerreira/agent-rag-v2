"""
================================================================================
 AGENTE RAG EMPRESARIAL — v2.0
 Análise Inteligente de Documentos Corporativos
================================================================================

 Descrição:
   Agente de IA com RAG (Retrieval-Augmented Generation) para análise
   automatizada de documentos PDF corporativos. Gera relatórios estruturados
   com insights estratégicos.

 Stack: Agno Framework + Google Gemini + LanceDB
 Autor: Equipe de IA
 Data: 2026-02-10
================================================================================
"""

import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from agno.agent import Agent
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.vectordb.lancedb import LanceDb
from dotenv import load_dotenv

# ============================================================================
#  CONFIGURAÇÃO CENTRALIZADA
# ============================================================================

load_dotenv()


@dataclass
class Config:
    """Configuração centralizada do agente empresarial."""

    # --- API ---
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))

    # --- Modelo ---
    model_id: str = "gemini-2.5-flash"

    # --- Knowledge Base ---
    knowledge_dir: str = "knowledge"
    lancedb_uri: str = "lancedb_data"
    lancedb_table: str = "docs_empresarial_v2"

    # --- Agente ---
    agent_name: str = "Analista Corporativo IA"
    max_search_results: int = 15

    # --- Output ---
    reports_dir: str = "reports"
    logs_dir: str = "logs"
    log_level: int = logging.INFO

    # --- Perguntas de Análise ---
    analysis_questions: List[str] = field(
        default_factory=lambda: [
            "Faça um resumo executivo dos documentos analisados, destacando os pontos mais relevantes para tomada de decisão estratégica.",
            "Quais são os valores de investimento em IA ao longo dos anos? Apresente uma análise de tendência com os dados disponíveis.",
            "Quais os principais setores que mais investem em IA? Identifique oportunidades e riscos para cada setor.",
            "Quais são as principais tecnologias emergentes mencionadas nos documentos? Como elas podem impactar o mercado nos próximos 2-3 anos?",
            "Com base nos dados analisados, quais recomendações estratégicas você faria para uma empresa que deseja investir em IA?",
        ]
    )

    def validate(self) -> None:
        """Valida as configurações obrigatórias."""
        if not self.google_api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY não encontrada. Configure no arquivo .env"
            )

        knowledge_path = Path(self.knowledge_dir)
        if not knowledge_path.exists():
            raise FileNotFoundError(
                f"Diretório de conhecimento não encontrado: {self.knowledge_dir}"
            )

        pdf_files = list(knowledge_path.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(
                f"Nenhum arquivo PDF encontrado em: {self.knowledge_dir}"
            )


# ============================================================================
#  LOGGING ESTRUTURADO
# ============================================================================


def setup_logging(config: Config) -> logging.Logger:
    """Configura logging estruturado com output no console e em arquivo."""

    logs_path = Path(config.logs_dir)
    logs_path.mkdir(exist_ok=True)

    logger = logging.getLogger("agente_empresarial")
    logger.setLevel(config.log_level)

    # Evita duplicação de handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_file = logs_path / "agent.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# ============================================================================
#  BASE DE CONHECIMENTO
# ============================================================================


def create_knowledge_base(config: Config, logger: logging.Logger) -> Knowledge:
    """
    Cria e popula a base de conhecimento com todos os PDFs do diretório.
    Usa skip_if_exists para evitar re-processamento desnecessário.
    """
    logger.info("Inicializando base de conhecimento vetorial...")

    vector_db = LanceDb(
        table_name=config.lancedb_table,
        uri=config.lancedb_uri,
        embedder=GeminiEmbedder(api_key=config.google_api_key),
    )

    knowledge_base = Knowledge(
        vector_db=vector_db,
        max_results=config.max_search_results,
    )

    # Carrega todos os PDFs dinamicamente
    knowledge_path = Path(config.knowledge_dir)
    pdf_files = sorted(knowledge_path.glob("*.pdf"))

    logger.info(f"Encontrados {len(pdf_files)} arquivo(s) PDF para indexação")

    for pdf_file in pdf_files:
        logger.info(f"  📄 Indexando: {pdf_file.name}")
        try:
            knowledge_base.insert(
                path=str(pdf_file),
                skip_if_exists=True,
            )
            logger.info(f"  ✅ Indexado com sucesso: {pdf_file.name}")
        except Exception as e:
            logger.warning(f"  ⚠️  Erro ao indexar {pdf_file.name}: {e}")

    logger.info("Base de conhecimento pronta")
    return knowledge_base


# ============================================================================
#  AGENTE EMPRESARIAL
# ============================================================================

AGENT_INSTRUCTIONS = [
    "Você é um analista corporativo sênior especializado em inteligência artificial e tecnologia.",
    "Sempre responda em português brasileiro (pt-BR) com linguagem profissional e objetiva.",
    "Estruture suas respostas com títulos, subtítulos e bullet points quando apropriado.",
    "Cite dados numéricos e estatísticas sempre que disponíveis nos documentos.",
    "Ao apresentar análises, separe em: Contexto, Dados Relevantes, Análise e Conclusão.",
    "Se não encontrar informações suficientes, indique claramente e sugira fontes alternativas.",
    "Mantenha um tom executivo adequado para apresentações em reuniões de diretoria.",
    "Priorize insights acionáveis que possam guiar decisões estratégicas.",
    "Não invente dados — baseie-se exclusivamente no conteúdo dos documentos fornecidos.",
]

AGENT_DESCRIPTION = (
    "Analista Corporativo de IA — Especialista em análise de documentos "
    "estratégicos, geração de insights e recomendações para tomada de decisão "
    "empresarial. Utiliza RAG (Retrieval-Augmented Generation) para fornecer "
    "respostas precisas e embasadas nos documentos da empresa."
)

EXPECTED_OUTPUT = (
    "Relatório estruturado em Markdown com análise profissional, dados "
    "quantitativos quando disponíveis, e recomendações estratégicas claras."
)


def create_agent(
    config: Config, knowledge_base: Knowledge, logger: logging.Logger
) -> Agent:
    """Cria o agente empresarial com configurações de produção."""

    logger.info(f"Configurando agente: {config.agent_name}")
    logger.info(f"Modelo: {config.model_id}")

    agent = Agent(
        name=config.agent_name,
        model=Gemini(id=config.model_id, api_key=config.google_api_key),
        knowledge=knowledge_base,
        # --- RAG ---
        search_knowledge=True,
        add_search_knowledge_instructions=True,
        # --- Instruções Corporativas ---
        description=AGENT_DESCRIPTION,
        instructions=AGENT_INSTRUCTIONS,
        expected_output=EXPECTED_OUTPUT,
        # --- Reasoning ---
        reasoning=True,
        reasoning_min_steps=2,
        reasoning_max_steps=8,
        # --- Contexto ---
        add_datetime_to_context=True,
        markdown=True,
        # --- Resiliência ---
        retries=2,
        delay_between_retries=3,
        exponential_backoff=True,
    )

    logger.info("Agente configurado com sucesso")
    return agent


# ============================================================================
#  EXECUÇÃO DA ANÁLISE
# ============================================================================


def run_analysis(
    agent: Agent,
    questions: List[str],
    logger: logging.Logger,
) -> List[dict]:
    """
    Executa uma lista de perguntas de análise e coleta as respostas.
    Retorna lista de dicts com pergunta, resposta e status.
    """
    results = []

    logger.info(f"Iniciando análise com {len(questions)} pergunta(s)...")
    logger.info("=" * 60)

    for i, question in enumerate(questions, 1):
        logger.info(f"[{i}/{len(questions)}] Processando: {question[:80]}...")

        try:
            response = agent.run(question)
            content = response.content if response and response.content else ""

            results.append(
                {
                    "numero": i,
                    "pergunta": question,
                    "resposta": content,
                    "status": "sucesso",
                }
            )

            logger.info(
                f"[{i}/{len(questions)}] ✅ Resposta obtida ({len(content)} caracteres)"
            )

        except Exception as e:
            logger.error(f"[{i}/{len(questions)}] ❌ Erro: {e}")
            results.append(
                {
                    "numero": i,
                    "pergunta": question,
                    "resposta": f"*Erro ao processar esta pergunta: {e}*",
                    "status": "erro",
                }
            )

    success_count = sum(1 for r in results if r["status"] == "sucesso")
    logger.info("=" * 60)
    logger.info(
        f"Análise concluída: {success_count}/{len(questions)} perguntas processadas com sucesso"
    )

    return results


# ============================================================================
#  GERAÇÃO DE RELATÓRIO
# ============================================================================


def generate_report(
    results: List[dict],
    config: Config,
    logger: logging.Logger,
) -> str:
    """Gera relatório Markdown profissional com cabeçalho corporativo."""

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    datetime_str = now.strftime("%d/%m/%Y às %H:%M")

    # Monta o relatório
    report_lines = [
        f"# 📊 Relatório de Análise — Inteligência Artificial",
        "",
        "---",
        "",
        "| Campo | Detalhe |",
        "| --- | --- |",
        f"| **Data de Geração** | {datetime_str} |",
        f"| **Modelo Utilizado** | `{config.model_id}` |",
        f"| **Agente** | {config.agent_name} |",
        f"| **Documentos Analisados** | Diretório `{config.knowledge_dir}/` |",
        f"| **Total de Perguntas** | {len(results)} |",
        f"| **Processadas com Sucesso** | {sum(1 for r in results if r['status'] == 'sucesso')} |",
        "",
        "---",
        "",
    ]

    # Adiciona cada seção de análise
    for result in results:
        status_icon = "✅" if result["status"] == "sucesso" else "❌"
        report_lines.extend(
            [
                f"## {status_icon} {result['numero']}. {result['pergunta']}",
                "",
                result["resposta"],
                "",
                "---",
                "",
            ]
        )

    # Rodapé corporativo
    report_lines.extend(
        [
            "## 📋 Notas e Disclaimers",
            "",
            "> **Aviso**: Este relatório foi gerado automaticamente por um sistema de IA "
            "com base nos documentos fornecidos. As análises e recomendações devem ser "
            "validadas por especialistas antes de serem utilizadas para tomada de decisão.",
            ">",
            "> As informações contidas neste documento são confidenciais e de uso interno. "
            "A reprodução ou distribuição sem autorização prévia é proibida.",
            "",
            "---",
            "",
            f"*Gerado automaticamente em {datetime_str} por {config.agent_name} v2.0*",
        ]
    )

    report_content = "\n".join(report_lines)

    # Salva o relatório
    reports_path = Path(config.reports_dir)
    reports_path.mkdir(exist_ok=True)

    report_filename = f"relatorio_analise_{date_str}.md"
    report_filepath = reports_path / report_filename

    with open(report_filepath, "w", encoding="utf-8") as f:
        f.write(report_content)

    logger.info(f"📄 Relatório salvo em: {report_filepath}")

    return str(report_filepath)


# ============================================================================
#  ENTRY POINT
# ============================================================================


def main() -> None:
    """Ponto de entrada principal do agente empresarial."""

    # 1. Configuração
    config = Config()

    # 2. Logging
    logger = setup_logging(config)
    logger.info("=" * 60)
    logger.info(f"🚀 Iniciando {config.agent_name} v2.0")
    logger.info("=" * 60)

    try:
        # 3. Validação
        config.validate()
        logger.info("✅ Configurações validadas")

        # 4. Knowledge Base
        knowledge_base = create_knowledge_base(config, logger)

        # 5. Agente
        agent = create_agent(config, knowledge_base, logger)

        # 6. Análise
        results = run_analysis(agent, config.analysis_questions, logger)

        # 7. Relatório
        report_path = generate_report(results, config, logger)

        # 8. Preview no console
        logger.info("")
        logger.info("=" * 60)
        logger.info("📊 PREVIEW DO RELATÓRIO")
        logger.info("=" * 60)
        agent.print_response(
            "Com base em todas as análises anteriores, apresente um resumo "
            "executivo de no máximo 10 linhas para a diretoria."
        )

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"✅ Processo concluído com sucesso!")
        logger.info(f"📄 Relatório completo disponível em: {report_path}")
        logger.info("=" * 60)

    except EnvironmentError as e:
        logger.critical(f"❌ Erro de configuração: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.critical(f"❌ Arquivo não encontrado: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("⚠️  Execução interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"❌ Erro inesperado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
