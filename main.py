from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import os

app = FastAPI()

# Carrega a chave da API a partir das variáveis de ambiente do Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chatgpt")
def chatgpt(req: PromptRequest):
    # Verifica se a chave da API foi carregada corretamente
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não foi configurada nas variáveis de ambiente.")

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

    # --- INÍCIO DA CORREÇÃO ---
    # Imprime a resposta completa da OpenAI no log do Render para depuração
    print(f"Resposta da OpenAI: {result}")

    # Verifica se a resposta contém a chave "choices" antes de acessá-la
    if "choices" in result and len(result["choices"]) > 0:
        output = result["choices"][0]["message"]["content"].strip()
        return {"response": output}
    else:
        # Se não houver "choices", a OpenAI retornou um erro.
        # Retornamos esse erro para o cliente (Zoho).
        error_message = result.get("error", {}).get("message", "Erro desconhecido da API da OpenAI.")
        print(f"Erro da OpenAI: {error_message}")
        raise HTTPException(status_code=500, detail=f"Erro na API da OpenAI: {error_message}")
    # --- FIM DA CORREÇÃO ---
