"""Configuração central do projeto."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "app" / ".env")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
MODEL_NAME = "gemma4:cloud"
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "https://ollama.com")

if not OLLAMA_API_KEY:
    raise RuntimeError(
        "OLLAMA_API_KEY não encontrada. Crie um arquivo .env a partir de .env.example "
        "e informe sua chave do Ollama Cloud."
    )
