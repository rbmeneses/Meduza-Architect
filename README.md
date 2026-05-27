"https://meduza-architect.streamlit.app/"

![Visão Geral](Screenshot_9.png)
![Visão Geral](Screenshot_16.png)
![Visão Geral](1766093357638.jfif)
![Visão Geral](1766093357705.jfif)

Markdown
# 🐙 Meduza Architect Pro

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Pro-8E75B2?logo=google&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Compatible-FF6D5A?logo=n8n&logoColor=white)

O **Meduza Architect Pro** é uma ferramenta avançada de engenharia de prompts e arquitetura de sistemas que transforma descrições em linguagem natural em diagramas [Mermaid.js](https://mermaid.js.org/) e fluxos de automação prontos para o [n8n](https://n8n.io/). 

Utilizando o poder do **Google Gemini 2.5 Pro**, o Meduza permite desenhar, visualizar e exportar workflows complexos de IA e orquestração de agentes em poucos segundos.

---

## ✨ Funcionalidades Principais

* **IA Generativa de Diagramas:** Descreva a lógica do seu sistema e veja o código Mermaid.js ser gerado e renderizado instantaneamente na interface.
* **Estilo n8n Nativo:** Opção para estilizar os diagramas com a identidade visual do n8n (nomenclatura, cores e formas específicas de nós).
* **Exportação Direta para n8n:** Gera automaticamente o arquivo `.json` (compatível com n8n v2.0.3+), pronto para importação direta.
* **Guia de Workflow Automático:** A IA gera um tutorial detalhado em Markdown explicando cada bloco lógico do fluxo arquitetado.
* **Banco de Dados Local:** Salve, recupere e gerencie seus rascunhos de arquitetura diretamente na interface via SQLite.
* **Suporte Multi-Modal:** Estruture fluxos que envolvem texto, visão computacional (Vision) e áudio (Whisper/Speech-to-Text).

---

## 🚀 Arquitetura e Tecnologias

O Meduza Architect foi projetado para atuar como o "cérebro" do desenho da sua automação, sendo altamente escalável para múltiplos sub-agentes especialistas (Pesquisa, Produtividade, RAG).

* **Linguagem:** Python 3.10+
* **Interface / Framework Web:** Streamlit
* **Motor de IA (Orquestrador):** Google Gemini 2.5 Pro
* **Motor de Renderização:** Mermaid.js (via `streamlit-mermaid`)
* **Persistência de Dados:** SQLite3
* **Infraestrutura Cloud (Opcional):** Pronto para integração com **Google Cloud & Vertex AI**, permitindo maior segurança empresarial e controle regional de dados.

---

## 🛠️ Instalação e Execução

### Pré-requisitos
Certifique-se de ter o Python 3.10 ou superior instalado em sua máquina.

### 1. Clonar o repositório

git clone [https://github.com/rbmeneses/Meduza-Architect.git](https://github.com/rbmeneses/Meduza-Architect.git)
cd meduza-architect
2. Instalar as dependências
Recomenda-se o uso de um ambiente virtual (venv). Execute:

Bash
pip install -r requirements.txt
3. Configurar a Chave de API
Para o sistema funcionar, é necessária uma API Key do Google AI Studio:

Acesse o Google AI Studio.

Clique em "Get API Key" e gere uma nova chave.

Você irá inserir essa chave na barra lateral da aplicação após iniciá-la.

4. Rodar a aplicação
Bash
streamlit run fluxocognos.py
📖 Como Usar
Configuração Inicial: Ao abrir a interface, insira sua Gemini API Key na barra lateral esquerda.

Gerar Diagrama: No campo Comando IA, descreva seu fluxo.

Exemplo: `"Crie um sistema de triagem de vendas para WhatsApp que verifica se o cliente existe no banco Postgres e passa por um agente LLM para análise de intenção."*

Estilo: Ative o checkbox Estilo n8n se desejar que a IA utilize a identidade visual padrão da ferramenta.

Executar: Clique em Gerar Alteração.

Exportar: Após a renderização visual, clique em Gerar Exportação para n8n v2.0.3. O sistema fornecerá o JSON do workflow e a documentação dos blocos lógicos.

📥 Importando para o n8n
Após gerar e baixar o seu arquivo workflow.json através do Meduza:

Abra sua instância do n8n.

Crie um novo workflow ou abra um painel em branco.

Clique no menu de três pontos (...) no canto superior direito da tela.

Selecione Import from File e escolha o arquivo .json gerado.

Aviso de Credenciais: O n8n importará perfeitamente a estrutura e a lógica dos nós. No entanto, por questões de segurança, você precisará configurar suas credenciais (WhatsApp, Postgres, APIs do Google, etc.) manualmente dentro de cada nó.

📂 Estrutura do Projeto
Plaintext
meduza-architect/
├── fluxocognos.py       # Código fonte principal da aplicação (Streamlit)
├── requirements.txt     # Dependências do projeto (Python)
├── README.md            # Documentação do projeto
└── meduza_diagrams.db   # Banco de dados SQLite (Gerado automaticamente na 1ª execução)

### Dica extra de organização no repositório:
Certifique-se de que o seu arquivo `requirements.txt` contenha exatamente isto e esteja na raiz do projeto (como referenciado na estrutura acima):


streamlit
streamlit-mermaid
google-generativeai
