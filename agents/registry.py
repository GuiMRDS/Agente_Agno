from agents.chat_agent import (
    create_chat_agent
)

from agents.pdf_agent import (
    create_pdf_agent
)

def get_agents():

    return [
        create_chat_agent(),
        create_pdf_agent()
    ]