"https://meduza-architect.streamlit.app/"

![Visão Geral](Screenshot_9.png)
![Visão Geral](Screenshot_16.png)
![Visão Geral](1766093357638.jfif)
![Visão Geral](1766093357705.jfif)

🐙 Meduza Architect Pro
Meduza Architect é uma ferramenta de engenharia de prompts e arquitetura de sistemas que transforma descrições em linguagem natural em diagramas Mermaid.js e fluxos de automação prontos para o n8n. Utilizando o poder do Google Gemini 2.5 Pro, ele permite desenhar, visualizar e exportar workflows complexos de IA em segundos.

✨ Funcionalidades Principais
IA Generativa de Diagramas: Descreva a lógica do seu sistema e veja o código Mermaid.js ser gerado e renderizado instantaneamente.

Estilo n8n Nativo: Opção para estilizar diagramas com a identidade visual do n8n (nós, cores e formas específicas).

Exportação Direta para n8n: Gera automaticamente o arquivo .json compatível com a versão v2.0.3+ do n8n, pronto para importar e rodar.

Guia de Workflow Automático: Além do código, a IA gera um tutorial detalhado (Markdown) explicando cada bloco lógico do fluxo criado.

Banco de Dados Local: Salve e gerencie seus rascunhos de arquitetura diretamente na interface via SQLite.

Interface Multi-Modal: Suporte para fluxos que envolvem texto, imagem (Vision) e áudio (Whisper).

🚀 Tecnologias Utilizadas
Linguagem: Python 3.10+

Framework Web: Streamlit

Modelo de IA: Google Gemini 2.5 Pro

Renderização: Mermaid.js (via streamlit_mermaid)

Banco de Dados: SQLite3

🛠️ Como Instalar e Rodar
Clone o repositório:

git clone https://github.com/rbmeneses/Meduza-Architect.git
cd meduza-architect
Instale as dependências:

pip install streamlit streamlit-mermaid google-generativeai
Execute a aplicação:

streamlit run fluxocognos.py
Configuração:

Insira sua Gemini API Key na barra lateral.

Comece a descrever seu fluxo no campo "Comando IA" (ex: "Crie um fluxo de vendas para WhatsApp que verifica se o cliente existe no banco Postgres").

📸 Demonstração
O Meduza Architect permite criar arquiteturas avançadas de Agentes Orquestradores, onde um agente central (Supervisor) delega tarefas para sub-agentes especialistas (Pesquisa, Produtividade, etc).

📄 Exemplo de Fluxo Gerado
Ao utilizar o comando de exportação, o sistema gera:

Diagrama Visual: Representação gráfica no editor.

Workflow JSON: Código pronto para o n8n.

Documentação:

Bloco 1: Verificação de Cliente (Postgres/Supabase).

Bloco 2: Análise de Intenção com LLM.

Bloco 3: Fluxo de Carrinho e Finalização de Pedido.

🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma Issue ou enviar um Pull Request.

📜 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

Desenvolvido para arquitetos de soluções e entusiastas de automação IA.

1. Arquivo requirements.txt
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

Plaintext

streamlit
streamlit-mermaid
google-generativeai
2. Seção de Configuração de API (para adicionar ao README)
Adicione este bloco ao seu README.md para orientar os usuários sobre como obter a chave necessária para o funcionamento da IA:

🔑 Configuração da API Google Gemini
Para que o Meduza Architect funcione, você precisa de uma chave de API do Google AI Studio.

Acesse o Google AI Studio.

Clique em "Get API Key".

Crie uma nova chave em um projeto novo ou existente.

No Meduza Architect, insira essa chave no campo Gemini API Key localizado na barra lateral esquerda.

Nota: O sistema utiliza o modelo gemini-2.5-pro para gerar a lógica dos diagramas e a conversão para o formato n8n.

3. Guia de Uso Rápido (Snippet para o README)
Gerar Diagrama: Digite um comando como "Sistema de triagem de vendas com resposta automática" no campo Comando IA e clique em Gerar Alteração.

Estilo n8n: Ative o checkbox Estilo n8n para que a IA utilize a nomenclatura e cores padrões de nós do n8n no diagrama Mermaid.

Exportar: Após finalizar o desenho, clique em Gerar Exportação para n8n v2.0.3 para obter o JSON de importação e o guia descritivo do workflow.

📥 Como Importar para o n8n
Após gerar e baixar o arquivo workflow.json no Meduza Architect, siga estes passos para colocá-lo em execução:

Abra a sua instância do n8n.

Crie um novo workflow ou abra um existente.

Clique no menu de três pontos (...) no canto superior direito da tela.

Selecione a opção "Import from File" (Importar de Arquivo).

Selecione o arquivo workflow.json baixado.

Configuração de Credenciais: Note que o n8n importará a estrutura dos nós, mas você precisará configurar as suas credenciais (WhatsApp, Google, Postgres, etc.) manualmente em cada nó para que o fluxo funcione.

☁️ Infraestrutura Google Cloud & Vertex AI
O Meduza Architect foi projetado para ser o "cérebro" da sua automação, utilizando a infraestrutura de ponta do Google Cloud.

Principais Componentes Utilizados:
Google Gemini 2.5 Pro: Atua como o orquestrador central, analisando intenções, gerando lógica de código Mermaid e estruturando o JSON do n8n.

Vertex AI (Opcional/Configurável): O código está preparado para escalar para modelos hospedados no Vertex AI, permitindo maior controle sobre a região dos dados e segurança empresarial.

Gemini Vision: Utilizado nos fluxos de mídia para processar e normalizar entradas de imagem enviadas via WhatsApp antes de passá-las para a lógica de decisão.

Vantagens desta Arquitetura:
Escalabilidade: Capaz de lidar com múltiplos sub-agentes especialistas (Pesquisa, Produtividade, RAG) simultaneamente.

Processamento Multimodal: Suporte nativo para Texto, Imagem e Áudio (via Whisper/Google Speech-to-Text) dentro do mesmo workflow.

Baixa Latência: Respostas rápidas para interações de chat em tempo real no WhatsApp.

📂 Estrutura de Arquivos Sugerida
Para manter seu GitHub organizado:

fluxocognos.py: Código fonte principal (Streamlit).

meduza_diagrams.db: Banco de dados SQLite criado automaticamente na primeira execução.

requirements.txt: Dependências do projeto.

README.md: Documentação completa.
