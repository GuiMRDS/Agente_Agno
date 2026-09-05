from agno.agent import Agent

from agents.base.base_agent import create_base_agent

def create_chat_agent():

    base = create_base_agent()

    return Agent(
        name="chat_agent",
        model=base.model,
        db=base.db,
        instructions=[
            "Você deve chamar o usuário de Guilherme."
        ]
    )