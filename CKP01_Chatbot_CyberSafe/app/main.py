"""Ponto de entrada local do CyberSafe, com interface Gradio."""

import gradio as gr

from .chain import build_chat_chain, build_structured_chain

chat_chain = build_chat_chain()
structured_chain = build_structured_chain()


def respond(message: str, history: list[dict]) -> str:
    """Envia a mensagem para a ConversationChain com memória gerenciada."""
    if not message.strip():
        return "Digite uma mensagem."

    result = chat_chain.invoke({"input": message})
    return result["response"]


def analyze(message: str):
    """Executa a segunda chain LCEL e valida a saída com Pydantic v2."""
    if not message.strip():
        return {"erro": "Digite uma consulta para analisar."}

    result = structured_chain.invoke(
        {
            "consulta": message,
            "format_instructions": (
                "Retorne um JSON compatível com o schema fornecido pelo parser."
            ),
        }
    )
    return result.model_dump()


def reset_memory():
    """Limpa a memória do chatbot."""
    chat_chain.memory.clear()
    return "Memória limpa. A próxima mensagem inicia uma nova sessão."


with gr.Blocks(title="CyberSafe — CKP01") as demo:
    gr.Markdown(
        "# 🛡️ CyberSafe\n"
        "Chatbot educacional de cibersegurança — FIAP · CKP01\n\n"
        "Modelo obrigatório: **gemma4:cloud via Ollama Cloud**."
    )

    with gr.Tab("Chat com memória"):
        chatbot = gr.Chatbot(height=500)
        msg = gr.Textbox(
            label="Mensagem",
            placeholder="Ex.: O que é autenticação multifator?",
        )
        send = gr.Button("Enviar", variant="primary")
        clear = gr.Button("Limpar memória")
        status = gr.Markdown()

        def chat_ui(message, history):
            answer = respond(message, history)
            history = history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": answer},
            ]
            return "", history

        send.click(chat_ui, [msg, chatbot], [msg, chatbot])
        msg.submit(chat_ui, [msg, chatbot], [msg, chatbot])
        clear.click(reset_memory, outputs=status)

    with gr.Tab("Análise estruturada"):
        analysis_input = gr.Textbox(
            label="Consulta",
            placeholder="Digite uma dúvida para classificar.",
        )
        analysis_output = gr.JSON(label="AnaliseConsulta — Pydantic v2")
        analysis_button = gr.Button("Analisar")
        analysis_button.click(analyze, inputs=analysis_input, outputs=analysis_output)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
