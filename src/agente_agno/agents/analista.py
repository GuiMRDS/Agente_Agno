from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

import os
from dotenv import load_dotenv

db = SqliteDb(db_file="tmp/agno.db")
load_dotenv()

agent = Agent(
    name="Analista Financeiro",
    model=Groq(id="openai/gpt-oss-20b"),
    tools=[YFinanceTools()],
    instructions="Use tabelas para motrar informações final. Não inclua nenhum outro texto",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

agent.print_response("Qual é a contação Petrobras", session_id='pretobras_session', user_id='analista_petrobras')
agent.print_response("Qual é a contação Vale", session_id='vale_session', user_id='analista_vale')
agent.print_response("Quais empresas já consultamos a cotação", session_id='pretobras_session', user_id='analista_empresas')