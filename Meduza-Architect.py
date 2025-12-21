import streamlit as st
from streamlit_mermaid import st_mermaid
import google.generativeai as genai
import re
import sqlite3
import datetime
import json

# ==========================================
# 1. BANCO DE DADOS (SQLite Local)
# ==========================================
class DiagramDB:
    def __init__(self, db_name="meduza_diagrams.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS diagrams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_diagram(self, name, code):
        try:
            self.conn.execute("INSERT INTO diagrams (name, code) VALUES (?, ?)", (name, code))
            self.conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
            return False

    def get_all_diagrams(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, code, created_at FROM diagrams ORDER BY created_at DESC")
        return cursor.fetchall()

    def delete_diagram(self, diagram_id):
        self.conn.execute("DELETE FROM diagrams WHERE id = ?", (diagram_id,))
        self.conn.commit()

db = DiagramDB()

# ==========================================
# 2. CONFIGURAÇÃO E CSS
# ==========================================
st.set_page_config(
    page_title="Meduza Architect Pro",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    textarea {
        font-family: 'Fira Code', 'Consolas', monospace !important; 
        font-size: 13px !important;
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
        border: 1px solid #444;
    }
    .stButton>button { font-weight: 600; border-radius: 6px; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE IA (GEMINI)
# ==========================================
class MeduzaAI:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _clean_response(self, text):
        pattern = r"```(?:mermaid)?(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match: text = match.group(1)
        return text.strip()

    def generate_diagram(self, prompt, current_code="", n8n_mode=False):
        if not self.api_key: return "graph TD\nError[Configure a API Key]"
        style_instruction = "Use nomes de nós reais do n8n se n8n_mode for True." if n8n_mode else ""
        system_prompt = f"Você é um especialista em Mermaid.js. {style_instruction} Retorne APENAS o código."
        try:
            response = self.model.generate_content(f"{system_prompt}\nContexto: {current_code}\nPedido: {prompt}")
            return self._clean_response(response.text)
        except Exception as e:
            return f"graph TD\nError[Erro IA: {str(e)}]"

    def generate_n8n_resources(self, mermaid_code):
        if not self.api_key: return None, "Erro: Sem API Key."
        prompt = f"""
        Atue como Especialista n8n (v2.0.3). Converta o Mermaid em Workflow JSON:
        {mermaid_code}
        REGRAS: 1. typeVersion: 1. 2. Objeto 'options': {{}} sempre presente.
        ---START_JSON---
        (JSON)
        ---END_JSON---
        ---START_GUIDE---
        (Markdown)
        ---END_GUIDE---
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            json_c = text.split("---START_JSON---")[1].split("---END_JSON---")[0].strip() if "---START_JSON---" in text else ""
            json_c = re.sub(r"```json\n|```", "", json_c)
            guide_c = text.split("---START_GUIDE---")[1].split("---END_GUIDE---")[0].strip() if "---START_GUIDE---" in text else text
            return json_c, guide_c
        except Exception as e:
            return None, str(e)

# ==========================================
# 4. TEMPLATES
# ==========================================
TEMPLATES = {
    "Vazio": "graph TD\n    Start --> End",
    "Fluxo n8n Avançado (WhatsApp)": """graph TD
    A[Webhook WhatsApp] --> B{Cliente Existe?}
    B -- Não --> D[Cria Cliente]
    B -- Sim --> E[AI Agent Supervisor]
    D --> E""",
    "Mapa Mental Projeto": "mindmap\n  root((Projeto))\n    Fase 1\n    Fase 2"
}

# ==========================================
# 5. GESTÃO DE ESTADO
# ==========================================
if "mermaid_code" not in st.session_state: st.session_state["mermaid_code"] = TEMPLATES["Vazio"]
if "history" not in st.session_state: st.session_state["history"] = []
if "fullscreen" not in st.session_state: st.session_state["fullscreen"] = False
if "n8n_json" not in st.session_state: st.session_state["n8n_json"] = None
if "n8n_guide" not in st.session_state: st.session_state["n8n_guide"] = None

def update_code(new_code):
    if st.session_state["mermaid_code"] != new_code:
        st.session_state["history"].append(st.session_state["mermaid_code"])
        st.session_state["mermaid_code"] = new_code

# ==========================================
# 6. INTERFACE
# ==========================================
with st.sidebar:
    st.title("🐙 Meduza Pro")
    api_key = st.text_input("Gemini API Key", type="password")
    ai_engine = MeduzaAI(api_key)
    st.divider()
    
    tab_lib, tab_db, tab_file = st.tabs(["📚 Modelos", "💾 Banco", "📂 Upload"])
    
    with tab_lib:
        sel_tpl = st.selectbox("Modelos:", list(TEMPLATES.keys()))
        if st.button("Carregar Modelo", use_container_width=True):
            update_code(TEMPLATES[sel_tpl])
            st.rerun()

    with tab_db:
        s_name = st.text_input("Nome do fluxo")
        if st.button("💾 Salvar no Banco", use_container_width=True):
            if s_name:
                db.save_diagram(s_name, st.session_state["mermaid_code"])
                st.toast("Salvo!", icon="✅")
        st.divider()
        items = db.get_all_diagrams()
        if items:
            map_items = {f"{i[1]} ({i[3][:10]})": i for i in items}
            sel_saved = st.selectbox("Seus fluxos:", list(map_items.keys()))
            if st.button("📂 Abrir", use_container_width=True):
                update_code(map_items[sel_saved][2])
                st.rerun()

    with tab_file:
        up_f = st.file_uploader("Upload .mmd", type=["mmd", "txt"])
        if up_f and st.button("Importar Arquivo"):
            update_code(up_f.getvalue().decode("utf-8"))
            st.rerun()

# ÁREA PRINCIPAL
st.title("🧠 Meduza Architect")

if st.session_state["fullscreen"]:
    st_mermaid(st.session_state["mermaid_code"], height=800)
    if st.button("✏️ Voltar ao Editor"):
        st.session_state["fullscreen"] = False
        st.rerun()
else:
    col_e, col_v = st.columns([1, 1.4])
    
    with col_e:
        prompt = st.text_input("Comando IA", placeholder="Descreva a alteração...")
        n8n_st = st.checkbox("🎨 Estilo n8n")
        
        if st.button("✨ Gerar Alteração", type="primary", use_container_width=True):
            # ANIMAÇÃO DE LOADING ADICIONADA AQUI
            with st.spinner("🤖 A IA está desenhando seu fluxo..."):
                new_c = ai_engine.generate_diagram(prompt, st.session_state["mermaid_code"], n8n_st)
                update_code(new_c)
                st.rerun()
        
        txt = st.text_area("Editor Mermaid", st.session_state["mermaid_code"], height=450)
        if txt != st.session_state["mermaid_code"]:
            update_code(txt)
            st.rerun()

    with col_v:
        st_mermaid(st.session_state["mermaid_code"], height=550)
        if st.button("👁️ Tela Cheia", use_container_width=True):
            st.session_state["fullscreen"] = True
            st.rerun()

    st.divider()
    
    if st.button("🚀 Gerar Exportação para n8n v2.0.3", use_container_width=True):
        # ANIMAÇÃO DE LOADING ADICIONADA AQUI
        with st.spinner("📦 Empacotando workflow e criando tutorial..."):
            j, g = ai_engine.generate_n8n_resources(st.session_state["mermaid_code"])
            st.session_state["n8n_json"], st.session_state["n8n_guide"] = j, g

    if st.session_state["n8n_json"]:
        st.success("Workflow gerado com sucesso!")
        st.download_button("📥 Baixar JSON do n8n", st.session_state["n8n_json"], "workflow.json", "application/json")
        st.markdown(st.session_state["n8n_guide"])
