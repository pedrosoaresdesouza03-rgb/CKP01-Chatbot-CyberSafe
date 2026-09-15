"""As duas chains do CKP01: conversa com memória e saída estruturada."""

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .config import MODEL_NAME, OLLAMA_API_KEY, OLLAMA_BASE_URL
from .memory_manager import create_memory
from .prompts import STRUCTURED_SYSTEM_PROMPT, SYSTEM_PROMPT
from .schemas import AnaliseConsulta

try:
    from langchain_ollama import ChatOllama
except ImportError as exc:
    raise ImportError(
        "Instale as dependências com: pip install -r requirements.txt"
    ) from exc

try:
    from langchain_classic.chains import ConversationChain
except ImportError:
    from langchain.chains import ConversationChain


def create_llm() -> ChatOllama:
    """Cria o ChatOllama usando exclusivamente gemma4:cloud."""
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        client_kwargs={"headers": {"Authorization": f"Bearer {OLLAMA_API_KEY}"}},
        temperature=0.2,
    )


def build_chat_chain(llm: ChatOllama | None = None):
    """Chain 1: ConversationChain + memória Buffer."""
    llm = llm or create_llm()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Histórico da conversa:\n{history}\n\nNova mensagem:\n{input}"),
        ]
    )

    memory = create_memory()
    return ConversationChain(
        llm=llm,
        prompt=chat_prompt,
        memory=memory,
        verbose=False,
    )


def build_structured_chain(llm: ChatOllama | None = None):
    """Chain 2: ChatPromptTemplate | ChatOllama | PydanticOutputParser."""
    llm = llm or create_llm()

    parser = PydanticOutputParser(pydantic_object=AnaliseConsulta)

structured_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", STRUCTURED_SYSTEM_PROMPT),
        (
            "human",
            "Analise esta consulta de cibersegurança:\n{consulta}\n\n"
            "{format_instructions}",
        ),
    ]
)

return structured_prompt | llm | parser

def build_text_chain(llm: ChatOllama | None = None):
    """Pipeline LCEL simples para texto, útil para testes do projeto."""
    llm = llm or create_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{consulta}"),
        ]
    )
    return prompt | llm | StrOutputParser()
