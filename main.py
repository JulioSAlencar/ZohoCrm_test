from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/chatgpt")
async def chatgpt(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = await request.form()

    prompt = data.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Campo 'prompt' é obrigatório")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if "choices" in result and len(result["choices"]) > 0:
        output = result["choices"][0]["message"]["content"].strip()
        return {"response": output}
    else:
        error_message = result.get("error", {}).get("message", "Erro desconhecido da API da OpenAI.")
        raise HTTPException(status_code=500, detail=f"Erro na API da OpenAI: {error_message}")