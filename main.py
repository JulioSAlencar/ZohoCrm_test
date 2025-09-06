from fastapi import FastAPI, Request
import requests, os, json

app = FastAPI()  # <<< Isso precisa estar antes de qualquer @app.post

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL = "google/flan-t5-base"

@app.post("/chatgpt")
async def chatgpt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}

    r = requests.post(f"https://api-inference.huggingface.co/models/{MODEL}", headers=headers, json=payload)
    result = r.json()

    output = result[0]["generated_text"] if isinstance(result, list) else str(result)
    return {"response": output}
