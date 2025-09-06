from fastapi import FastAPI, Request
import requests, os, json

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY não definida no ambiente!")

@app.post("/chatgpt")
async def chatgpt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = r.json()

    # Debug: log completo do retorno
    print(json.dumps(result, indent=2))

    if "choices" not in result:
        return {"error": result}  # retorna o erro completo da OpenAI

    output = result["choices"][0]["message"]["content"].strip()
    return {"response": output}
