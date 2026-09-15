"""Diferencial opcional: meta prompting.

Usa o próprio modelo para sugerir melhorias no system prompt e registra
antes/depois para documentação do CKP01.
"""

from pathlib import Path

from .chain import create_llm
from .prompts import SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "meta_prompting_before_after.md"


def improve_prompt() -> str:
    llm = create_llm()
    instruction = f"""
Você é um revisor de prompt engineering. Melhore o system prompt abaixo para
um chatbot educacional de cibersegurança. Preserve o domínio, a persona,
as restrições de segurança e o uso de XML tagging. Não transforme o prompt
em instruções ofensivas.

PROMPT ATUAL:
{SYSTEM_PROMPT}

Retorne apenas a nova versão do system prompt.
"""
    response = llm.invoke(instruction)
    return getattr(response, "content", str(response))


if __name__ == "__main__":
    improved = improve_prompt()
    OUT.write_text(
        "# Meta Prompting — Antes e Depois\n\n"
        "## Antes\n\n```text\n"
        + SYSTEM_PROMPT
        + "\n```\n\n## Depois\n\n```text\n"
        + improved
        + "\n```\n",
        encoding="utf-8",
    )
    print(f"Comparação salva em: {OUT}")
