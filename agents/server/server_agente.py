import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv, find_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.os import AgentOS

load_dotenv(find_dotenv())

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY não encontrada no arquivo .env"
    )

BASE_DIR = Path(__file__).resolve().parent

TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

db = SqliteDb(
    session_table="agent_session",
    db_file=str(TMP_DIR / "agent.db")
)

agent = Agent(
    name="server_agente",
    model=Groq(
        id="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY
    ),
    db=db,
    instructions=[
        "Você deve chamar o usuário de Guilherme."
    ],
    num_history_runs=3,
    debug_mode=True,
)

agent_os = AgentOS(
    name="Agente",
    agents=[agent]
)

app = agent_os.get_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )