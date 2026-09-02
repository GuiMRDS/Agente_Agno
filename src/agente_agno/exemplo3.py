import requests
import json
from pprint import pprint

AGENT_ID = "agente_pdf"
ENDPOINT_URL = f"http://localhost:7777/agents/{AGENT_ID}/runs"


def get_response_strem(message: str):
    response = requests.post(
        url=ENDPOINT_URL,
        data={
            "message": message,
            "strem": "true"
        },
        stream=True
    )

    return type(response)




if __name__ == "__main__":
    message = input("Digite uma mensagem: ")
    response = get_response_strem(message)
    print(response)