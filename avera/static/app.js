const NOME_USUARIO = "Maria";
const ROTULOS_RISCO = { alto: "🔴 Risco alto", medio: "🟡 Risco médio", baixo: "🟢 Risco baixo" };
const PREFIXO_AUDIO = "[TRANSCRIÇÃO DE ÁUDIO] ";

const conversa = document.getElementById("conversa");
const campo = document.getElementById("mensagem");
const contexto = document.getElementById("contexto");
const botaoEnviar = document.getElementById("enviar");
const botaoMicrofone = document.getElementById("microfone");
const statusChat = document.getElementById("status-chat");
const notificacoes = document.getElementById("notificacoes");

let veioDeAudio = false;

function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function adicionarBalao(html, tipo) {
  const balao = document.createElement("div");
  balao.className = `balao ${tipo}`;
  balao.innerHTML = html;
  conversa.appendChild(balao);
  conversa.scrollTop = conversa.scrollHeight;
  return balao;
}

function falar(texto) {
  if (!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const fala = new SpeechSynthesisUtterance(texto);
  fala.lang = "pt-BR";
  fala.rate = 0.95;
  const voz = speechSynthesis.getVoices().find((v) => v.lang === "pt-BR");
  if (voz) fala.voice = voz;
  speechSynthesis.speak(fala);
}

function mostrarAnalise(r) {
  let html = `<span class="risco ${r.nivel_risco}">${ROTULOS_RISCO[r.nivel_risco]}</span>\n`;
  html += escapar(r.resposta_para_usuario);
  html += `<br><button class="ouvir">🔊 Ouvir de novo</button>`;

  if (r.orientacao_pos_golpe) {
    html += `<details open><summary>O que fazer agora</summary><ol>`;
    html += r.orientacao_pos_golpe.map((p) => `<li>${escapar(p)}</li>`).join("");
    html += `</ol></details>`;
  }
  if (r.sinais.length) {
    html += `<details><summary>Por que desconfiei (${r.sinais.length})</summary><ul>`;
    html += r.sinais
      .map((s) => `<li><strong>${escapar(s.tipo)}</strong><span class="trecho">“${escapar(s.trecho)}”</span>${escapar(s.explicacao)}</li>`)
      .join("");
    html += `</ul></details>`;
  }
  if (r.pergunta_verificacao) {
    html += `<details><summary>Como conferir</summary><p>${escapar(r.pergunta_verificacao)}</p></details>`;
  }

  const balao = adicionarBalao(html, "recebido");
  balao.querySelector(".ouvir").addEventListener("click", () => falar(r.resposta_para_usuario));
  falar(r.resposta_para_usuario);

  if (r.alertar_guardiao && r.mensagem_para_guardiao) alertarGuardiao(r.mensagem_para_guardiao);
}

function alertarGuardiao(texto) {
  notificacoes.querySelector(".vazio")?.remove();
  const aviso = document.createElement("div");
  aviso.className = "notificacao";
  aviso.innerHTML = `<strong><span class="ponto"></span>AVERA · agora</strong>${escapar(texto)}`;
  setTimeout(() => notificacoes.prepend(aviso), 1200);
}

async function enviar() {
  const texto = campo.value.trim();
  if (!texto) return;
  const mensagem = veioDeAudio ? PREFIXO_AUDIO + texto : texto;
  const rotulo = veioDeAudio ? "🎤 Áudio encaminhado (transcrito)" : "↪ Encaminhada";
  adicionarBalao(`<span class="rotulo">${rotulo}</span>${escapar(texto)}`, "enviado");

  campo.value = "";
  veioDeAudio = false;
  botaoEnviar.disabled = true;
  statusChat.textContent = "analisando...";
  const digitando = adicionarBalao(`<span class="digitando">Avera está conferindo a mensagem...</span>`, "recebido");

  try {
    const resposta = await fetch("/api/analisar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem, contexto: contexto.value, nome_usuario: NOME_USUARIO }),
    });
    const dados = await resposta.json();
    digitando.remove();
    if (!resposta.ok) throw new Error(dados.detail || "Erro ao analisar.");
    mostrarAnalise(dados);
  } catch (erro) {
    digitando.remove();
    adicionarBalao(escapar(`Desculpe, não consegui conferir agora. ${erro.message}`), "recebido");
  } finally {
    botaoEnviar.disabled = false;
    statusChat.textContent = "online";
  }
}

function configurarMicrofone() {
  const Reconhecimento = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Reconhecimento) {
    botaoMicrofone.disabled = true;
    botaoMicrofone.title = "Gravação de áudio disponível no Google Chrome";
    return;
  }
  const rec = new Reconhecimento();
  rec.lang = "pt-BR";
  rec.interimResults = true;
  let gravando = false;

  rec.onresult = (e) => {
    campo.value = Array.from(e.results).map((r) => r[0].transcript).join("");
  };
  rec.onend = () => {
    gravando = false;
    botaoMicrofone.classList.remove("gravando");
    if (campo.value.trim()) veioDeAudio = true;
  };
  botaoMicrofone.addEventListener("click", () => {
    if (gravando) return rec.stop();
    campo.value = "";
    gravando = true;
    botaoMicrofone.classList.add("gravando");
    rec.start();
  });
}

// Escolhe a opção do seletor de origem que corresponde ao contexto de um exemplo
function indiceContexto(texto) {
  if (texto.includes("já fiz")) return 3;
  if (texto === "SMS") return 2;
  if (texto.includes("salvo")) return 1;
  return 0;
}

function relogio() {
  const agora = new Date();
  document.getElementById("hora").textContent = agora.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  document.getElementById("data").textContent = agora.toLocaleDateString("pt-BR", { weekday: "long", day: "numeric", month: "long" });
}

async function iniciar() {
  relogio();
  setInterval(relogio, 10000);
  configurarMicrofone();

  adicionarBalao(
    `Oi, ${NOME_USUARIO}! 👋 Recebeu alguma mensagem ou áudio estranho? Encaminhe aqui que eu confiro para você antes de qualquer Pix.`,
    "recebido"
  );

  const status = await (await fetch("/api/status")).json();
  const modo = document.getElementById("modo");
  modo.className = `modo ${status.modo}`;
  modo.textContent = status.modo === "real" ? "● IA ao vivo" : "● Modo demonstração";

  const lista = document.getElementById("lista-exemplos");
  status.exemplos.forEach((ex) => {
    const botao = document.createElement("button");
    botao.textContent = ex.nome;
    botao.addEventListener("click", () => {
      const audio = ex.mensagem.startsWith(PREFIXO_AUDIO);
      campo.value = audio ? ex.mensagem.slice(PREFIXO_AUDIO.length) : ex.mensagem;
      veioDeAudio = audio;
      contexto.selectedIndex = indiceContexto(ex.contexto);
      campo.focus();
    });
    lista.appendChild(botao);
  });
}

campo.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    enviar();
  }
});
botaoEnviar.addEventListener("click", enviar);
iniciar();
