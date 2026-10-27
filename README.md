# Avera

**Um assistente que usa IA para proteger idosos de golpes feitos com IA.**

Projeto desenvolvido para o desafio **#AIforImpact2026** (NAU / Junior Achievement Américas).

## O problema

Golpes como o do "falso parente" sempre existiram, mas a IA generativa os deixou muito mais convincentes: hoje é possível clonar a voz de um neto com poucos segundos de áudio e escrever mensagens sem nenhum erro. Idosos e pessoas com pouca familiaridade digital são os mais afetados, porque confiam na voz que conhecem e têm menos repertório para desconfiar. O resultado é perda financeira, vergonha (muitos nem denunciam) e perda de confiança no próprio celular.

## A solução

O Avera é um assistente no WhatsApp, onde essas pessoas já estão:

1. A pessoa **encaminha** a mensagem ou o áudio suspeito.
2. A IA **transcreve** o áudio e **analisa o padrão do golpe**: urgência, pedido de Pix, troca de número, pedido de segredo, chave em nome de terceiro, falsa autoridade.
3. O Avera responde **em áudio, em linguagem simples**, com uma ação concreta: ligar para o número antigo, fazer uma pergunta de verificação ou usar a palavra-segura da família.
4. Em risco alto, um **guardião** (familiar de confiança) recebe um alerta curto.
5. Se a pessoa **já pagou**, o Avera a acolhe e orienta: banco e devolução pelo MED, boletim de ocorrência, recuperação do WhatsApp.

### Por que IA, e quais são os limites

Um filtro de palavras-chave não entende contexto nem variações e não sabe explicar o risco de forma acolhedora. Um modelo de linguagem entende a mensagem, aponta o trecho exato que é suspeito e conversa por voz com quem não lê bem.

O Avera **não** tenta dizer se uma voz é real ou clonada, porque essa detecção ainda não é confiável. Ele analisa o **conteúdo e o padrão** da mensagem, que se repetem mesmo quando a voz é perfeita, e leva a pessoa a **verificar por outro canal**. Ele também não armazena as mensagens analisadas e nunca afirma que algo é "100% seguro".

## Estrutura

```
prompt/
  system_prompt.md     Prompt de sistema do Avera (regras, sinais, formato JSON)
  exemplos_teste.md    7 casos de teste com o resultado esperado
avera/
  analisador.py        Envia a mensagem ao Claude e devolve a análise em JSON
  testar_casos.py      Roda os 7 casos e verifica as respostas
```

## Como rodar

Requer Python 3.10+.

```bash
pip install -r requirements.txt
cp .env.example .env   # depois coloque sua chave da API da Anthropic no .env
python avera/testar_casos.py
```

## Tecnologias

- **Claude Opus 5.5** (API da Anthropic) com saída estruturada em JSON
- **Python** + **FastAPI**
- Web Speech API do navegador para transcrição e leitura em voz alta (interface em desenvolvimento)
