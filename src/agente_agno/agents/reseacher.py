from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

load_dotenv()

agent = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    tools=[TavilyTools()],
    markdown=True,
)

agent.print_response(
    "Pesquise a temperatura atual em Sorocaba-SP e informe a fonte."
)