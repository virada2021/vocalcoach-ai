from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 SUA CHAVE DO OPENROUTER
OPENROUTER_API_KEY = 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

# 🔁 Função que envia a pergunta para a IA (OpenRouter com GPT-3.5 Turbo)
def enviar_para_ia(pergunta):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um coach vocal experiente. Ajude o usuário com estudo de canto, "
                    "exercícios práticos, análise vocal e suporte emocional com respostas claras, educativas e personalizadas."
                )
            },
            {"role": "user", "content": pergunta}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao conectar com a IA: {str(e)}"

# 🧠 Endpoint principal da IA
@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta = data.get("pergunta", "")
    
    if not pergunta:
        return jsonify({"resposta": "Pergunta vazia!"}), 400

    resposta_ia = enviar_para_ia(pergunta)
    return jsonify({"resposta": resposta_ia})

# ✅ Teste básico
@app.route("/", methods=["GET"])
def home():
    return "ok"


