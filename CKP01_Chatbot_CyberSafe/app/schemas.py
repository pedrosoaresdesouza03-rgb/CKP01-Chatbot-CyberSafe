"""Schemas Pydantic v2 usados para validar saídas do modelo."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnaliseConsulta(BaseModel):
    """Representação estruturada de uma consulta do CyberSafe."""

    model_config = ConfigDict(extra="forbid")

    categoria: str = Field(description="Categoria principal da consulta.")
    nivel: Literal["iniciante", "intermediario", "avancado"] = Field(
        description="Nível técnico estimado da consulta."
    )
    risco: Literal["baixo", "moderado", "alto"] = Field(
        description="Classificação educacional de risco do conteúdo."
    )
    objetivo: str = Field(description="Objetivo aparente da consulta, sem presumir fatos.")
    resposta_curta: str = Field(description="Síntese curta do que deve ser respondido.")
    recomendacao: str = Field(description="Boa prática defensiva relacionada à consulta.")

    @field_validator("categoria", "objetivo", "resposta_curta", "recomendacao")
    @classmethod
    def texto_nao_vazio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode ficar vazio.")
        return value
