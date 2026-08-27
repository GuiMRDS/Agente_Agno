import os

from agno.models.groq import Groq
from agno.models.message import Message

from dotenv import load_dotenv

load_dotenv()

model = Groq(id="openai/gpt-oss-20b")

# Mensagem do usuário 
user_message = Message(role="user", content="Olá, meu nome é Guilherme")

# Mensagem assistente 
assistant_message = Message(role="assistant", content="") 

# Invocar 
response = model.invoke( 
	messages=[user_message], 
	assistant_message=assistant_message )

print(response.content)
