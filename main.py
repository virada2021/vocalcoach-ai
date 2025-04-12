from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # permite receber chamadas de fora

@app.route("/", methods=["GET"])
def health_check():
    return "OK"

@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta = data.get("pergunta", "")
    resposta = gerar_feedback_vocal(pergunta)
    return jsonify({"resposta": resposta})

def gerar_feedback_vocal(pergunta):
    if "agudo" in pergunta.lower():
        return "Sua afinação nos agudos pode melhorar. Experimente escalas mais lentas com apoio no diafragma."
    elif "respiração" in pergunta.lower():
        return "Seu controle respiratório precisa de treino. Faça exercícios com apneia e apoio."
    elif "voz fraca" in pergunta.lower():
        return "Você precisa de mais projeção. Use exercícios com sons sustentados, como 'M' e 'N'."
    else:
        return "Muito bom! Continue praticando sua afinação e presença vocal. Estou aqui para ajudar!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # fallback local
    app.run(host='0.0.0.0', port=port)
