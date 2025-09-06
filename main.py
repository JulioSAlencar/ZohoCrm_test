from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import os

app = FastAPI()

# Carrega a chave da API a partir das variáveis de ambiente do Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define um modelo para validar o corpo da requisição
class PromptRequest(BaseModel):
    prompt: str

@app.post("/chatgpt")
def chatgpt(req: PromptRequest):
    # Verifica se a chave da API foi carregada corretamente
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="A variável de ambiente OPENAI_API_KEY não foi encontrada.")

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

    # --- CORREÇÃO IMPORTANTE ---
    # Verifica se a resposta da OpenAI contém a chave "choices" ANTES de tentar acessá-la.
    if "choices" in result and len(result["choices"]) > 0:
        output = result["choices"][0]["message"]["content"].strip()
        return {"response": output}
    else:
        # Se "choices" não existe, a OpenAI retornou um erro.
        # Capturamos a mensagem de erro e a retornamos de forma controlada.
        error_message = result.get("error", {}).get("message", "Erro desconhecido retornado pela API da OpenAI.")
        raise HTTPException(status_code=500, detail=f"Erro na API da OpenAI: {error_message}")

