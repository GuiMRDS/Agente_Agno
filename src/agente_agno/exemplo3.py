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

    for line in response.iter_lines():
        if line:
            if line.startswith(b'data: '):
                data = line[6:]
                try:
                    event = json.loads(data)
                    yield event
                except json.decoder.JSONDecodeError:
                    continue



def print_stream_response(message: str):
    for event in get_response_strem(message):
        event_type = event.get("event", "")
        print(event_type)



if __name__ == "__main__":
    message = input("Digite uma mensagem: ")
    print_stream_response(message)