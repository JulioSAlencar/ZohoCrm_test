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
    # Verificação nº 1: A chave da API foi carregada do ambiente do Render?
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="A variável de ambiente OPENAI_API_KEY não foi configurada no servidor Render."
        )

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": req.prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        # Força uma verificação de erro na resposta HTTP
        response.raise_for_status() 
        result = response.json()
    except requests.exceptions.RequestException as e:
        # Captura erros de conexão ou HTTP (como 401 Unauthorized)
        raise HTTPException(status_code=502, detail=f"Erro ao comunicar com a API da OpenAI: {e}")

    # Verificação nº 2: A resposta da OpenAI contém um resultado de sucesso?
    if "choices" in result and len(result["choices"]) > 0:
        output = result["choices"][0]["message"]["content"].strip()
        return {"response": output}
    else:
        # Se não tiver "choices", a OpenAI retornou um erro estruturado.
        error_message = result.get("error", {}).get("message", "Erro desconhecido da OpenAI.")
        raise HTTPException(
            status_code=500, 
            detail=f"A API da OpenAI retornou um erro: {error_message}"
        )

