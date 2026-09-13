/**
 * DinDin web — a UI. Toda a economia vive no Python via Pyodide.
 * Este arquivo NAO sabe nenhuma regra do jogo: so desenha o que a bridge devolve.
 */
import { DindinEngine } from "./pyodide-bridge.js";
import { CENA_HERO, CENA_RELATORIO, CENA_FILA, cenaLocal, cenaRegiao } from "./svg-art.js";

const eng = new DindinEngine();
const $ = (s) => document.querySelector(s);
const el = (t, c, txt) => {
  const e = document.createElement(t);
  if (c) e.className = c;
  if (txt != null) e.textContent = txt;
  return e;
};

const ICONE = {
  escaldante: "🔥", quente: "☀️", abafado: "🥵",
  nublado: "☁️", chuva: "🌧️", temporal: "⛈️", frio: "🥶",
};

let estado = null, catalogo = null, carrinho = {}, producao = {},
    precos = {}, tempos = null, saboresDoDia = [];
// Idioma da interface. Nome do produto e girias ficam regionais sempre.
let lang = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "pt";
// "Modo bandeira": tema claro com a paleta da bandeira do Brasil. Lembrado
// entre sessoes; o padrao e o escuro (o tema original do redesenho).
let tema = localStorage.getItem("dindin-tema") === "claro" ? "claro" : "escuro";
document.documentElement.dataset.tema = tema;
// Regioes ja vencidas. Vive fora da partida (o estado do jogo morre no fim,
// a conquista fica), por isso mora aqui e nao no GameState.
let conquistas = carregarConquistas();

function carregarConquistas() {
  try {
    const cru = JSON.parse(localStorage.getItem("dindin-conquistas") ?? "[]");
    return Array.isArray(cru) ? cru.filter((k) => typeof k === "string") : [];
  } catch {
    return [];   // storage corrompido nao pode impedir o jogo de abrir
  }
}

function salvarConquistas(lista) {
  conquistas = lista;
  try {
    localStorage.setItem("dindin-conquistas", JSON.stringify(lista));
  } catch { /* modo privado/sem quota: joga sem guardar */ }
}
// null = ainda nao escolhido hoje; desenharGelo adota a sugestao do calor.
let gelo = null;
// Refaz a tela atual depois de trocar o tema. So telaDia/telaRelatorio tem
// cabecalho (com o botao de tema), entao so elas precisam se registrar aqui.
let redesenharTelaAtual = () => {};
// Contador de passos do dia: cartoes aparecem/somem conforme o local.
let passoN = 0;
const tit = (nome) => `${++passoN}. ${nome}`;

const money = (c) => {
  const s = c < 0 ? "-" : "";
  const v = Math.abs(c);
  return `${s}R$ ${Math.floor(v / 100).toLocaleString("pt-BR")},${String(v % 100).padStart(2, "0")}`;
};
const t = (k, vars) => {
  let s = catalogo?.textos?.[k] ?? k;
  if (vars) for (const [a, b] of Object.entries(vars)) s = s.replaceAll(`{${a}}`, b);
  return s;
};

/** Cabecalho de tabela com versao curta pro celular (evita quebra feia
 * de titulos como "Dá pra fazer" numa coluna estreita). CSS troca qual
 * das duas aparece por largura de tela. */
const rotuloCurto = (cheio, curto) =>
  `<span class="rotulo-cheio">${cheio}</span><span class="rotulo-curto">${curto}</span>`;

// ------------------------------------------------------------------ boot
/* No celular nao existe :hover, e o :focus em <span> e inconsistente no
 * iOS. Um toque no "?" alterna a classe .aberta; tocar fora fecha. */
document.addEventListener("click", (e) => {
  const alvo = e.target.closest?.(".ajuda");
  for (const a of document.querySelectorAll(".ajuda.aberta")) {
    if (a !== alvo) a.classList.remove("aberta");
  }
  if (alvo) { e.preventDefault(); alvo.classList.toggle("aberta"); }
});

async function boot() {
  const barra = $(".barra-dentro"), txt = $(".carga-txt");
  try {
    tempos = await eng.iniciar((msg, pct) => {
      txt.textContent = msg;
      barra.style.width = pct + "%";
    });
    $("#carregando").classList.add("sumindo");
    setTimeout(() => ($("#carregando").style.display = "none"), 400);
    telaRegioes();
  } catch (e) {
    txt.innerHTML = `<span style="color:#e8517a">Falhou: ${e.message}</span>`;
    console.error(e);
  }
}

// ------------------------------------------------------------------ telas
function telaRegioes() {
  redesenharTelaAtual = telaRegioes;
  // Textos neutros (sem sotaque regional) so pra tela de escolha.
  catalogo = { textos: eng.textosBase(lang) };
  const regioes = eng.regioes(lang, conquistas);
  const placar = eng.placarCampanha(conquistas);
  const app = $("#app");
  app.innerHTML = "";

  // O seletor de idioma + tema: controles fixos no topo da tela.
  const picker = el("div", "lang-picker");
  for (const [codigo, rotulo] of [["pt", "Português"], ["en", "English"]]) {
    const chip = el("button", "lang-chip" + (lang === codigo ? " ativa" : ""),
                    rotulo);
    chip.onclick = () => {
      if (lang === codigo) return;
      lang = codigo;
      const url = new URLSearchParams(location.search);
      if (lang === "en") url.set("lang", "en"); else url.delete("lang");
      history.replaceState({}, "", url.size ? `?${url}` : location.pathname);
      telaRegioes();
    };
    picker.append(chip);
  }
  picker.append(botaoTema());
  app.append(picker);

  const replLink = el("button", "repl-link", t("repl.menu_link"));
  replLink.onclick = telaRepl;
  app.append(replLink);

  // --- hero: titulo grande + cena de abertura
  const hero = el("div", "hero");
  const heroTexto = el("div", "hero-texto");
  heroTexto.innerHTML =
    `<div class="hero-eyebrow">${t("ui.subtitulo")}</div>
     <h1>${t("ui.escolha_regiao")}</h1>
     <p>${t("regiao.subtitulo")}</p>`;
  if (placar.quantas > 0) {
    const p = el("div", "campanha-placar" + (placar.zerou ? " zerou" : ""));
    p.textContent = placar.zerou
      ? t("campanha.zerou")
      : t("campanha.placar", { n: placar.quantas, total: placar.total });
    heroTexto.append(p);
  }
  const heroCena = el("div", "hero-cena");
  heroCena.innerHTML = CENA_HERO[tema] ?? CENA_HERO.escuro;
  hero.append(heroTexto, heroCena);
  app.append(hero);

  const grade = el("div", "grade-regioes");
  for (const r of regioes) {
    const b = el("button", "regiao" + (r.vencida ? " vencida" : ""));
    const cena = el("div", "cena-svg");
    cena.innerHTML = cenaRegiao(r.key, tema);
    if (r.vencida) {
      const selo = el("span", "selo-vencida");
      selo.title = t("campanha.vencida");
      selo.innerHTML =
        `<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true">
           <path d="M4 12.5 L9.5 18 L20 6.5" fill="none" stroke="currentColor"
                 stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
         </svg><span>${t("campanha.vencida")}</span>`;
      cena.append(selo);
    }
    const corpo = el("div", "corpo");
    corpo.innerHTML =
      `<div class="produto">${r.produto}</div>
       <div class="uf">${r.nome} · ${r.gentilico}</div>
       <div class="giria">"${r.giria.join('", "')}"</div>
       <div class="favs">${t("regiao.sai_muito")}: ${r.favoritos.map((f) => f.nome).join(", ")}</div>`;
    b.append(cena, corpo);
    b.onclick = () => comecar(r.key);
    grade.append(b);
  }
  app.append(grade);
  app.append(caixaBench());
}

function comecar(regiao) {
  const seed = Number(new URLSearchParams(location.search).get("seed"))
            || Math.floor(Math.random() * 1e6);
  estado = eng.novoJogo(regiao, seed);
  // Catalogo filtrado pelo progresso: dia 1 abre so 3 sabores.
  catalogo = eng.catalogo(regiao, estado.locais_desbloqueados, lang);
  history.replaceState({}, "",
    `?r=${regiao}&seed=${seed}${lang === "en" ? "&lang=en" : ""}`);
  telaDia();
}

// -------------------------------------------------------------------- repl
/* Console de Python de aprendizado. Roda no MESMO interprete Pyodide do
 * jogo, mas num namespace isolado (eng.rodarRepl) -- nao mexe no estado da
 * partida nem precisa dele. Existe pra dar ao curioso um lugar pra digitar
 * "2 + 2" e ver Python de verdade rodando no navegador, sem instalar nada. */
const REPL_EXEMPLOS = ["2 + 2", 'nome = "Ana"', "print(nome)", "for i in range(3):\n    print(i)"];
let replHistorico = [];   // linhas ja rodadas, mais recente por ultimo
let replIndiceHist = null; // posicao ao navegar com as setas; null = fora do historico
let replRascunho = "";     // o que o aluno estava digitando antes de apertar seta

function telaRepl() {
  redesenharTelaAtual = telaRepl;
  const app = $("#app");
  app.innerHTML = "";

  const topo = el("div", "lang-picker");
  const voltar = el("button", "lang-chip", `← ${t("ui.voltar")}`);
  voltar.onclick = telaRegioes;
  topo.append(voltar);
  topo.append(botaoTema());
  app.append(topo);

  const c = el("div", "cartao repl-cartao");
  c.append(el("h2", null, t("repl.titulo")));
  c.append(el("p", "sub", t("repl.subtitulo")));

  const tela = el("div", "repl-tela");
  tela.id = "repl-tela";
  c.append(tela);

  const linha = el("div", "repl-linha");
  const prompt = el("span", "repl-prompt", ">>>");
  const campo = el("textarea", "repl-input");
  campo.id = "repl-input";
  campo.placeholder = t("repl.placeholder");
  campo.rows = 1;
  campo.spellcheck = false;
  campo.autocapitalize = "off";
  campo.autocomplete = "off";
  const rodar = el("button", "principal", t("repl.rodar"));
  linha.append(prompt, campo, rodar);
  c.append(linha);

  const acoes = el("div", "repl-acoes");
  const limpar = el("button", "secundaria", t("repl.limpar"));
  const reiniciar = el("button", "secundaria", t("repl.reiniciar"));
  acoes.append(limpar, reiniciar);
  c.append(acoes);

  const ex = el("div", "repl-exemplos");
  ex.append(el("span", "rotulo", t("repl.exemplos_titulo")));
  for (const codigo of REPL_EXEMPLOS) {
    const chip = el("button", "repl-exemplo", codigo.split("\n")[0]);
    chip.onclick = () => { campo.value = codigo; ajustarAlturaRepl(campo); campo.focus(); };
    ex.append(chip);
  }
  c.append(ex);

  app.append(c);

  const executar = () => {
    const codigo = campo.value;
    if (!codigo.trim()) return;
    replHistorico.push(codigo);
    replIndiceHist = null;
    replRascunho = "";
    const { saida, erro } = eng.rodarRepl(codigo);
    replEcoar(codigo, saida, erro);
    campo.value = "";
    ajustarAlturaRepl(campo);
  };

  campo.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      executar();
      return;
    }
    if (e.key === "ArrowUp" && !codigoTemQuebraDeLinha(campo)) {
      if (!replHistorico.length) return;
      e.preventDefault();
      if (replIndiceHist === null) { replRascunho = campo.value; replIndiceHist = replHistorico.length; }
      replIndiceHist = Math.max(0, replIndiceHist - 1);
      campo.value = replHistorico[replIndiceHist];
      ajustarAlturaRepl(campo);
    } else if (e.key === "ArrowDown" && !codigoTemQuebraDeLinha(campo)) {
      if (replIndiceHist === null) return;
      e.preventDefault();
      replIndiceHist += 1;
      if (replIndiceHist >= replHistorico.length) {
        replIndiceHist = null;
        campo.value = replRascunho;
      } else {
        campo.value = replHistorico[replIndiceHist];
      }
      ajustarAlturaRepl(campo);
    }
  });
  campo.addEventListener("input", () => ajustarAlturaRepl(campo));
  rodar.onclick = executar;
  limpar.onclick = () => { tela.innerHTML = ""; };
  reiniciar.onclick = () => {
    eng.reiniciarRepl();
    tela.innerHTML = "";
    replLinha(tela, "aviso", t("repl.reiniciado"));
  };

  const versao = eng.versaoPython();
  replLinha(tela, "boas-vindas",
    t("repl.bem_vindo", { versao, exemplo: `<code>${REPL_EXEMPLOS[0]}</code>` }));
  const dica = el("div", "repl-dica");
  dica.textContent = t("repl.dica_setas");
  tela.append(dica);
  campo.focus();
}

/** true se o textarea tem mais de uma linha -- af, aí as setas devem mover
 * o cursor dentro do texto, nao navegar o historico. */
function codigoTemQuebraDeLinha(campo) {
  return campo.value.includes("\n");
}

function ajustarAlturaRepl(campo) {
  campo.style.height = "auto";
  campo.style.height = campo.scrollHeight + "px";
}

function replLinha(tela, cls, html) {
  const d = el("div", `repl-msg ${cls}`);
  d.innerHTML = html;
  tela.append(d);
  tela.scrollTop = tela.scrollHeight;
  return d;
}

/** Registra um comando + sua saida na tela, tipo scrollback de terminal. */
function replEcoar(codigo, saida, erro) {
  const tela = $("#repl-tela");
  if (!tela) return;
  const bloco = el("div", "repl-bloco");
  const linhas = codigo.split("\n");
  bloco.innerHTML = linhas
    .map((l, i) => `<div class="repl-echo"><span class="repl-prompt">${
      i === 0 ? "&gt;&gt;&gt;" : "..."}</span><code>${escaparHtml(l)}</code></div>`)
    .join("");
  if (saida) {
    const out = el("pre", "repl-saida");
    out.textContent = saida.replace(/\n$/, "");
    bloco.append(out);
  }
  if (erro) {
    const out = el("pre", "repl-erro");
    out.textContent = erro;
    bloco.append(out);
  }
  tela.append(bloco);
  tela.scrollTop = tela.scrollHeight;
}

function escaparHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function cabecalho(clima) {
  const h = el("header");
  h.append(el("div", "marca", `DinDin · ${catalogo.produto.plur}`));
  const s = el("div", "stats");
  const add = (rot, val) => {
    const d = el("div", "stat");
    d.append(el("b", null, val), el("span", null, rot));
    s.append(d);
  };
  const c = clima ?? eng.previsao(estado);
  const dClima = el("div", "stat stat-clima");
  dClima.innerHTML =
    `<b><span class="icone">${ICONE[c.kind] ?? "☀️"}</span>${Math.round(c.temp_c)}°C</b>
     <span>${t("clima." + c.kind)}</span>`;
  s.append(dClima);
  add(t("ui.dia"), estado.dia);
  add(t("ui.caixa"), money(estado.caixa));
  add(t("ui.fama"), Math.round(estado.reputacao));
  add(t("ui.ponto"), t(`local.${estado.local_atual}`));
  h.append(s);
  h.append(botaoTema());
  return h;
}

/** Alterna entre o tema escuro (padrao) e o "modo bandeira" (claro). */
function botaoTema() {
  const b = el("button", "tema-toggle",
    tema === "claro" ? t("ui.modo_noite") : t("ui.modo_bandeira"));
  b.onclick = alternarTema;
  return b;
}

function alternarTema() {
  tema = tema === "claro" ? "escuro" : "claro";
  localStorage.setItem("dindin-tema", tema);
  document.documentElement.dataset.tema = tema;
  redesenharTelaAtual();
}

function telaDia() {
  redesenharTelaAtual = telaDia;
  const clima = eng.previsao(estado);
  carrinho = {}; producao = {}; precos = {}; gelo = null; passoN = 0;
  saboresDoDia = eng.sabores(estado, {}, {}, lang);

  const app = $("#app");
  app.innerHTML = "";
  app.append(cabecalho(clima));

  // --- tira de pontos: onde a campanha ja te deixa vender
  app.append(tiraDePontos());

  const layout = el("div", "dia-layout");
  const coluna = el("div", "dia-coluna");
  layout.append(coluna);

  // --- plano do dia: onde voce esta + como esta o tempo
  const pl = el("div", "cartao");
  pl.append(el("h2", null,
    `${t("ui.dia")} ${estado.dia} · ${t("local." + estado.local_atual)}`));
  pl.append(el("p", "sub", t("ui.antes")));
  const plGrid = el("div", "plano-grid");
  const cena = el("div", "cena-svg cena");
  cena.innerHTML = cenaLocal(estado.local_atual, tema, estado.regiao);
  const local0 = catalogo.locais.find((l) => l.key === estado.local_atual);
  const falta = Math.max(0, local0.meta - estado.caixa);
  const resumo = el("div", "plano-resumo");
  resumo.innerHTML =
    `<div><span>${t("ui.no_caixa")}</span><b>${money(estado.caixa)}</b></div>
     <div><span>${t("ui.meta_curta")}</span><b>${money(local0.meta)}</b>${falta
       ? ` <i>${t("ui.faltam", { v: money(falta) })}</i>`
       : ` <i class="ok">${t("ui.meta_batida")}</i>`}</div>
     <div><span>${t("ui.sabores")}</span><b>${catalogo.sabores.length}</b></div>
     <div><span>${t("ui.congelado")}</span><b>${
       Object.values(estado.inventario.prontos ?? {}).reduce((a,b)=>a+b,0)}</b></div>`;
  plGrid.append(cena, resumo);
  pl.append(plGrid);
  pl.append(el("div", "aviso", t(`dica.${estado.local_atual}`)));
  coluna.append(pl);

  // --- clima + o que sai bem nessa regiao
  const cc = el("div", "cartao");
  cc.append(el("h2", null, t("ui.clima_amanha")));
  const cl = el("div", "clima");
  cl.innerHTML =
    `<div class="icone">${ICONE[clima.kind] ?? "☀️"}</div>
     <div>
       <div class="temp">${Math.round(clima.temp_c)}°C</div>
       <div class="desc">${t("clima." + clima.kind)} · ${t("clima.sensacao")} ${Math.round(clima.heat_index)}°C</div>
       <div class="dica" style="color:${dicaCor(clima)}">${dicaTexto(clima)}</div>
     </div>`;
  cc.append(cl);
  const favoritos = [...catalogo.sabores]
    .sort((a, b) => b.preferencia - a.preferencia)
    .slice(0, 3);
  if (favoritos.length) {
    cc.append(el("div", "favs-regiao",
      `${t("regiao.sai_muito")}: ${favoritos.map((f) => f.nome).join(", ")}`));
  }
  coluna.append(cc);

  // --- isopor (equipamento, antes de gastar na feira)
  const iso = cartaoIsopor();
  if (iso) coluna.append(iso);
  // --- feira
  coluna.append(cartaoFeira());
  // --- cozinha
  coluna.append(cartaoCozinha());
  // --- preco (com o grafico)
  coluna.append(cartaoPreco(saboresDoDia));
  // --- gelo (depende do quanto foi produzido)
  const gl = cartaoGelo();
  if (gl) coluna.append(gl);
  // Monta a tabela ja: esperar timeout deixava a cozinha vazia num primeiro frame.
  recarregarCozinha();

  layout.append(sidebarDia(local0));
  app.append(layout);
}

/** Tira de status: onde a progressao ja libera vender, ponto atual em destaque. */
function tiraDePontos() {
  const c = el("div", "cartao pontos-tira");
  c.append(el("span", "rotulo", t("ui.ponto")));
  const lista = el("div", "lista");
  for (const l of catalogo.locais) {
    const liberado = estado.locais_desbloqueados.includes(l.key);
    const atual = l.key === estado.local_atual;
    const chip = el("span", "ponto-chip" +
      (atual ? " atual" : liberado ? "" : " bloqueado"));
    chip.innerHTML = `${l.nome}` +
      (atual ? ` <span class="tag">${t("ui.dia")} ${estado.dia}</span>` : "");
    lista.append(chip);
  }
  c.append(lista);
  return c;
}

/** Resumo fixo do dia + botao de vender, ao lado dos cartoes na tela larga. */
function sidebarDia(local0) {
  const sb = el("div", "sidebar-dia");
  sb.id = "sidebar-dia";
  sb.append(el("div", "eyebrow", t("dia.resumo_titulo")));
  const corpo = el("div");
  corpo.id = "sidebar-dia-corpo";
  sb.append(corpo);
  const vender = el("button", "principal", t("ui.vender"));
  vender.onclick = rodarDia;
  sb.append(vender);
  setTimeout(atualizarSidebarDia, 0);
  return sb;
}

/** Refaz os totais da barra lateral com o que ja foi decidido no dia. */
function atualizarSidebarDia() {
  const corpo = $("#sidebar-dia-corpo");
  if (!corpo) return;
  const local0 = catalogo.locais.find((l) => l.key === estado.local_atual);
  const custoFeira = custoCarrinho();
  const unidades = unidadesDoDia();
  const sacos = gelo ?? 0;
  const precoSaco = estado.local_atual === "casa" ? 0
    : eng.infoDoGelo(estado, unidades).preco_saco;
  const custoGelo = sacos * precoSaco;
  const sobra = estado.caixa - custoFeira - custoGelo;

  corpo.innerHTML = "";
  const linha = (rot, val) => {
    const d = el("div", "linha");
    d.innerHTML = `<span>${rot}</span><b>${val}</b>`;
    corpo.append(d);
  };
  linha(t("dia.resumo_feira"), money(custoFeira));
  if (estado.local_atual !== "casa") linha(t("dia.resumo_gelo"), money(custoGelo));
  linha(t("dia.resumo_vai"), unidades);
  linha(t("dia.resumo_sobra"), money(sobra));
  corpo.append(el("div", "nota", t(`dica.${estado.local_atual}`)));
  const meta = Math.min(100, Math.round(100 * estado.caixa / local0.meta));
  const bm = el("div", "barra-meta");
  bm.innerHTML = `<i style="width:${meta}%"></i>`;
  corpo.append(bm);
}

function dicaCor(c) {
  if (["chuva", "temporal", "frio"].includes(c.kind)) return "#3b9edb";
  if (c.heat_index > 34) return "#f5c518";
  return "#2fa84f";
}
function dicaTexto(c) {
  if (["temporal", "chuva", "frio"].includes(c.kind)) return t(`clima.dica.${c.kind}`);
  if (c.heat_index > 34) return t("clima.dica.calorao");
  if (c.heat_index > 30) return t("clima.dica.bom");
  return t("clima.dica.normal");
}

/* ---------------------------------------------------------------- isopor
 * Fora de casa o isopor e equipamento: compra unica que dura N dias e
 * define capacidade e derretimento. Sem ele nao da pra vender na rua.
 */
function cartaoIsopor() {
  const info = eng.isopores(estado, lang);
  // Em casa o freezer resolve: nao precisa de isopor nem faz sentido mostrar.
  if (estado.local_atual === "casa" && !info.atual) return null;

  const c = el("div", "cartao");
  c.append(el("h2", null, tit(t("ui.isopor"))));

  if (info.atual && !info.precisa) {
    const atual = info.opcoes.find((o) => o.key === info.atual);
    const urgente = info.acabando ? " atencao" : "";
    const box = el("div", "isopor-atual" + urgente);
    box.innerHTML =
      `<div><span>${t("isopor.em_uso")}</span><b>${atual?.nome ?? info.atual}</b></div>
       <div><span>${t("isopor.dura_mais")}</span><b>${
         t("isopor.dias_valor", { n: info.dias_restantes })}</b></div>
       <div><span>${t("isopor.capacidade")}</span><b>${atual?.capacidade ?? "-"}</b></div>`;
    c.append(box);
    if (info.acabando) {
      c.append(el("div", "aviso", t("isopor.acabando")));
    } else {
      return c;   // ainda bom: nao polui a tela com a vitrine
    }
  } else {
    c.append(el("p", "sub", t("isopor.precisa")));
  }

  const grade = el("div", "isopor-grade");
  for (const o of info.opcoes) {
    const card = el("div", "isopor-op" + (o.pode ? "" : " sem-grana"));
    card.innerHTML =
      `<b>${o.nome}</b>
       <div class="preco">${money(o.custo)}</div>
       <div class="det">${t("isopor.det1", { dias: o.dias, cap: o.capacidade })}</div>
       <div class="det">${t("isopor.det2", { custo: money(o.custo_por_dia),
         pct: Math.round(o.derretimento * 100) })}</div>
       <div class="desc">${o.descricao}</div>`;
    const b = el("button", o.pode ? "" : "desligado",
                 o.pode ? t("ui.comprar") : t("ui.falta_dinheiro"));
    b.disabled = !o.pode;
    if (o.pode) {
      b.onclick = () => {
        const out = eng.comprarIsopor(estado, o.key);
        if (out.ok) { estado = out.estado; telaDia(); }
      };
    }
    card.append(b);
    grade.append(card);
  }
  c.append(grade);
  return c;
}

function cartaoFeira() {
  const c = el("div", "cartao");
  c.append(el("h2", null, tit(t("feira.titulo"))));
  c.append(el("p", "sub", t("feira.desconto")));
  const tab = el("table", "tab-feira");
  tab.innerHTML = `<thead><tr><th>${t("feira.insumo")}</th><th>${t("feira.unidade")}</th>
    <th class="num">${t("feira.preco")}</th><th class="num">${t("feira.tem")}</th>
    <th>${t("feira.levar")}</th></tr></thead>`;
  const tb = el("tbody");
  for (const i of catalogo.insumos) {
    const tr = el("tr");
    const tem = estado.inventario.ingredientes[i.key] ?? 0;
    tr.innerHTML = `<td>${i.nome}</td><td style="color:var(--dim)">${i.unidade}</td>
      <td class="num">${money(i.preco)}</td>
      <td class="num" style="color:var(--dim)">${(+tem).toFixed(1)}</td>`;
    const td = el("td");
    td.append(passo(() => carrinho[i.key] ?? 0, (v) => {
      if (v > 0) carrinho[i.key] = v; else delete carrinho[i.key];
      atualizarTotalFeira();
      recarregarCozinha();
    }));
    tr.append(td);
    tb.append(tr);
  }
  tab.append(tb);
  c.append(tab);
  const tot = el("div", "aviso");
  tot.id = "total-feira";
  c.append(tot);
  setTimeout(atualizarTotalFeira, 0);
  return c;
}

function custoCarrinho() {
  let total = 0;
  for (const [k, q] of Object.entries(carrinho)) {
    const i = catalogo.insumos.find((x) => x.key === k);
    let fator = 1;
    for (const b of i.bulk) if (q >= b.min) fator = b.fator;
    total += Math.round(i.preco * fator) * q;
  }
  return total;
}

function atualizarTotalFeira() {
  const box = $("#total-feira");
  if (!box) return;
  const custo = custoCarrinho();
  const sobra = estado.caixa - custo;
  box.innerHTML = sobra < 0
    ? `<b style="color:var(--rosa)">${t("feira.falta", { v: money(-sobra) })}</b>`
    : t("feira.resumo", { c: `<b>${money(custo)}</b>`, s: `<b>${money(sobra)}</b>` });
  const btn = document.querySelector("button.principal");
  if (btn) btn.disabled = sobra < 0;
  atualizarSidebarDia();
}

function cartaoCozinha() {
  const c = el("div", "cartao");
  c.append(el("h2", null, tit(t("cozinha.titulo"))));
  c.append(el("p", "sub", t("cozinha.subtitulo")));
  const tab = el("table", "tab-cozinha");
  tab.innerHTML = `<thead><tr><th>${t("cozinha.sabor")}</th>
    <th class="num">${t("preco.custo")}</th>
    <th class="num">${rotuloCurto(t("cozinha.maximo"), t("cozinha.maximo_curto"))}</th>
    <th class="num">${t("cozinha.pronto_curto")}</th>
    <th>${t("cozinha.produzir")}</th></tr></thead>`;
  tab.append(el("tbody", null, ""));
  tab.querySelector("tbody").id = "corpo-cozinha";
  c.append(tab);
  c.append(el("p", "sub", t("cozinha.cabe", { n: estado.capacidade_freezer })));
  return c;
}

/** Refaz a tabela da cozinha contando o que esta no carrinho da feira. */
function recarregarCozinha() {
  const tb = document.querySelector("#corpo-cozinha");
  if (!tb) return;
  saboresDoDia = eng.sabores(estado, carrinho, producao, lang);
  tb.innerHTML = "";

  for (const s of saboresDoDia) {
    const max = s.pode_produzir;
    // Nao deixa pedir mais do que da: evita "fiz 40" e sair 12.
    if ((producao[s.key] ?? 0) > max) {
      if (max > 0) producao[s.key] = max; else delete producao[s.key];
    }
    const tr = el("tr");
    const podeCor = max > 0 ? "var(--verde)" : "var(--dim)";
    tr.innerHTML = `<td>${s.nome}${s.tier === "gourmet"
        ? ' <span style="color:var(--rosa);font-size:11px">gourmet</span>' : ""}
        <span class="ajuda" tabindex="0">?<span class="balao">${dicaReceita(s)}</span></span></td>
      <td class="num">${money(s.custo)}</td>
      <td class="num" style="color:${podeCor};font-weight:700">${max}</td>
      <td class="num">${s.pronto || "—"}</td>`;
    const td = el("td");
    td.append(passo(() => producao[s.key] ?? 0, (v) => {
      const lim = Math.min(v, s.pode_produzir);
      if (lim > 0) producao[s.key] = lim; else delete producao[s.key];
      // Insumo e compartilhado: mexer num sabor muda o teto dos outros.
      recarregarCozinha();
    }, 5, () => s.pode_produzir));
    tr.append(td);
    tb.append(tr);
  }
  montarPreco(saboresDoDia);
  atualizarSidebarDia();
}

/** Texto do tooltip: o que precisa pra fazer 10 unidades. */
function dicaReceita(s) {
  const de = lang === "en" ? "of" : "de";
  const linhas = s.receita.map((r) => {
    const falta = r.tem < r.por_dez / 10;
    const cor = falta ? "var(--rosa)" : "var(--verde)";
    return `<span style="color:${cor}">${r.por_dez} ${r.unidade} ${de} ${r.nome}</span>` +
           `<span style="color:var(--dim)"> ${t("cozinha.tem", { n: r.tem })}</span>`;
  });
  const cab = `<b>${t("cozinha.pra10", { plur: catalogo.produto.plur })}</b>`;
  const rodape = s.faltando.length
    ? `<div style="color:var(--rosa);margin-top:6px">${t("cozinha.falta", { lista: s.faltando.join(", ") })}</div>`
    : `<div style="color:var(--verde);margin-top:6px">${t("cozinha.tem_tudo")}</div>`;
  return `${cab}<br>${linhas.join("<br>")}${rodape}`;
}

function passo(get, set, delta = 1, getMax = null) {
  const d = el("div", "passo");
  const menos = el("button", null, "−"), mais = el("button", null, "+");
  const v = el("span", "v", String(get()));
  const sync = () => {
    v.textContent = get();
    if (getMax) mais.disabled = get() >= getMax();
  };
  menos.onclick = () => { set(Math.max(0, get() - delta)); sync(); };
  mais.onclick = () => {
    const alvo = get() + delta;
    set(getMax ? Math.min(alvo, getMax()) : alvo);
    sync();
  };
  sync();
  d.append(menos, v, mais);
  return d;
}

// --- o cartao de preco: aqui mora o grafico que o terminal nao conseguia fazer
function cartaoPreco(sabores) {
  const c = el("div", "cartao");
  c.id = "cartao-preco";
  c.append(el("h2", null, tit(t("preco.titulo"))));
  c.append(el("p", "sub", t("preco.curva")));
  c.append(el("div", null, "").id = "");
  const alvo = el("div");
  alvo.id = "area-preco";
  c.append(alvo);
  setTimeout(() => montarPreco(sabores), 0);
  return c;
}

function montarPreco(sabores) {
  const area = $("#area-preco");
  if (!area) return;
  const ativos = Object.keys(producao).filter((k) => producao[k] > 0);
  const prontos = Object.keys(estado.inventario.prontos ?? {});
  const lista = [...new Set([...ativos, ...prontos])];

  if (!lista.length) {
    area.innerHTML = `<p style="color:var(--dim);font-size:13px">
      ${t("preco.vazio")}</p>`;
    return;
  }
  area.innerHTML = "";
  for (const key of lista) {
    const s = sabores.find((x) => x.key === key);
    if (!s) continue;
    if (precos[key] == null) precos[key] = s.preco_ref;
    area.append(blocoPreco(s));
  }
}

function blocoPreco(s) {
  const curva = eng.curvaDePreco(estado, s.key);
  const box = el("div");
  box.style.marginBottom = "22px";

  const topo = el("div");
  topo.style.cssText = "display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px";
  topo.innerHTML = `<b>${s.nome}</b>
    <span style="font-size:12px;color:var(--dim)">${t("preco.custo").toLowerCase()} ${money(curva.custo)} ·
    ${t("preco.melhor")} <b style="color:var(--verde)">${money(curva.melhor_preco)}</b></span>`;
  box.append(topo);

  const svgBox = el("div", "grafico-caixa");
  svgBox.append(desenharCurva(curva, () => precos[s.key]));
  box.append(svgBox);

  const linha = el("div", "slider-linha");
  const range = el("input");
  range.type = "range";
  range.min = 50; range.max = 900; range.step = 10;
  range.value = precos[s.key];
  const val = el("b", null, money(precos[s.key]));
  val.style.minWidth = "84px";
  const info = el("span");
  info.style.cssText = "font-size:12px;color:var(--dim);min-width:120px";

  const refresh = () => {
    precos[s.key] = +range.value;
    val.textContent = money(precos[s.key]);
    const p = curva.pontos.reduce((a, b) =>
      Math.abs(b.preco - precos[s.key]) < Math.abs(a.preco - precos[s.key]) ? b : a);
    const margem = precos[s.key] - curva.custo;
    info.innerHTML = `${t("preco.compram", { pct: Math.round(p.resposta * 100) })}
      <b style="color:${margem > 0 ? "var(--verde)" : "var(--rosa)"}">${money(margem)}</b>`;
    svgBox.innerHTML = "";
    svgBox.append(desenharCurva(curva, () => precos[s.key]));
  };
  range.oninput = refresh;
  linha.append(range, val, info);
  box.append(linha);
  setTimeout(refresh, 0);
  return box;
}

/** Curva de demanda + lucro em SVG. O termometro do terminal virando grafico. */
function desenharCurva(curva, getPreco) {
  const W = 640, H = 190, PAD = 34;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.style.cssText = "width:100%;height:auto;display:block";

  const ps = curva.pontos.filter((p) => p.preco <= 800);
  const xmin = ps[0].preco, xmax = ps[ps.length - 1].preco;
  const maxLucro = Math.max(...ps.map((p) => p.lucro_rel), 1);
  const X = (p) => PAD + ((p - xmin) / (xmax - xmin)) * (W - PAD * 2);
  const Yr = (r) => H - PAD - r * (H - PAD * 2);
  const Yl = (l) => H - PAD - (l / maxLucro) * (H - PAD * 2);

  const mk = (n, at) => {
    const e = document.createElementNS("http://www.w3.org/2000/svg", n);
    for (const [k, v] of Object.entries(at)) e.setAttribute(k, v);
    return e;
  };

  svg.append(mk("line", { x1: PAD, y1: H - PAD, x2: W - PAD, y2: H - PAD,
                          stroke: "#3a322c", "stroke-width": 1 }));

  // area de lucro
  const dLucro = ps.map((p, i) => `${i ? "L" : "M"}${X(p.preco)},${Yl(p.lucro_rel)}`).join("");
  svg.append(mk("path", {
    d: `${dLucro}L${X(ps[ps.length-1].preco)},${H-PAD}L${X(xmin)},${H-PAD}Z`,
    fill: "rgba(47,168,79,.16)",
  }));
  svg.append(mk("path", { d: dLucro, fill: "none", stroke: "#2fa84f", "stroke-width": 2 }));

  // curva de quem compra
  const dResp = ps.map((p, i) => `${i ? "L" : "M"}${X(p.preco)},${Yr(p.resposta)}`).join("");
  svg.append(mk("path", { d: dResp, fill: "none", stroke: "#3b9edb",
                          "stroke-width": 2, "stroke-dasharray": "5 4" }));

  // custo
  svg.append(mk("line", { x1: X(curva.custo), y1: PAD - 12, x2: X(curva.custo),
    y2: H - PAD, stroke: "#e8517a", "stroke-width": 1.5, "stroke-dasharray": "3 3" }));

  // melhor preco
  const mx = X(curva.melhor_preco), my = Yl(maxLucro);
  svg.append(mk("path", {
    d: `M${mx},${my-7}L${mx+7},${my}L${mx},${my+7}L${mx-7},${my}Z`,
    fill: "#f5c518",
  }));

  // preco atual
  const atual = getPreco();
  if (atual) {
    svg.append(mk("line", { x1: X(atual), y1: PAD - 12, x2: X(atual), y2: H - PAD,
                            stroke: "#f28c28", "stroke-width": 2.5 }));
  }

  for (const p of [100, 300, 500, 700]) {
    const tx = mk("text", { x: X(p), y: H - PAD + 15, fill: "#9a8f84",
                            "font-size": 10, "text-anchor": "middle" });
    tx.textContent = `R$${p / 100}`;
    svg.append(tx);
  }
  return svg;
}

/* ------------------------------------------------------------------ gelo
 * Um saco cobre ~50 unidades num dia ameno, mas so ~30 num dia escaldante.
 * Por isso a escolha e do jogador: comprar de menos derrete o estoque.
 */
function cartaoGelo() {
  if (estado.local_atual === "casa") return null;   // freezer de casa nao usa gelo

  const c = el("div", "cartao");
  c.append(el("h2", null, tit(t("ui.gelo"))));
  const corpo = el("div", "gelo-corpo");
  c.append(corpo);
  desenharGelo(corpo);
  return c;
}

/** Total que vai pro isopor hoje: o que foi produzido + o que ja estava pronto. */
function unidadesDoDia() {
  return Object.values(producao).reduce((a, b) => a + b, 0)
       + Object.values(estado.inventario.prontos ?? {}).reduce((a, b) => a + b, 0);
}

function desenharGelo(corpo) {
  // A bridge corta pro que cabe no isopor: gelo pro que nem vai nao conta.
  const info = eng.infoDoGelo(estado, unidadesDoDia());
  const unidades = info.unidades;

  // Primeira montagem do dia: segue a sugestao calculada pelo calor.
  if (gelo === null) gelo = info.sugestao;
  gelo = Math.min(gelo, 8);

  const escolhido = info.opcoes[gelo] ?? info.opcoes[0];
  const quente = info.cobertura < info.cobertura_normal;

  corpo.innerHTML = "";
  const topo = el("div", "gelo-topo");
  topo.innerHTML =
    `<div><span>${t("gelo.vai")}</span><b>${unidades}</b></div>
     <div><span>${t("gelo.cobre")}</span><b class="${quente ? "quente" : ""}">${
       info.cobertura}</b>${quente
         ? ` <i>${t("gelo.calor", { n: info.cobertura_normal })}</i>` : ""}</div>
     <div><span>${t("gelo.saco")}</span><b>${money(info.preco_saco)}</b></div>`;
  corpo.append(topo);

  const linha = el("div", "gelo-linha");
  linha.append(passo(() => gelo, (v) => { gelo = v; desenharGelo(corpo); },
                     1, () => 8));
  const rot = el("div", "gelo-rotulo");
  rot.innerHTML = `<b>${t("gelo.sacos", { n: gelo })}</b> · ${
    money(escolhido.custo)}`;
  linha.append(rot);
  corpo.append(linha);

  const perde = escolhido.derrete;
  const res = el("div", "gelo-resultado" + (perde ? " ruim" : " bom"));
  res.textContent = perde
    ? t("gelo.derrete", { n: perde })
    : (unidades ? t("gelo.tudo") : t("gelo.nada"));
  corpo.append(res);

  if (perde && info.sugestao > gelo) {
    const b = el("button", "sugestao", t("gelo.atalho", { n: info.sugestao }));
    b.onclick = () => { gelo = info.sugestao; desenharGelo(corpo); };
    corpo.append(b);
  }
  atualizarSidebarDia();
}

// ------------------------------------------------------------------ o dia
function rodarDia() {
  // O gelo agora e escolha do jogador (cartaoGelo). Em casa nao se usa.
  const sacos = estado.local_atual === "casa" ? 0 : (gelo ?? 0);
  const plano = { compras: carrinho, producao, precos, gelo: sacos };
  const out = eng.jogarDia(estado, plano);
  estado = out.estado;
  telaRelatorio(out.resultado, out.desbloqueou);
}

function telaRelatorio(r, desbloqueou) {
  redesenharTelaAtual = () => telaRelatorio(r, desbloqueou);
  const app = $("#app");
  app.innerHTML = "";
  app.append(cabecalho(r.clima));

  // --- hero: titulo do resultado + cena de fechamento
  const local = catalogo.locais.find((l) => l.key === estado.local_atual);
  const hero = el("div", "rel-hero");
  const heroTexto = el("div", "texto");
  heroTexto.innerHTML =
    `<div class="eyebrow">${t("ui.dia")} ${r.dia} · ${t("local." + estado.local_atual)} · ${Math.round(r.clima.temp_c)}°C</div>
     <h2>${ICONE[r.clima.kind] ?? "☀️"} ${t("clima." + r.clima.kind)}</h2>`;
  const hResumo = el("p");
  hResumo.textContent = r.resumo_key ? t(r.resumo_key) : t("rel.titulo");
  heroTexto.append(hResumo);
  const heroCena = el("div", "cena-svg");
  heroCena.innerHTML = CENA_RELATORIO[tema] ?? CENA_RELATORIO.escuro;
  hero.append(heroTexto, heroCena);
  app.append(hero);

  // --- tiles de resumo
  const tiles = el("div", "tiles");
  const tile = (rot, val, cls) => {
    const d = el("div", "tile");
    d.append(el("span", null, rot), el("b", cls, val));
    tiles.append(d);
  };
  tile(t("rel.receita"), money(r.receita));
  tile(t("rel.custos"), money(r.custo_insumos + r.custo_fixo));
  tile(t("rel.lucro"), money(r.lucro), r.lucro >= 0 ? "lucro" : "prejuizo");
  tile(t("ui.caixa"), money(r.caixa_final));
  app.append(tiles);

  const layout = el("div", "rel-layout");
  const coluna = el("div", "rel-coluna cartao");
  layout.append(coluna);

  coluna.append(el("h2", null, `${t("rel.titulo")} — ${t("ui.dia")} ${r.dia}`));

  if (r.eventos?.length) {
    const ev = el("div", "eventos");
    for (const e of r.eventos) {
      ev.append(el("div", "evento", t(e.text_key, e.params)));
    }
    coluna.append(ev);
  }

  const c = coluna;
  const tab = el("table", "tab-rel");
  tab.innerHTML = `<thead><tr><th>${t("rel.sabor")}</th>
    <th class="num">${t("rel.levou")}</th>
    <th class="num">${t("rel.vendeu")}</th>
    <th class="num">${t("rel.queria_curto")}</th>
    <th class="num">${t("rel.derreteu")}</th>
    <th class="num">${t("rel.receita")}</th></tr></thead>`;
  const tb = el("tbody");
  for (const f of r.por_sabor) {
    const faltou = f.demanda_potencial > f.ofertados;
    const nome = catalogo.sabores.find((s) => s.key === f.flavor)?.nome ?? f.flavor;
    const tr = el("tr");
    tr.innerHTML = `<td>${nome}</td><td class="num">${f.ofertados}</td>
      <td class="num">${f.vendidos}</td>
      <td class="num ${faltou ? "destaque" : ""}">${f.demanda_potencial}</td>
      <td class="num ${f.perdidos_derretimento ? "derreteu" : ""}">${
        f.perdidos_derretimento || "-"}</td>
      <td class="num">${money(f.receita)}</td>`;
    tb.append(tr);
  }
  tab.append(tb);
  c.append(tab);

  const perdida = r.por_sabor.reduce(
    (a, f) => a + Math.max(0, f.demanda_potencial - f.ofertados), 0);
  if (perdida > 0) {
    c.append(el("div", "aviso", t("rel.sellout", { perdidos: perdida })));
  }

  // Derretimento sem explicacao e o pior tipo de punicao: o jogador perde
  // estoque e nao sabe por que. Aqui ele ve quanto e o motivo.
  const derretido = r.por_sabor.reduce((a, f) => a + f.perdidos_derretimento, 0);
  if (derretido > 0) {
    c.append(el("div", "aviso ruim", t("rel.derreteu_aviso", { n: derretido })));
  }
  if (!r.por_sabor.length) {
    c.append(el("div", "aviso ruim",
      estado.local_atual === "casa" ? t("rel.nada_casa") : t("rel.nada_rua")));
  }

  const pct = Math.min(100, Math.round(100 * estado.caixa / local.meta));
  c.append(el("p", "sub",
    `${t("ui.meta")}: ${money(estado.caixa)} / ${money(local.meta)}`));
  const bm = el("div", "barra-meta");
  bm.innerHTML = `<i style="width:${pct}%"></i>`;
  c.append(bm);

  // --- sidebar: falas da freguesia + acao de seguir pro proximo dia
  const sidebar = el("div", "rel-sidebar");
  if (r.barks?.length) {
    const falasCard = el("div", "cartao");
    falasCard.append(el("div", "eyebrow", t("rel.na_fila")));
    const f = el("div", "falas");
    r.barks.slice(0, 5).forEach((b, i) => {
      const tag = Array.isArray(b) ? b[0] : b;
      const d = el("div", "fala" + (String(tag).includes("preco_alto") ? " caro" : ""));
      d.textContent = "— " + falaDe(String(tag));
      d.style.animationDelay = i * 90 + "ms";
      f.append(d);
    });
    falasCard.append(f);
    sidebar.append(falasCard);

    const filaCena = el("div", "cena-svg");
    filaCena.innerHTML = CENA_FILA[tema] ?? CENA_FILA.escuro;
    sidebar.append(filaCena);
  }

  if (desbloqueou) {
    const nome = t(`local.${desbloqueou}`);
    const info = catalogo.locais.find((l) => l.key === desbloqueou);
    const av = el("div", "aviso");
    av.innerHTML = `<b>${t("cap.desbloqueou")}</b> ${nome} —
      ${t("cap.det", { v: money(info.entrada), n: info.trafego })}`;
    sidebar.append(av);
    const b = el("button", "principal", t("cap.mudar", { nome }));
    b.onclick = () => {
      const o = eng.mudarDePonto(estado, desbloqueou);
      if (o.ok) {
        estado = o.estado;
        // Ponto novo abre sabores e insumos novos.
        catalogo = eng.catalogo(estado.regiao, estado.locais_desbloqueados, lang);
      }
      telaDia();
    };
    sidebar.append(b);
  }
  const seg = el("button", desbloqueou ? "secundaria" : "principal",
                 `${t("ui.proximo_dia")} →`);
  seg.onclick = () => {
    if (estado.encerrado) telaFim();
    else telaDia();
  };
  sidebar.append(seg);

  layout.append(sidebar);
  app.append(layout);
}

// Fallback neutro caso o catalogo nao tenha a fala regional.
const FALAS = {
  compra_simples: "Me vê um aí!",
  compra_gourmet: "Esse cremoso é bom demais!",
  preco_alto: "Tá caro isso aí...",
  preco_barato: "Tá barato! Me vê três.",
  sellout: "Acabou já?",
  calor: "Que calor! Me vê um gelado.",
  chuva: "Vou correr antes de molhar.",
  fila: "Tem fila, hein!",
};
const falaDe = (tag) => {
  const pool = catalogo?.barks?.[tag];
  if (pool?.length) return pool[Math.floor(Math.random() * pool.length)];
  return FALAS[tag] ?? "Me vê um aí!";
};

function telaFim() {
  const app = $("#app");
  app.innerHTML = "";
  const c = el("div", "cartao");
  const venceu = estado.encerrado === "vitoria";
  c.append(el("h2", null, venceu ? t("cap.vitoria") : t("cap.falencia")));
  c.append(el("p", "sub", t("fim.resumo", {
    d: estado.dia - 1, c: money(estado.caixa), f: Math.round(estado.reputacao),
  })));

  // Vencer a regiao fica registrado na campanha, fora desta partida.
  if (venceu) {
    const placar = eng.registrarVitoria(conquistas, estado.regiao);
    salvarConquistas(placar.conquistas);
    const nome = (eng.regioes(lang).find((r) => r.key === estado.regiao)
                  ?? {}).nome ?? estado.regiao;
    const linha = el("div", "campanha-fim" + (placar.zerou ? " zerou" : ""));
    linha.textContent = placar.zerou
      ? t("campanha.zerou")
      : t("campanha.conquistou", {
          nome, n: placar.quantas, total: placar.total,
        });
    c.append(linha);
  }

  const b = el("button", "principal",
                venceu ? t("campanha.escolher_outra") : t("ui.denovo"));
  b.onclick = telaRegioes;
  c.append(b);
  app.append(c);
}

function caixaBench() {
  const d = el("div", "bench");
  d.innerHTML = `<b>Pyodide pronto.</b> interpretador ${Math.round(tempos.interpretador)}ms ·
    módulos ${Math.round(tempos.modulos)}ms · total <b>${(tempos.total / 1000).toFixed(1)}s</b><br>
    <span id="bench-sim">medindo velocidade da simulação...</span>`;
  setTimeout(() => {
    const b = eng.benchmark(200);
    const s = document.querySelector("#bench-sim");
    if (s) s.innerHTML = `Simular um dia: <b>${b.porDiaMs}ms</b> ` +
      `(${b.dias} dias em ${b.totalMs}ms) — orçamento de um frame é 16.7ms.`;
  }, 400);
  return d;
}

boot();
