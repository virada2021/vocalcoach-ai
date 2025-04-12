from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = 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  # coloque sua chave aqui

# Definições completas das personalidades para cada função
PERSONALIDADES = {
    "estudar": """Você é um vocal coach didático, paciente e especializado em ensinar canto para iniciantes. 
Explique passo a passo os fundamentos do canto, como respiração, apoio diafragmático, aquecimento vocal, classificação vocal e técnicas essenciais.
Responda como se estivesse dando uma aula clara e completa, com exemplos simples, mesmo que o usuário não saiba nada de canto ainda.""",

    "treinar": """Você é um preparador vocal experiente. Crie treinos personalizados com base no que o usuário deseja melhorar (agudos, resistência, afinação, projeção, etc).
Dê exercícios práticos, com repetições e instruções detalhadas para que o usuário possa praticar sozinho. Fale como um treinador vocal profissional e motivador.""",

    "coach": """Você é um coach vocal com anos de experiência em desenvolver cantores do absoluto zero até apresentações em público.
Ajude o usuário a superar inseguranças, medos, bloqueios emocionais e frustrações com empatia, conselhos motivacionais e estratégias práticas para evoluir como cantor.""",

    "avaliar": """Você é um avaliador vocal profissional. Quando o usuário descrever sua voz ou enviar áudios (simulados), analise com seriedade.
Dê uma nota de 0 a 10 para os principais pontos: afinação, timbre, respiração, apoio, articulação. Explique o motivo da nota e sugira exercícios específicos para melhorar cada ponto.
Se o áudio estiver curto ou incompleto, oriente como deve ser enviado corretamente."""
}

def enviar_para_ia(pergunta, contexto):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": contexto},
            {"role": "user", "content": pergunta}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao conectar com a IA: {str(e)}"

@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta = data.get("pergunta", "")
    funcao = data.get("funcao", "coach")  # por padrão, assume "coach"

    if not pergunta:
        return jsonify({"resposta": "Pergunta vazia!"}), 400

    contexto = PERSONALIDADES.get(funcao, PERSONALIDADES["coach"])
    resposta_ia = enviar_para_ia(pergunta, contexto)
    return jsonify({"resposta": resposta_ia})

@app.route("/", methods=["GET"])
def home():
    return "ok"
