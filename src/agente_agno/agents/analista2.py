from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

import os

from agno.utils.streamlit import add_message
from dotenv import load_dotenv

db = SqliteDb(db_file="tmp/agno.db")
load_dotenv()

agent = Agent(
    name="Analista Financeiro",
    model=Groq(id="openai/gpt-oss-20b"),
    tools=[YFinanceTools()],
    instructions="Você é um analista e tem diferentes clientes. Lembre-se de cada cliente, suas informações e preferências.",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    add_memories_to_context=True,
    enable_agentic_memory=True,
)


# agent.print_response(
#    "Olá, prefiro as respostas em formanto de tabelas, gosto de poucas informações.",
#    session_id='pretobras_session_1',
#    user_id='analista_petrobras_1'
# )

# agent.print_response(
#    "Olá, prefiro as respostas em formanto de texto, gosto de bastantes detalhes.",
#   session_id='vale_session_1',
#   user_id='analista_vale_1'
# )



agent.print_response("Qual é a contação Petrobras", session_id='pretobras_session_2', user_id='analista_petrobras')
agent.print_response("Qual é a contação Vale", session_id='vale_session_2', user_id='analista_vale')
