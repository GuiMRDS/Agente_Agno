from agno.agent import Agent

from agents.base_agent import create_base_agent

from services.knowledge_service import (
    KnowledgeService
)

from config.settings import PDF_DIR

def create_pdf_agent():

    knowledge = KnowledgeService.load_pdf(
        str(PDF_DIR / "Curriculo.pdf")
    )

    base = create_base_agent()

    return Agent(
        name="pdf_agent",
        model=base.model,
        db=base.db,
        knowledge=knowledge,
        search_knowledge=True
    )