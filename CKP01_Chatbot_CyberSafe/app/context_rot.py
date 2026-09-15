"""Medição de contexto e demonstração de context rot.

A ideia é usar a mesma pergunta e a mesma instrução, variando apenas a
quantidade de contexto. O script conta tokens com tiktoken e, quando
executado com uma OLLAMA_API_KEY válida, pode comparar respostas.

O benchmark é deliberadamente reproduzível: cada janela contém a mesma
informação-alvo e diferentes blocos de contexto distrator.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import tiktoken

from .chain import create_llm
from .prompts import SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = ROOT / "context_rot_results.md"

QUESTION = (
    "Qual é a recomendação principal registrada no contexto-alvo para proteger "
    "uma conta de estudante?"
)

TARGET_CONTEXT = (
    "CONTEXTO-ALVO: A recomendação principal é ativar autenticação multifator "
    "(MFA) e usar uma senha única e forte."
)

DISTRACTORS = [
    "NOTA-EXTRA: backups devem ser testados periodicamente.",
    "NOTA-EXTRA: atualizações reduzem a exposição a vulnerabilidades conhecidas.",
    "NOTA-EXTRA: phishing costuma usar engenharia social.",
    "NOTA-EXTRA: princípio do menor privilégio reduz permissões desnecessárias.",
    "NOTA-EXTRA: redes públicas exigem atenção redobrada à privacidade.",
    "NOTA-EXTRA: gestores de senhas podem ajudar a manter credenciais únicas.",
    "NOTA-EXTRA: logs auxiliam investigação e monitoramento.",
    "NOTA-EXTRA: segmentação limita o impacto de alguns incidentes.",
    "NOTA-EXTRA: treinamento recorrente melhora conscientização.",
    "NOTA-EXTRA: políticas de senha devem ser simples e aplicáveis.",
    "NOTA-EXTRA: criptografia protege dados em trânsito e em repouso.",
    "NOTA-EXTRA: controle de acesso deve ser revisado.",
    "NOTA-EXTRA: dispositivos devem receber atualizações de segurança.",
    "NOTA-EXTRA: dados pessoais devem ser coletados com finalidade definida.",
    "NOTA-EXTRA: incidentes devem ser registrados para análise posterior.",
]


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Conta tokens com tiktoken."""
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))


def build_context(extra_items: int) -> str:
    items = DISTRACTORS[: max(0, min(extra_items, len(DISTRACTORS)))]
    return "\n".join([TARGET_CONTEXT, *items])


def evaluate_windows(windows: Iterable[int] = (0, 5, 10, 15)) -> list[dict]:
    """Executa a mesma tarefa com janelas crescentes."""
    llm = create_llm()
    rows = []

    for size in windows:
        context = build_context(size)
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"<contexto>\n{context}\n</contexto>\n\n"
            f"<pergunta>\n{QUESTION}\n</pergunta>"
        )
        response = llm.invoke(prompt)
        answer = getattr(response, "content", str(response))
        answer_lower = answer.lower()

        # Métrica simples e transparente: a resposta contém os dois conceitos-alvo?
        hits = int("mfa" in answer_lower) + int("senha" in answer_lower)
        quality = "adequada" if hits == 2 else "parcial" if hits == 1 else "inadequada"

        rows.append(
            {
                "distratores": size,
                "tokens": count_tokens(prompt),
                "qualidade": quality,
                "resposta": answer.replace("\n", " "),
            }
        )

    return rows


def save_results(rows: list[dict]) -> None:
    """Salva uma tabela Markdown para documentação da demonstração."""
    lines = [
        "# Resultado do Context Rot",
        "",
        "| Distratores | Tokens | Qualidade | Resposta |",
        "|---:|---:|---|---|",
    ]
    for row in rows:
        safe_answer = row["resposta"].replace("|", "/")
        lines.append(
            f"| {row['distratores']} | {row['tokens']} | "
            f"{row['qualidade']} | {safe_answer} |"
        )
    RESULTS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    rows = evaluate_windows()
    save_results(rows)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"Resultados salvos em: {RESULTS_FILE}")
