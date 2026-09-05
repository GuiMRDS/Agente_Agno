from agno.os import AgentOS

from agents.registry import (
    get_agents
)

agent_os = AgentOS(
    name="Agente",
    agents=get_agents()
)

app = agent_os.get_app()