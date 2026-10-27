# Roteiro do vídeo – Avera (#AIforImpact2026)

**Duração-alvo:** 2:50 (o limite é 3:00; a folga cobre respiros e transições).
**Formato:** MP4, 16:9, 1920x1080, com áudio.
**Narração:** cerca de 360 palavras, num ritmo calmo.

Legenda das colunas: **Imagem** = o que aparece na tela. **Áudio** = o que se ouve. Os trechos entre colchetes são instruções, não são falados.

---

## 1. Gancho – o golpe (0:00–0:18)

**Imagem:** animação gerada por IA (cenas A, B e C do Higgsfield). Apartamento em Copacabana, fim de tarde. Dona Maria, uns 70 anos, recebe uma mensagem no celular, ouve o áudio, fica preocupada e abre o app do banco.

**Áudio:** a voz do "neto", **clonada por IA a partir da sua própria voz**:

> "Vó, sou eu, o Pedro! Meu celular caiu na água, esse é meu número novo. Preciso de um Pix de mil e oitocentos reais hoje, pra um amigo. E não conta pra mãe, tá?"

[Congelar a imagem com o dedo da Maria sobre o botão "Pagar". Corte seco para o silêncio.]

## 2. A revelação (0:18–0:28)

**Imagem:** você na câmera, ou a tela preta com o texto aparecendo.

**Texto na tela:** "Essa voz foi criada por IA."

**Narração:**
> Esse áudio não foi gravado por ninguém. Eu criei com inteligência artificial, a partir de poucos segundos da minha própria voz, em menos de cinco minutos.

## 3. O problema (0:28–0:55)

**Imagem:** você na câmera, intercalado com manchetes reais de golpes com voz clonada (prints de notícias) e o dado na tela.

**Narração:**
> Eu sou o Luiz, estudo Inteligência Artificial na PUC-Rio. O golpe do falso parente não é novo. O novo é que a IA deixou ele quase perfeito: a voz é igual e o texto não tem erro. [DADO COM FONTE, ver a seção "Pesquisar antes de gravar"]. Quem mais sofre são os idosos, que confiam na voz que conhecem e, muitas vezes, nem denunciam por vergonha.

## 4. A solução e a demo ao vivo (0:55–1:50)

**Imagem:** gravação de tela do Avera no Chrome, **num plano contínuo**, no modo **IA ao vivo**. Os dois celulares lado a lado.

**Narração (antes de gravar a voz):**
> Por isso eu criei o Avera: uma IA que protege as pessoas dos golpes feitos com IA. A Maria só precisa encaminhar o áudio suspeito. Vou simular isso agora, ao vivo, com a minha voz.

**Ação:** clique no 🎤 e **dite** a mensagem do golpe (a mesma do gancho). Selecione "De um número desconhecido" e envie.

[A análise leva uns 7 segundos. Na edição, acelere esse trecho e mostre "2x" no canto, para continuar honesto.]

**Narração (enquanto a resposta aparece):**
> Risco alto. O Avera explica em voz alta, em linguagem simples, por que desconfiar e o que fazer: não fazer o Pix e ligar para o número antigo do neto. E a Ana, filha da Maria e guardiã cadastrada, recebe um alerta na hora.

**Ação:** dê um zoom de 2 segundos no rodapé técnico (modelo, tempo, tokens, custo).

**Narração:**
> Nada aqui está pronto: cada resposta é gerada agora, por menos de três centavos de dólar.

[Deixe a voz do Avera lendo a resposta tocar por 2 ou 3 segundos antes da narração continuar.]

## 5. Como funciona (1:50–2:12)

**Imagem:** diagrama animado, com cada etapa surgindo da esquerda para a direita (ver "Diagrama de arquitetura" abaixo). Os nomes técnicos aparecem na tela; a narração fala do fluxo.

**Narração:**
> A voz é transcrita no próprio navegador e vai para o Claude, um modelo de linguagem da Anthropic, com instruções que eu escrevi e testei: doze sinais de golpe, três níveis de risco e respostas para quem não lê bem. E se a pessoa já fez o Pix, o Avera acolhe e orienta: falar com o banco e pedir a devolução pelo MED.

## 6. Por que IA, e os limites (2:12–2:32)

**Imagem:** volta para a interface. Mostre rapidamente o caso 6 (a mensagem que tenta enganar o Avera) com o sinal "Tentativa de enganar o Avera" destacado.

**Narração:**
> Um filtro de palavras não entende contexto, e o golpista muda as palavras. A IA entende a intenção, e percebe até quando a mensagem tenta enganar o próprio Avera. Mas ele não promete o impossível: não diz se uma voz é falsa, porque isso ainda não é confiável. Ele analisa o padrão, não guarda as mensagens e sempre manda conferir por outro caminho.

## 7. Próximos passos (2:32–2:48)

**Imagem:** mockup simples de uma notificação no celular: "Essa mensagem fala de Pix e número novo. Quer conferir no Avera?" Ao lado, um cadeado com o texto "Nada sai do seu celular".

**Narração:**
> O próximo passo é a integração oficial com o WhatsApp e um alerta opcional, que roda só no celular: ele percebe palavras como "Pix" e "número novo" e sugere conferir, sem ler nem enviar as conversas. Eu escolhi não monitorar tudo, porque proteger também é respeitar a privacidade.

## 8. Fechamento (2:48–2:55)

**Imagem:** cena D do Higgsfield (Maria sorrindo, ligando para o neto de verdade), com o logo do Avera por cima.

**Narração:**
> Avera. Antes do Pix, confere.

**Texto na tela:** logo do Avera + "github.com/Luix-2007/avera" + "#AIforImpact2026".

---

## Diagrama de arquitetura (seção 5)

Cinco caixas, ligadas por setas:

```
🎤 Áudio ou texto  →  Transcrição no navegador  →  Claude Opus 5.5  →  Análise em JSON  →  🔊 Voz + 🔔 Alerta ao guardião
                       (Web Speech API)            (prompt com 12      (risco, sinais,
                                                    sinais de golpe)    ação, verificação)
```

Embaixo, em letras menores: **Python · FastAPI · API do Claude · HTML/CSS/JS**.

---

## Cenas de animação para o Higgsfield

Gere **primeiro uma imagem de referência** da Dona Maria e use essa mesma imagem em todos os clipes, para que ela tenha o mesmo rosto em todas as cenas. Faça cada clipe com 5 a 8 segundos. Prompts em inglês costumam funcionar melhor nesses modelos.

**Imagem de referência:**
> Pixar-style 3D animation, a warm Brazilian grandmother in her 70s, short gray curly hair, glasses, floral blouse, sitting on a sofa in a cozy Copacabana apartment at golden hour, window with view of the beach, soft cinematic lighting

**Cena A – a mensagem chega:**
> The grandmother's smartphone buzzes on the coffee table, she picks it up and smiles seeing a notification, cozy apartment, golden hour, slow camera push-in

**Cena B – o áudio preocupa:**
> Close-up of the grandmother holding the phone to her ear, her smile fades into worry, she puts her hand on her chest, warm light, shallow depth of field

**Cena C – quase faz o Pix:**
> Over-the-shoulder shot of the grandmother opening a banking app on her phone, her finger hesitating over a payment button, tense mood, slow zoom

**Cena D – final feliz:**
> The grandmother laughing while on a phone call, relieved, sunset light through the window, the camera slowly pulls back

Isso dá **4 imagens/clipes**. Confira quantos créditos cada geração consome antes de começar, para não ficar sem créditos no meio. Se sobrar crédito, uma quinta cena com a Ana (a filha) recebendo o alerta no trabalho reforça a parte do guardião.

---

## Pesquisar antes de gravar

- **1 dado com fonte** para a seção 3. Boas fontes: Anuário Brasileiro de Segurança Pública (estelionatos), Febraban, ou uma notícia recente sobre golpes com voz clonada. Coloque a fonte na tela, em letras pequenas.
- **2 ou 3 manchetes reais** sobre golpes com voz clonada no Brasil, para os prints da seção 3.

---

## Checklist da gravação

- [ ] Clone **só a sua própria voz** para o gancho (por exemplo, no ElevenLabs) e mostre "voz gerada por IA" na tela na revelação.
- [ ] Grave a demo no **Google Chrome**, porque o microfone não funciona em todos os navegadores.
- [ ] Antes de gravar, troque o seletor para **IA ao vivo** e faça um teste de microfone.
- [ ] Feche abas e notificações do computador. **Nunca** abra o `.env` ou o `API_key.env` na tela.
- [ ] Grave a narração em um lugar silencioso, separada da tela, e sincronize na edição.
- [ ] Coloque legendas: muita gente assiste sem som, e isso também ajuda quem avalia.
- [ ] Antes de mostrar o link, torne o repositório do GitHub **público**.

## Checklist da entrega

- [ ] Duração **menor que 3:00**. Confira no player.
- [ ] MP4, 16:9, 1920x1080, até 500 MB.
- [ ] Nome do arquivo: `Luiz José Vieira da Cruz_Brasil_Video_#AIforImpact2026`
- [ ] Google Drive com a permissão **"Qualquer pessoa com o link pode visualizar"**.
- [ ] Teste o link numa **aba anônima** antes de enviar.
- [ ] Envie com folga, até umas 22h, para ter margem antes das 23:59.
