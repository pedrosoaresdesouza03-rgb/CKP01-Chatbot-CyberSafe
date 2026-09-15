"""Gerenciamento da memória conversacional.

Estratégia escolhida: ConversationBufferMemory.
Ela é adequada ao CKP01 porque preserva o histórico recente de forma literal,
facilitando uma conversa coerente em pelo menos 5 turnos. O custo de tokens
cresce com o histórico, por isso o projeto mede esse crescimento no módulo
context_rot.py.
"""

try:
    from langchain_classic.memory import ConversationBufferMemory
except ImportError:
    from langchain.memory import ConversationBufferMemory


def create_memory() -> ConversationBufferMemory:
    """Cria a única estratégia de memória exigida pelo CKP01: Buffer."""
    return ConversationBufferMemory(
        memory_key="history",
        input_key="input",
        return_messages=False,
    )


MEMORY_TYPE = "ConversationBufferMemory (Buffer)"
