import streamlit as st
from streamlit_mermaid import st_mermaid
import google.generativeai as genai
import re
import sqlite3
import datetime

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

# Instancia o banco
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
    
    /* Melhoria visual na Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    
    @media print {
        [data-testid="stSidebar"], header, footer, .stButton, .stTabs nav { display: none !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
    }
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
            self.model = genai.GenerativeModel('gemini-3-pro-preview')

    def _clean_response(self, text):
        pattern = r"```(?:mermaid)?(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match: text = match.group(1)
        return text.strip()

    def generate_diagram(self, prompt, current_code=""):
        if not self.api_key: return "graph TD\nError[Configure a API Key]"
        system_prompt = "Você é um especialista em Mermaid.js. Gere APENAS o código."
        try:
            response = self.model.generate_content(f"{system_prompt}\nContexto: {current_code}\nPedido: {prompt}")
            return self._clean_response(response.text)
        except Exception as e:
            return f"graph TD\nError[Erro IA: {str(e)}]"

    def fix_code(self, broken_code, error_msg):
        if not self.api_key: return broken_code
        try:
            response = self.model.generate_content(f"Corrija este Mermaid (Erro: {error_msg}). Retorne APENAS o código:\n{broken_code}")
            return self._clean_response(response.text)
        except: return broken_code

# ==========================================
# 4. TEMPLATES COMPLEXOS
# ==========================================
TEMPLATES = {
    "Vazio": "graph TD\n    Start --> End",
    
    "Fluxo n8n Avançado (WhatsApp)": """graph TD
    %% Estilos
    classDef whatsapp fill:#25D366,stroke:#128C7E,color:white;
    classDef db fill:#333,stroke:#fff,color:white,shape:cylinder;
    classDef ai fill:#8e44ad,stroke:#9b59b6,color:white;
    
    A[Webhook WhatsApp: Recebe Mensagem]:::whatsapp --> B[Busca Cliente pelo Telefone]
    B --> C{Cliente Existe?}
    C -- Não --> D[Cria Novo Cliente no BD]:::db
    C -- Sim --> E[Carrega Histórico e Carrinho]:::db
    D --> E
    E --> F[AI Agent: Analisa Intenção]:::ai
    
    %% Fluxo de Dúvidas
    F -- Dúvida --> G[LLM: RAG Knowledge Base]:::ai
    G --> H[WhatsApp: Envia Resposta]:::whatsapp
    H --> I[BD: Salva Log]:::db

    %% Fluxo de Carrinho
    F -- Pedido --> J[Identifica Produto e Qtd]
    J --> K{Ação}
    K -- Adicionar --> L[API Estoque]
    L -- OK --> O[Atualiza Carrinho]:::db
    L -- Falta --> N[Avisa Indisponibilidade]:::whatsapp
    O --> P[Calcula Total]
    P --> Q[Confirmação]:::whatsapp
    Q --> I

    %% Pagamento
    F -- Pagar --> R{Tem CEP?}
    R -- Sim --> T[Calcula Frete]
    T --> U[Total + Frete]
    U --> V[Confirma Valores]:::whatsapp
    V --> W{Confirmado?}
    W -- Sim --> X[Gera PIX]
    X --> Y[Envia QR Code]:::whatsapp
    Y --> Z((Aguardando PIX))
    Z --> AA[Pagamento Confirmado]""",

    "Arquitetura AWS Microservices": """C4Context
      title Arquitetura E-commerce Cloud
      
      Person(customer, "Cliente", "Usuário do App Mobile")
      
      System_Boundary(c1, "AWS Cloud") {
        System(api, "API Gateway", "Entry Point")
        
        System_Boundary(c2, "Backend Services") {
            Container(auth, "Auth Service", "Lambda", "JWT Auth")
            Container(cart, "Cart Service", "ECS Fargate", "Gerencia Carrinho")
            Container(payment, "Payment Service", "ECS Fargate", "Processa Pagamento")
        }
        
        System_Boundary(c3, "Data Layer") {
            SystemDb(user_db, "User DB", "DynamoDB")
            SystemDb(cart_db, "Cart Redis", "ElastiCache")
            SystemDb(orders_db, "Orders DB", "Aurora Serverless")
        }
        
        System_Boundary(c4, "Async Events") {
            SystemQueue(sns, "SNS Topic", "Order Events")
            SystemQueue(sqs, "SQS Queue", "Invoice Processing")
        }
      }
      
      Rel(customer, api, "HTTPS/REST")
      Rel(api, auth, "Validate Token")
      Rel(api, cart, "Add Items")
      Rel(api, payment, "Checkout")
      
      Rel(auth, user_db, "Read/Write")
      Rel(cart, cart_db, "Cache")
      Rel(payment, orders_db, "Store Order")
      
      Rel(payment, sns, "Publish Event")
      Rel(sns, sqs, "Fan-out")""",
      
    "Mapa Mental Projeto": "mindmap\n  root((Lançamento SaaS))\n    Produto\n      MVP\n      Beta Test\n    Marketing\n      Ads\n      Social\n    Vendas\n      CRM\n      Funil"
}

# ==========================================
# 5. GESTÃO DE ESTADO
# ==========================================
if "mermaid_code" not in st.session_state:
    st.session_state["mermaid_code"] = TEMPLATES["Vazio"]
if "history" not in st.session_state:
    st.session_state["history"] = []
if "fullscreen" not in st.session_state:
    st.session_state["fullscreen"] = False

def update_code(new_code):
    if st.session_state["mermaid_code"] != new_code:
        st.session_state["history"].append(st.session_state["mermaid_code"])
        st.session_state["mermaid_code"] = new_code

# ==========================================
# 6. INTERFACE
# ==========================================

# --- SIDEBAR: CONTROLE TOTAL ---
with st.sidebar:
    st.title("🐙 Meduza Pro")
    api_key = st.text_input("Gemini API Key", type="password")
    ai_engine = MeduzaAI(api_key)
    
    st.divider()
    
    # ABAS DA SIDEBAR
    tab_lib, tab_db, tab_file = st.tabs(["📚 Modelos", "💾 Banco", "📂 Upload"])
    
    # 1. TEMPLATES
    with tab_lib:
        selected_tpl = st.selectbox("Escolha um modelo:", list(TEMPLATES.keys()))
        if st.button("Carregar Modelo", use_container_width=True):
            update_code(TEMPLATES[selected_tpl])
            st.rerun()
            
    # 2. BANCO DE DADOS
    with tab_db:
        st.caption("Salvar Fluxo Atual")
        save_name = st.text_input("Nome do fluxo", placeholder="Ex: Checkout V2")
        if st.button("💾 Salvar no Banco", use_container_width=True):
            if save_name:
                if db.save_diagram(save_name, st.session_state["mermaid_code"]):
                    st.toast(f"'{save_name}' salvo com sucesso!", icon="✅")
                else:
                    st.error("Erro ao salvar.")
            else:
                st.warning("Digite um nome.")
        
        st.divider()
        st.caption("Carregar do Banco")
        saved_items = db.get_all_diagrams() # Retorna (id, name, code, date)
        
        if saved_items:
            # Cria dicionário para mapear Nome -> ID/Codigo
            map_saved = {f"{item[1]} ({item[3][:16]})": item for item in saved_items}
            selected_saved = st.selectbox("Seus fluxos:", list(map_saved.keys()))
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📂 Abrir", use_container_width=True):
                    code_to_load = map_saved[selected_saved][2]
                    update_code(code_to_load)
                    st.rerun()
            with c2:
                if st.button("❌ Apagar", use_container_width=True):
                    id_to_del = map_saved[selected_saved][0]
                    db.delete_diagram(id_to_del)
                    st.rerun()
        else:
            st.info("Nenhum fluxo salvo ainda.")

    # 3. UPLOAD DE ARQUIVO
    with tab_file:
        uploaded_file = st.file_uploader("Carregar .mmd ou .txt", type=["mmd", "txt"])
        if uploaded_file is not None:
            stringio = uploaded_file.getvalue().decode("utf-8")
            if st.button("Importar Arquivo"):
                update_code(stringio)
                st.toast("Arquivo importado!", icon="📂")
                st.rerun()

# --- ÁREA PRINCIPAL ---
col_head, col_act = st.columns([0.85, 0.15], vertical_alignment="bottom")
with col_head:
    st.title("🧠 Meduza Architect")
with col_act:
    if st.button("👁️ Tela Cheia" if not st.session_state["fullscreen"] else "✏️ Editar"):
        st.session_state["fullscreen"] = not st.session_state["fullscreen"]
        st.rerun()

# --- MODO TELA CHEIA ---
if st.session_state["fullscreen"]:
    st.toast("Pressione Ctrl+P para imprimir em PDF", icon="🖨️")
    try:
        st_mermaid(st.session_state["mermaid_code"], height=900)
    except Exception as e:
        st.error(f"Erro: {e}")

# --- MODO EDITOR ---
else:
    # 1. Prompt IA
    with st.container():
        c1, c2 = st.columns([5, 1])
        with c1:
            prompt = st.text_input("Comando IA", placeholder="Descreva a alteração ou o novo fluxo...", label_visibility="collapsed")
        with c2:
            if st.button("✨ Gerar", type="primary", use_container_width=True):
                with st.spinner("Processando..."):
                    new_c = ai_engine.generate_diagram(prompt, st.session_state["mermaid_code"])
                    update_code(new_c)
                    st.rerun()

    # 2. Editor vs Preview
    col_edit, col_view = st.columns([1, 1.4])
    
    with col_edit:
        st.caption("Editor de Código")
        txt = st.text_area("Code", st.session_state["mermaid_code"], height=600, label_visibility="collapsed")
        if txt != st.session_state["mermaid_code"]:
            st.session_state["mermaid_code"] = txt
            
        # Histórico (Undo)
        if st.button("↩️ Desfazer Alteração", disabled=not st.session_state["history"]):
            st.session_state["mermaid_code"] = st.session_state["history"].pop()
            st.rerun()

    with col_view:
        st.caption("Visualização em Tempo Real")
        try:
            st_mermaid(st.session_state["mermaid_code"], height=600)
        except Exception as e:
            st.error("Erro de Sintaxe no Mermaid")
            if st.button("🚑 Tentar Auto-Correção IA"):
                fixed = ai_engine.fix_code(st.session_state["mermaid_code"], str(e))
                update_code(fixed)
                st.rerun()
                
    st.markdown("---")
    
    # 3. Exportação HTML Offline
    def get_html_download(code):
        return f"""<!DOCTYPE html><html><body><div class="mermaid">{code}</div>
        <script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});</script></body></html>"""
        
    st.download_button("🌍 Baixar Versão HTML (Offline)", get_html_download(st.session_state["mermaid_code"]), "fluxo.html", "text/html")