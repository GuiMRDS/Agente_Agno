import os
import uvicorn

from dotenv import load_dotenv, find_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.os import AgentOS

load_dotenv(find_dotenv())

db = SqliteDb(
    session_table="agent_session",
    db_file="tmp/agent.db"
)

agent = Agent(
    name="server_agente",
    model=Groq(
        id="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY")
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
    print("Servidor iniciado em http://localhost:8000")

    print("\n=== AGENTES REGISTRADOS ===")
    print(agent)

    print("\n=== ROTAS ===")
    for route in app.routes:
        try:
            print(route.path)
        except Exception:
            pass

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )