"""Roda os 7 casos de teste do prompt e compara o nível de risco com o esperado.

Uso: python avera/testar_casos.py
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analisador import analisar  # noqa: E402
from casos import CASOS, NOME  # noqa: E402


def rodar(caso):
    try:
        return caso, analisar(caso["mensagem"], caso["contexto"], NOME), None
    except Exception as erro:  # noqa: BLE001
        return caso, None, erro


def verificar(caso, r):
    problemas = []
    if r["nivel_risco"] not in caso["esperado"]:
        problemas.append(f"nível {r['nivel_risco']}, esperado {'/'.join(caso['esperado'])}")
    if r["alertar_guardiao"] != (r["nivel_risco"] == "alto"):
        problemas.append("alertar_guardiao incoerente com o nível")
    if r["alertar_guardiao"] and not r["mensagem_para_guardiao"]:
        problemas.append("faltou mensagem_para_guardiao")
    if r["nivel_risco"] != "baixo" and not r["pergunta_verificacao"]:
        problemas.append("faltou pergunta_verificacao")
    if caso.get("exige_pos_golpe") and not r["orientacao_pos_golpe"]:
        problemas.append("faltou orientacao_pos_golpe")
    if not caso.get("exige_pos_golpe") and r["orientacao_pos_golpe"]:
        problemas.append("orientacao_pos_golpe sem a pessoa ter pago")
    if "100%" in r["resposta_para_usuario"]:
        problemas.append("resposta diz 100%")
    return problemas


def main():
    with ThreadPoolExecutor(max_workers=7) as pool:
        resultados = list(pool.map(rodar, CASOS))

    aprovados = 0
    saida = []
    for caso, r, erro in resultados:
        print("=" * 70)
        print(caso["nome"])
        if erro:
            print(f"  ERRO: {erro}")
            continue
        problemas = verificar(caso, r)
        aprovados += not problemas
        print(f"  {'OK' if not problemas else 'FALHOU: ' + '; '.join(problemas)}")
        print(f"  Risco: {r['nivel_risco']} | Sinais: {', '.join(s['tipo'] for s in r['sinais']) or '-'}")
        print(f"  Resposta (voz): {r['resposta_para_usuario']}")
        print(f"  Verificação: {r['pergunta_verificacao']}")
        print(f"  Guardião: {r['mensagem_para_guardiao']}")
        if r["orientacao_pos_golpe"]:
            print("  Pós-golpe: " + " | ".join(r["orientacao_pos_golpe"]))
        saida.append({"caso": caso["nome"], "resultado": r, "problemas": problemas})

    print("=" * 70)
    print(f"{aprovados}/{len(CASOS)} casos aprovados")
    destino = Path(__file__).resolve().parent / "resultados_testes.json"
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Resultados completos em {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
