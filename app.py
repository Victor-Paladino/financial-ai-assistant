import json
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ========= CARREGA .ENV =========
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key do Gemini não encontrada. Verifique seu .env")
    st.stop()

genai.configure(api_key=api_key)

MODEL = "gemini-1.5-flash-001"
model = genai.GenerativeModel(MODEL)

# ========= DADOS =========
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ========= RESUMO =========
def gerar_resumo():
    receitas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
    despesas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()

    categorias = (
        transacoes[transacoes["tipo"] == "saida"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": receitas - despesas,
        "top_categoria": categorias.idxmax(),
        "top_valor": categorias.max()
    }

resumo = gerar_resumo()

# ========= CONTEXTO =========
def montar_contexto():
    return f"""
Cliente: {perfil['nome']}, {perfil['idade']} anos
Perfil: {perfil['perfil_investidor']}
Objetivo: {perfil['objetivo_principal']}

Receitas: R$ {resumo['receitas']:.2f}
Despesas: R$ {resumo['despesas']:.2f}
Saldo: R$ {resumo['saldo']:.2f}

Maior gasto: {resumo['top_categoria']} (R$ {resumo['top_valor']:.2f})

Reserva atual: R$ {perfil['reserva_emergencia_atual']}
"""

# ========= PROMPT =========
SYSTEM_PROMPT = """
Você é o FinSight, um educador financeiro inteligente.

Regras:
- Explique de forma simples
- Use dados do cliente sempre que possível
- Não recomende produtos financeiros específicos
- Não invente informações
- Seja direto e didático (máximo 3 parágrafos)
- Sempre mantenha o nome FinSight como identidade
"""

# ========= IA (GEMINI) =========
def perguntar(pergunta):
    prompt = f"""
{SYSTEM_PROMPT}

Contexto do cliente:
{montar_contexto()}

Pergunta:
{pergunta}
"""

    response = model.generate_content(prompt)
    return response.text

# ========= STREAMLIT =========
st.title("🎓 FinSight - Educador Financeiro Inteligente (Gemini)")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

# Mensagem inicial opcional
if len(st.session_state.chat) == 0:
    st.chat_message("assistant").write(
        "Olá, eu sou o FinSight. Posso te ajudar a entender suas finanças de forma simples."
    )

if pergunta := st.chat_input("Pergunte sobre suas finanças..."):
    st.chat_message("user").write(pergunta)
    st.session_state.chat.append({"role": "user", "content": pergunta})

    with st.spinner("Analisando suas finanças..."):
        try:
            resposta = perguntar(pergunta)
        except Exception as e:
            resposta = f"Erro ao chamar a API: {str(e)}"

    st.chat_message("assistant").write(resposta)
    st.session_state.chat.append({"role": "assistant", "content": resposta})
