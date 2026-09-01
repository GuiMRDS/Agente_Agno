from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb

from fastapi import FastAPI
import uvicorn
import asyncio

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# RAG
from agno.embedder.ollama import OllamaEmbedder

vector_db = ChromaDb(
    collection="pdf_agent",
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

# FASTAPI ===========================================================
app = FastAPI(title="Agente de PDF", description="Agente de PDF")

@app.get("/agent_pdf")
def agent_pdf(pergunta: str):
    return {"message": agent.run(pergunta)}

# RUN ===========================================================
if __name__ == "__main__":
    asyncio.run(knowledge.add_content_async(
        path="D:/Projetos/Temp/ws-pycharm/Agente_Agno/pdf_exemplo/Currículo.pdf",
        metadata={"source": "Guilherme", "type": "pdf", "description": "Currículo"},
        skip_if_exists=True,
        reader=PDFReader()
    ))
    uvicorn.run("exemplo1.py", host="0.0.0.0", port=8000, reload=True)