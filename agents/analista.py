
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

load_dotenv()

agent = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    tools=[YFinanceTools()],
    markdown=True,
    instructions="Use tabelas para motrar informações final. Não inclua nenhum outro texto"
)

agent.print_response("Qual é a contação Petrobras")
agent.print_response("Qual é a contação Vale")
agent.print_response("Quausi empresas já consultamos a cotação")