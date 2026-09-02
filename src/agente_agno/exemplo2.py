from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.os import AgentOS
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# RAG
from agno.knowledge.embedder.ollama import OllamaEmbedder

vector_db = ChromaDb(
    collection="pdf_agent_ollama",
    path="tmp/chromadb",
    persistent_client=True,
    embedder=OllamaEmbedder(
        id="nomic-embed-text"
    )
)
knowledge = Knowledge(vector_db=vector_db)


db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de PDF",
    model=Groq(id="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY")),
    db=db,
    knowledge=knowledge,
    instructions="Você deve chamar o usuário de Guilherme",
    description="",
    search_knowledge=True,
    num_history_runs=3,
    debug_mode=True
)

# AGENT OS ===========================================================
agent_os = AgentOS(
    agents=[agent],
)

app = agent_os.get_app()

# RUN ===========================================================
if __name__ == "__main__":
    agent_os.serve(app="exemplo2:app", reload=True)