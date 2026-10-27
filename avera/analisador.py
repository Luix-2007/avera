"""Núcleo do Avera: envia a mensagem suspeita ao Claude e devolve a análise em JSON."""

import json
import os
import time
from pathlib import Path

import anthropic

RAIZ = Path(__file__).resolve().parent.parent
PROMPT_SISTEMA = (RAIZ / "prompt" / "system_prompt.md").read_text(encoding="utf-8")
MODELO = "claude-opus-5-5"
# Preço do Claude Opus 5.5 em US$ por token (US$ 4 e US$ 20 por milhão)
PRECO_ENTRADA = 4 / 1_000_000
PRECO_SAIDA = 20 / 1_000_000


def _carregar_env():
    """Lê ANTHROPIC_API_KEY de .env (na raiz) ou de avera/API_key.env, se existirem.

    Aceita linhas no formato ANTHROPIC_API_KEY=... ou só a chave (sk-ant-...).
    """
    for arquivo in (RAIZ / ".env", RAIZ / "avera" / "API_key.env"):
        if not arquivo.exists():
            continue
        for linha in arquivo.read_text(encoding="utf-8-sig").splitlines():
            linha = linha.strip().strip('"')
            if linha.startswith("sk-ant-"):
                os.environ.setdefault("ANTHROPIC_API_KEY", linha)
            elif linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                os.environ.setdefault(chave.strip(), valor.strip().strip('"'))


_carregar_env()
cliente = anthropic.Anthropic()

TEXTO_OU_NULO = {"anyOf": [{"type": "string"}, {"type": "null"}]}

ESQUEMA_RESPOSTA = {
    "type": "object",
    "properties": {
        "nivel_risco": {"type": "string", "enum": ["baixo", "medio", "alto"]},
        "sinais": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tipo": {"type": "string"},
                    "trecho": {"type": "string"},
                    "explicacao": {"type": "string"},
                },
                "required": ["tipo", "trecho", "explicacao"],
                "additionalProperties": False,
            },
        },
        "resposta_para_usuario": {"type": "string"},
        "acao_recomendada": {"type": "string"},
        "pergunta_verificacao": TEXTO_OU_NULO,
        "orientacao_pos_golpe": {
            "anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}]
        },
        "alertar_guardiao": {"type": "boolean"},
        "mensagem_para_guardiao": TEXTO_OU_NULO,
    },
    "required": [
        "nivel_risco",
        "sinais",
        "resposta_para_usuario",
        "acao_recomendada",
        "pergunta_verificacao",
        "orientacao_pos_golpe",
        "alertar_guardiao",
        "mensagem_para_guardiao",
    ],
    "additionalProperties": False,
}


def montar_entrada(mensagem: str, contexto: str = "", nome_usuario: str = "") -> str:
    partes = []
    if nome_usuario:
        partes.append(f"<nome_usuario>{nome_usuario}</nome_usuario>")
    if contexto:
        partes.append(f"<contexto>{contexto}</contexto>")
    partes.append(f"<mensagem_suspeita>\n{mensagem}\n</mensagem_suspeita>")
    return "\n".join(partes)


def analisar(mensagem: str, contexto: str = "", nome_usuario: str = "") -> dict:
    return analisar_com_detalhes(mensagem, contexto, nome_usuario)[0]


def analisar_com_detalhes(mensagem: str, contexto: str = "", nome_usuario: str = "") -> tuple[dict, dict]:
    """Devolve a análise e os dados técnicos da chamada (modelo, tempo, tokens, custo)."""
    inicio = time.perf_counter()
    resposta = cliente.beta.messages.create(
        model=MODELO,
        max_tokens=4000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=PROMPT_SISTEMA,
        output_config={
            "effort": "low",
            "format": {"type": "json_schema", "schema": ESQUEMA_RESPOSTA},
        },
        messages=[{"role": "user", "content": montar_entrada(mensagem, contexto, nome_usuario)}],
    )
    if resposta.stop_reason == "refusal":
        raise RuntimeError("O modelo recusou a análise desta mensagem.")
    texto = next(b.text for b in resposta.content if b.type == "text")
    entrada, saida = resposta.usage.input_tokens, resposta.usage.output_tokens
    detalhes = {
        "modelo": resposta.model,
        "segundos": round(time.perf_counter() - inicio, 1),
        "tokens_entrada": entrada,
        "tokens_saida": saida,
        "custo_usd": round(entrada * PRECO_ENTRADA + saida * PRECO_SAIDA, 4),
    }
    return json.loads(texto), detalhes
