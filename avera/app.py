"""Servidor web do Avera.

Com ANTHROPIC_API_KEY no .env, analisa qualquer mensagem com o Claude.
Sem chave, roda em modo demonstração com as respostas salvas dos 7 casos.

Uso: python avera/app.py  (abre em http://localhost:8000)
"""

import json
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA))
import analisador  # noqa: E402
from casos import CASOS  # noqa: E402

MODO_REAL = bool(os.environ.get("ANTHROPIC_API_KEY"))
RESPOSTAS_DEMO = json.loads((PASTA / "respostas_demo.json").read_text(encoding="utf-8"))

app = FastAPI(title="Avera")
app.mount("/static", StaticFiles(directory=PASTA / "static"), name="static")


class Pedido(BaseModel):
    mensagem: str
    contexto: str = ""
    nome_usuario: str = ""


def _normalizar(texto: str) -> str:
    return " ".join(texto.replace("[TRANSCRIÇÃO DE ÁUDIO]", "").split()).lower()


@app.get("/")
def pagina():
    return FileResponse(PASTA / "static" / "index.html")


@app.get("/api/status")
def status():
    return {
        "modo": "real" if MODO_REAL else "demonstracao",
        "exemplos": [
            {"nome": c["nome"], "mensagem": c["mensagem"], "contexto": c["contexto"]} for c in CASOS
        ],
    }


@app.post("/api/analisar")
def analisar(pedido: Pedido):
    if not pedido.mensagem.strip():
        raise HTTPException(400, "Mensagem vazia.")

    if MODO_REAL:
        try:
            return analisador.analisar(pedido.mensagem, pedido.contexto, pedido.nome_usuario)
        except Exception as erro:  # noqa: BLE001
            raise HTTPException(502, f"Não foi possível analisar agora: {erro}") from erro

    alvo = _normalizar(pedido.mensagem)
    for caso, resposta in zip(CASOS, RESPOSTAS_DEMO):
        if _normalizar(caso["mensagem"]) == alvo:
            return resposta
    raise HTTPException(
        404,
        "No modo demonstração, só os exemplos prontos podem ser analisados. "
        "Coloque uma chave da API no .env para analisar qualquer mensagem.",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
