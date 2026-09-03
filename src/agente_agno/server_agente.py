import uvicorn
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.reader.pdf_reader import PDFReader
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
    collection="agente_pdf",
    path="tmp/chromadb/agente_pdf",
    persistent_client=True,
    embedder=OllamaEmbedder(
        id="nomic-embed-text"
    )
)
knowledge = Knowledge(vector_db=vector_db)


db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="server_agente",
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
    name = "Agente PDF",
    agents=[agent],
)
app = agent_os.get_app()

# RUN ===========================================================
if __name__ == "__main__":
    knowledge.insert(
        path="D:/Projetos/Temp/ws-pycharm/Agente_Agno/pdf_exemplo/Currículo.pdf",
        reader=PDFReader(),
        skip_if_exists=True
    )
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
    agent_os.serve(app="server_agente:app", reload=True)