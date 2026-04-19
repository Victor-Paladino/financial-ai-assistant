# FinSight - Assistente Financeiro Inteligente

FinSight é um assistente financeiro baseado em IA que ajuda usuários a entender melhor suas finanças pessoais por meio de explicações simples, análise de gastos e educação financeira contextualizada.

O projeto utiliza **Streamlit** e a **Google Gemini API**, simulando um educador financeiro que responde com base em dados estruturados do usuário.

---

## Demonstração

O usuário pode interagir com o FinSight fazendo perguntas como:

- “Onde estou gastando mais?”
- “O que é reserva de emergência?”
- “Como organizar meu orçamento?”

O sistema responde com explicações personalizadas baseadas no perfil financeiro simulado.

---

## Funcionalidades

- Análise automática de gastos por categoria  
- Resumo financeiro (receitas, despesas e saldo)  
- Contextualização com dados do usuário  
- Explicação de conceitos financeiros com IA  
- Interface de chat estilo assistente  
- Atualização em tempo real com Streamlit  

---

## Tecnologias Utilizadas

- Python  
- Streamlit  
- Pandas  
- Google Gemini API  
- python-dotenv  

---

## Como Executar

### 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/finsight.git
cd finsight

### 2. Criar ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate  
#### Windows
#### source venv/bin/activate  
#### Mac/Linux (caso alguém fora do Windows exista no seu universo)

### 3. Instalar dependências
pip install -r requirements.txt

### 4. Configurar API Key
Crie um arquivo `.env` na raiz do projeto:

GEMINI_API_KEY=sua-chave-aqui

### 5. Executar aplicação
streamlit run app.py
