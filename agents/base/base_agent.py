from agno.agent import Agent
from agno.models.groq import Groq

from config.settings import (
    MODEL_ID,
    GROQ_API_KEY
)

from database.sqlite import get_sqlite

def create_base_agent():

    return Agent(
        model=Groq(
            id=MODEL_ID,
            api_key=GROQ_API_KEY
        ),
        db=get_sqlite(),
        num_history_runs=3,
        debug_mode=True
    )