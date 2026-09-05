import json
import requests

AGENT_ID = "server_agente"

ENDPOINT_URL = (
    f"http://localhost:8000/agents/{AGENT_ID}/runs"
)


def get_response_stream(message: str):
    try:
        response = requests.post(
            ENDPOINT_URL,
            files={
                "message": (None, message),
                "stream": (None, "true")
            },
            stream=True,
            timeout=30
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return

    for line in response.iter_lines():

        if not line:
            continue

        if line.startswith(b"data: "):
            try:
                yield json.loads(line[6:])
            except json.JSONDecodeError:
                pass


def print_stream_response(message: str):

    for event in get_response_stream(message):

        event_type = event.get("event")

        if event_type == "RunContent":
            print(
                event.get("content", ""),
                end="",
                flush=True
            )

        elif event_type == "RunCompleted":
            print("\n")


if __name__ == "__main__":
    pergunta = input("Digite uma mensagem: ")
    print_stream_response(pergunta)