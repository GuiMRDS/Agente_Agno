from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.os import AgentOS

db = SqliteDb(db_file="agno.db")

agent = Agent(
    name="Agno Assist",
    model=Groq(id="openai/gpt-oss-20b"),
    db=db,
)

agent_os = AgentOS(agents=[agent], db=db)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agno_assist:app", reload=True)