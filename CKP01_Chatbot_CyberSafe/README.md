# CKP01 — Chatbot Profissional · CyberSafe

**Prompt Engineering & AI · FIAP · 2º Semestre 2026**

**Integrantes:**   
· PEDRO SOARES DE SOUZA (RM 571285)   
· JHON CUTILE TITIRICO (RM571976)   
· PAULO HENRIQUE LIRA BILAC DE ARAUJO (RM569496)   
· MATEUS DE OLIVEIRA FERNANDES NEVES (RM 572431)   
· OLAVO DADARIO VIANNA BARRETO (RM569272)     

## Domínio

**CyberSafe — educação em cibersegurança e fundamentos de defesa.**

### Por que este domínio?

Cibersegurança foi escolhida por ser um domínio real, amplo o suficiente para
evoluir nos próximos CKPs e adequado à aplicação de memória, RAG e agentes.
O chatbot do CKP01 foi construído de forma modular para que possa servir como
base do CKP02 (RAG) e como ferramenta do CKP03 (Agente).

### Usuários-alvo

- estudantes e iniciantes em tecnologia;
- pessoas que precisam aprender fundamentos de segurança;
- equipes em treinamento de conscientização;
- profissionais iniciantes que precisam revisar conceitos defensivos.

### Escopo e limites

O CyberSafe é educacional e defensivo. Ele explica conceitos e boas práticas,
mas não deve orientar ações de acesso indevido, evasão de controles ou dano a
sistemas. Essa restrição faz parte do system prompt.

## Arquitetura

O projeto implementa a arquitetura de **2 chains** solicitada no CKP01:

1. **Chain de conversa:** `ConversationChain + ConversationBufferMemory`
   para manter o histórico da conversa.
2. **Chain LCEL estruturada:**
   `ChatPromptTemplate | ChatOllama | PydanticOutputParser`
   para classificar e sintetizar uma consulta.

O modelo usado é exclusivamente **`gemma4:cloud` via Ollama Cloud**, com a
chave carregada de `.env`.

```text
Usuário
  │
  ├──────────────► ConversationChain
  │                    │
  │                    ├── ChatPromptTemplate
  │                    ├── ChatOllama (gemma4:cloud)
  │                    └── ConversationBufferMemory
  │
  └──────────────► Chain LCEL
                       │
                       ├── ChatPromptTemplate
                       ├── ChatOllama (gemma4:cloud)
                       └── PydanticOutputParser
                                  │
                                  ▼
                           AnaliseConsulta
```

## Requisitos atendidos

| Requisito | Status | Implementação |
|---|---|---|
| LangChain LCEL | ✅ | `app/chain.py` com operador `\|` |
| ChatOllama | ✅ | `ChatOllama` + `gemma4:cloud` |
| Ollama Cloud | ✅ | `OLLAMA_API_KEY` em `.env` |
| ChatPromptTemplate | ✅ | mensagens system/human com variáveis |
| 2 chains | ✅ | conversa com memória + pipeline LCEL estruturado |
| Memória gerenciada | ✅ | `ConversationBufferMemory` |
| 5+ turnos | ✅ | a interface mantém a mesma memória durante a sessão |
| Pydantic v2 | ✅ | `AnaliseConsulta` com 6 campos tipados |
| PydanticOutputParser | ✅ | integrado à chain LCEL |
| System prompt rico | ✅ | persona, objetivo, regras, domínio e formato |
| XML tagging | ✅ | `<persona>`, `<objetivo>`, `<regras>`, `<dominio>`, `<formato>` |
| Context rot | ✅ | `app/context_rot.py` com janelas crescentes |
| tiktoken | ✅ | contagem de tokens no benchmark |
| Domínio documentado | ✅ | esta seção |
| Projeto local | ✅ | pacote `app/`, sem Colab |
| `.env.example` | ✅ | presente; `.env` não deve ser enviado |
| Meta prompting | ⭐ +0,5 | `app/meta_prompting.py` |

## Justificativa da memória

Foi escolhida a **ConversationBufferMemory** porque o domínio é conversacional:
o estudante pode fazer uma sequência de perguntas sobre o mesmo assunto e
espera que o chatbot preserve o contexto anterior.

O Buffer guarda as mensagens de forma literal. Isso simplifica a implementação
e melhora a fidelidade do histórico, sendo adequado para uma conversa curta de
demonstração. O ponto negativo é o crescimento do número de tokens conforme
novos turnos são adicionados. Por isso, o projeto também mede tokens e
context rot.

Para a demonstração, realizar pelo menos **5 turnos** na aba "Chat com memória".
Uma sequência sugerida:

1. "Meu nome é [nome] e estou estudando segurança."
2. "Qual é o meu foco de estudo?"
3. "Explique autenticação multifator."
4. "Como isso se relaciona com meu estudo?"
5. "Resuma o que você sabe sobre o meu contexto nesta conversa."

## Pydantic v2

O schema `AnaliseConsulta` possui seis campos tipados:

- `categoria: str`
- `nivel: Literal[...]`
- `risco: Literal[...]`
- `objetivo: str`
- `resposta_curta: str`
- `recomendacao: str`

Há também validação com `field_validator` para impedir campos textuais vazios
e `extra="forbid"` para evitar campos inesperados.

A validação é feita por **`PydanticOutputParser`**, conforme solicitado no
enunciado.

## Context rot

O arquivo `app/context_rot.py` usa a mesma pergunta, o mesmo system prompt e
o mesmo contexto-alvo, alterando apenas a quantidade de informações
distratoras. As janelas padrão são **0, 5, 10 e 15 distratores**.

A métrica objetiva usada no exemplo verifica se a resposta preservou os dois
conceitos essenciais da resposta-alvo: **MFA** e **senha**.

Além da qualidade, `tiktoken` registra o número de tokens de cada janela.

### Como gerar a demonstração

Depois de configurar o `.env`:

```bash
python -m app.context_rot
```

O resultado será salvo em:

```text
context_rot_results.md
```

A tabela final deve ser incluída na documentação/README entregue, mostrando
as janelas crescentes e os resultados observados. A interpretação deve ser
feita com os dados reais produzidos pelo modelo, sem inventar resultados.

## Meta prompting — diferencial (+0,5)

O arquivo `app/meta_prompting.py` usa o próprio `gemma4:cloud` para propor uma
versão melhorada do system prompt, preservando o domínio e as restrições.

Execute:

```bash
python -m app.meta_prompting
```

Isso gera:

```text
meta_prompting_before_after.md
```

Na entrega, comparar o prompt original e o melhorado e explicar quais mudanças
foram feitas e por que elas podem melhorar consistência, clareza ou aderência
ao domínio.

## Como executar localmente

### 1. Criar e ativar um ambiente virtual

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar a chave

Copie:

```text
.env.example
```

para:

```text
.env
```

Depois informe sua chave:

```text
OLLAMA_API_KEY=sua_chave_aqui
```

**Nunca envie `.env` no ZIP.** O arquivo permitido na entrega é somente
`.env.example`.

### 4. Iniciar

```bash
python -m app.main
```

A interface Gradio ficará disponível em:

```text
http://localhost:7860
```

## Estrutura do projeto

```text
CKP01_Chatbot_CyberSafe/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── chain.py
│   ├── memory_manager.py
│   ├── schemas.py
│   ├── context_rot.py
│   ├── prompts.py
│   ├── config.py
│   └── meta_prompting.py
├── .env.example
├── requirements.txt
└── README.md
```

## Checklist antes de enviar

- [ ] Preencher nome completo e RM de todos os integrantes.
- [ ] Confirmar o domínio registrado pelo grupo.
- [ ] Criar `.env` localmente e testar a chave.
- [ ] Confirmar que `python -m app.main` inicia sem erros.
- [ ] Testar pelo menos 5 turnos de memória.
- [ ] Testar a aba de análise estruturada e conferir os 6 campos Pydantic.
- [ ] Executar `python -m app.context_rot`.
- [ ] Inserir os resultados reais do context rot no README.
- [ ] Executar `python -m app.meta_prompting` para o diferencial, se desejado.
- [ ] Conferir que `.env` NÃO está no ZIP.
- [ ] Enviar somente o arquivo ZIP pelo Teams, pelo líder.

## Relação com os próximos CKPs

O domínio e a modularização foram escolhidos para permitir continuidade:

**CKP01 → Chatbot profissional**

`CyberSafe + memória + saída estruturada`

**CKP02 → RAG**

`CyberSafe + base documental + recuperação de conhecimento`

**CKP03 → Agente**

`CyberSafe + RAG + ferramentas`

A decisão de domínio, portanto, não fica isolada neste checkpoint.
