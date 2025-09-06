from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

OPENAI_API_KEY = "SUA_API_KEY"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chatgpt")
def chatgpt(req: PromptRequest):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": req.prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    output = result["choices"][0]["message"]["content"].strip()
    return {"response": output}