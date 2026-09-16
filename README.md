# 🛡️ CKP01 — CyberSafe

### Chatbot Profissional de Cibersegurança

**Prompt Engineering & AI · FIAP · Ciência da Computação · 2º Semestre 2026**

---

## 👥 Integrantes

- **Pedro Soares de Souza — RM 571285**
- **Olavo Dadario Vianna Barreto — RM 569272**
- **Jhon Cutile Titirico — RM 571976**
- **Paulo Henrique Lira Bilac de Araujo — RM 569496**
- **Nome do Integrante 3 — RM XXXXX**

---

## 📌 Sobre o projeto

O **CyberSafe** é um chatbot educacional desenvolvido para o Checkpoint 01 do Módulo 1 da FIAP.

O projeto utiliza técnicas de **LangChain, LCEL, memória gerenciada e Pydantic v2** para criar uma aplicação capaz de manter o contexto da conversa e também realizar análises estruturadas relacionadas à cibersegurança.

O chatbot foi desenvolvido localmente como um pacote Python, utilizando **Ollama Cloud** como modelo de linguagem.

---

## 🎯 Domínio

### Cibersegurança

O domínio escolhido para o projeto é **cibersegurança**, com foco em orientação e educação sobre situações relacionadas à segurança digital.

O CyberSafe foi pensado para usuários que desejam obter orientações iniciais sobre temas de segurança digital de maneira clara e educativa.

---

## 🧠 Principais funcionalidades

- 💬 Chatbot com memória de conversa
- 🔗 Pipeline utilizando **LangChain LCEL**
- 🤖 Integração com **ChatOllama**
- 🧩 Respostas estruturadas utilizando **Pydantic v2**
- 📝 System Prompt estruturado com XML tagging
- 🧠 Demonstração de **context rot**
- 📊 Contagem e comparação de tokens
- 🔬 Meta prompting para melhoria do system prompt
- 🖥️ Interface gráfica desenvolvida com **Gradio**

---

## ⚙️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| LangChain | Construção das chains |
| LCEL | Pipeline de processamento |
| Ollama Cloud | Modelo de linguagem |
| `gemma4:cloud` | Modelo utilizado |
| Pydantic v2 | Validação das saídas |
| Gradio | Interface do chatbot |
| tiktoken | Contagem de tokens |

---

## 📂 Estrutura do projeto

```text
CKP01_Chatbot_CyberSafe/
├── app/
│   ├── main.py
│   ├── chain.py
│   ├── memory_manager.py
│   ├── schemas.py
│   ├── context_rot.py
│   ├── prompts.py
│   └── config.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
