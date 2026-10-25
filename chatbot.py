import ollama
from ollama import Client

MODEL_NAME="qwen3:0.6b"

client=Client(

    host="http://127.0.0.1:11434",
    trust_env=False
)



def get_ai_response(messages):
    try:
        response=client.chat(
            model=MODEL_NAME,
            messages=messages ,
            think=False
        )
        answer=response.message.content
        if "</think>" in answer:
            answer=answer.split("</think>")[-1]
        return answer.strip()
    except Exception as error:
        raise RuntimeError(
            f"unexcepted error while get AI response:{error}"
        )from error
    except ConnectionError as error:
        raise RuntimeError(
            "could not connect to Ollama"
            "make sure ollama is running"
        )from error
    except ollama.ResponseError as error:
        if error.status_code ==404:
            raise RuntimeError(
                f"model'{MODEL_NAME}'was not found."
                f"run: ollama pull {MODEL_NAME}"  
            )from error
        raise RuntimeError(
            f"ollama returned an error:{error.error}"
        )from error
            