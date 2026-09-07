/**
 * DinDin web — a UI. Toda a economia vive no Python via Pyodide.
 * Este arquivo NAO sabe nenhuma regra do jogo: so desenha o que a bridge devolve.
 */
import { DindinEngine } from "./pyodide-bridge.js";

const eng = new DindinEngine();
const $ = (s) => document.querySelector(s);
const el = (t, c, txt) => {
  const e = document.createElement(t);
  if (c) e.className = c;
  if (txt != null) e.textContent = txt;
  return e;
};

// Desenho do ponto de venda, igual ao do terminal.
const CENAS = {
  casa: `    ┌───────────────┐
    │  ▄▄▄▄▄▄▄▄▄▄▄  │
    │  █ FREEZER █  │
    │  █ ░░░░░░░ █  │
    │  ▀▀▀▀▀▀▀▀▀▀▀  │
    │   cozinha     │
    └───────────────┘`,
  isopor: `       ___________
      /  ISOPOR  /|
     /__________/ |
     |░░░░░░░░░| /
     |_________|/
   ─────────────────
       calçada`,
  praia: `  ~  ~   ~   ~   ~  ~
~~~~~~~~~~~~~~~~~~~~~~~
   ___________
  /  ISOPOR  /|    __
 /__________/ |   /  \\
 |░░░░░░░░░| /   |    |
 |_________|/     areia`,
  escola: ` ╔═══════════════════╗
 ║  ESCOLA MUNICIPAL ║
 ╚═══════════════════╝
   ▌▌▌ portão ▌▌▌
    ___________
   /  ISOPOR  /|
  /__________/ |`,
  carrinho: `  ╔═══════════════════╗
  ║   ★  DINDIN  ★    ║
  ╠═══════════════════╣
  ║ ░░░░░░░░░░░░░░░░░ ║
  ╚═══════════════════╝
     ◯           ◯`,
};

const DICAS_PONTO = {
  casa: "Comece pequeno: faça poucos e veja quantos a vizinhança quer.",
  isopor: "Na rua o movimento é bem maior — mas chuva esvazia a calçada.",
  praia: "Praia paga mais caro e adora cremoso. Só que chuva aqui é fatal.",
  escola: "Criança tem pouco dinheiro: aqui o barato vende, o gourmet encalha.",
  carrinho: "Seu ponto, suas regras. Olhe a previsão e escolha o dia certo.",
};

const ICONE = {
  escaldante: "🔥", quente: "☀️", abafado: "🥵",
  nublado: "☁️", chuva: "🌧️", temporal: "⛈️", frio: "🥶",
};

let estado = null, catalogo = null, carrinho = {}, producao = {},
    precos = {}, tempos = null, saboresDoDia = [];

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

// ------------------------------------------------------------------ boot
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
  const regioes = eng.regioes();
  const app = $("#app");
  app.innerHTML = "";

  const c = el("div", "cartao");
  c.append(el("h2", null, "De onde você é?"));
  c.append(el("p", "sub",
    "O doce muda de nome em cada estado — e o clima, o gosto e o preço mudam junto."));

  const grade = el("div", "grade-regioes");
  for (const r of regioes) {
    const b = el("button", "regiao");
    b.innerHTML =
      `<div class="produto">${r.produto}</div>
       <div class="uf">${r.nome} · ${r.gentilico}</div>
       <div class="giria">"${r.giria.join('", "')}"</div>
       <div class="favs">Sai muito: ${r.favoritos.map((f) => f.nome).join(", ")}</div>`;
    b.onclick = () => comecar(r.key);
    grade.append(b);
  }
  c.append(grade);
  app.append(c);
  app.append(caixaBench());
}

function comecar(regiao) {
  const seed = Number(new URLSearchParams(location.search).get("seed"))
            || Math.floor(Math.random() * 1e6);
  estado = eng.novoJogo(regiao, seed);
  // Catalogo filtrado pelo progresso: dia 1 abre so 3 sabores.
  catalogo = eng.catalogo(regiao, estado.locais_desbloqueados);
  history.replaceState({}, "", `?r=${regiao}&seed=${seed}`);
  telaDia();
}

function cabecalho() {
  const h = el("header");
  h.append(el("div", "marca", `DinDin · ${catalogo.produto.plur}`));
  const s = el("div", "stats");
  const add = (rot, val) => {
    const d = el("div", "stat");
    d.append(el("b", null, val), el("span", null, rot));
    s.append(d);
  };
  add("Dia", estado.dia);
  add("Caixa", money(estado.caixa));
  add("Fama", Math.round(estado.reputacao));
  add("Ponto", t(`local.${estado.local_atual}`));
  h.append(s);
  return h;
}

function telaDia() {
  const clima = eng.previsao(estado);
  carrinho = {}; producao = {}; precos = {};
  saboresDoDia = eng.sabores(estado, {}, {});

  const app = $("#app");
  app.innerHTML = "";
  app.append(cabecalho());

  // --- plano do dia: onde voce esta + como esta o tempo
  const pl = el("div", "cartao");
  pl.append(el("h2", null,
    `Dia ${estado.dia} · ${t("local." + estado.local_atual)}`));
  pl.append(el("p", "sub", "Antes de começar: veja como está o dia."));
  const plGrid = el("div", "plano-grid");
  const cena = el("pre", "cena");
  cena.textContent = CENAS[estado.local_atual] ?? CENAS.casa;
  const local0 = catalogo.locais.find((l) => l.key === estado.local_atual);
  const falta = Math.max(0, local0.meta - estado.caixa);
  const resumo = el("div", "plano-resumo");
  resumo.innerHTML =
    `<div><span>No caixa</span><b>${money(estado.caixa)}</b></div>
     <div><span>Meta</span><b>${money(local0.meta)}</b>${falta
       ? ` <i>faltam ${money(falta)}</i>` : ' <i class="ok">batida!</i>'}</div>
     <div><span>Sabores</span><b>${catalogo.sabores.length}</b></div>
     <div><span>Congelado</span><b>${
       Object.values(estado.inventario.prontos ?? {}).reduce((a,b)=>a+b,0)}</b></div>`;
  plGrid.append(cena, resumo);
  pl.append(plGrid);
  pl.append(el("div", "aviso", DICAS_PONTO[estado.local_atual] ?? ""));
  app.append(pl);

  // --- clima
  const cc = el("div", "cartao");
  cc.append(el("h2", null, "Previsão de hoje"));
  const cl = el("div", "clima");
  cl.innerHTML =
    `<div class="icone">${ICONE[clima.kind] ?? "☀️"}</div>
     <div>
       <div class="temp">${Math.round(clima.temp_c)}°C</div>
       <div class="desc">${t("clima." + clima.kind)} · sensação ${Math.round(clima.heat_index)}°C</div>
       <div class="dica" style="color:${dicaCor(clima)}">${dicaTexto(clima)}</div>
     </div>`;
  cc.append(cl);
  app.append(cc);

  // --- feira
  app.append(cartaoFeira());
  // --- cozinha
  app.append(cartaoCozinha());
  // --- preco (com o grafico)
  app.append(cartaoPreco(saboresDoDia));
  // Monta a tabela ja: esperar timeout deixava a cozinha vazia num primeiro frame.
  recarregarCozinha();

  const acoes = el("div", "linha-acoes");
  const vender = el("button", "principal", "Vender! →");
  vender.onclick = rodarDia;
  acoes.append(vender);
  app.append(acoes);
}

function dicaCor(c) {
  if (["chuva", "temporal", "frio"].includes(c.kind)) return "#3b9edb";
  if (c.heat_index > 34) return "#f5c518";
  return "#2fa84f";
}
function dicaTexto(c) {
  if (c.kind === "temporal") return "Temporal. Quase ninguém na rua.";
  if (c.kind === "chuva") return "Chuva. Movimento fraco.";
  if (c.kind === "frio") return "Frio. Ninguém quer gelado.";
  if (c.heat_index > 34) return "Calor forte! Vai vender muito — e dá pra cobrar mais.";
  if (c.heat_index > 30) return "Movimento bom.";
  return "Movimento normal.";
}

function cartaoFeira() {
  const c = el("div", "cartao");
  c.append(el("h2", null, "1. Feira"));
  c.append(el("p", "sub", "Comprando em quantidade, sai mais barato."));
  const tab = el("table");
  tab.innerHTML = `<thead><tr><th>Insumo</th><th>Unid.</th>
    <th class="num">Preço</th><th class="num">Tem</th><th>Levar</th></tr></thead>`;
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
    ? `<b style="color:var(--rosa)">Falta ${money(-sobra)}</b> — tire alguma coisa do carrinho.`
    : `Compra: <b>${money(custo)}</b> · sobra <b>${money(sobra)}</b>`;
  const btn = document.querySelector("button.principal");
  if (btn) btn.disabled = sobra < 0;
}

function cartaoCozinha() {
  const c = el("div", "cartao");
  c.append(el("h2", null, "2. Cozinha"));
  c.append(el("p", "sub", t("cozinha.subtitulo")));
  const tab = el("table");
  tab.innerHTML = `<thead><tr><th>Sabor</th><th class="num">Custo</th>
    <th class="num">Dá pra fazer</th><th class="num">Pronto</th><th>Fazer</th></tr></thead>`;
  tab.append(el("tbody", null, ""));
  tab.querySelector("tbody").id = "corpo-cozinha";
  c.append(tab);
  c.append(el("p", "sub",
    `Cabe ${estado.capacidade_freezer} no freezer. O que passar disso derrete.`));
  return c;
}

/** Refaz a tabela da cozinha contando o que esta no carrinho da feira. */
function recarregarCozinha() {
  const tb = document.querySelector("#corpo-cozinha");
  if (!tb) return;
  saboresDoDia = eng.sabores(estado, carrinho, producao);
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
}

/** Texto do tooltip: o que precisa pra fazer 10 unidades. */
function dicaReceita(s) {
  const linhas = s.receita.map((r) => {
    const falta = r.tem < r.por_dez / 10;
    const cor = falta ? "var(--rosa)" : "var(--verde)";
    return `<span style="color:${cor}">${r.por_dez} ${r.unidade} de ${r.nome}</span>` +
           `<span style="color:var(--dim)"> (tem ${r.tem})</span>`;
  });
  const cab = `<b>Pra fazer 10 ${catalogo.produto.plur}:</b>`;
  const rodape = s.faltando.length
    ? `<div style="color:var(--rosa);margin-top:6px">Falta comprar: ${s.faltando.join(", ")}</div>`
    : `<div style="color:var(--verde);margin-top:6px">Tem tudo que precisa.</div>`;
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
  c.append(el("h2", null, "3. Preço"));
  c.append(el("p", "sub",
    "A curva mostra quantos compram em cada preço. O losango é o preço de maior lucro."));
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
      Faça alguma coisa na cozinha primeiro.</p>`;
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
    <span style="font-size:12px;color:var(--dim)">custo ${money(curva.custo)} ·
    melhor preço <b style="color:var(--verde)">${money(curva.melhor_preco)}</b></span>`;
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
    info.innerHTML = `${Math.round(p.resposta * 100)}% compram · margem
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

// ------------------------------------------------------------------ o dia
function rodarDia() {
  const plano = { compras: carrinho, producao, precos, gelo: 0 };
  if (estado.local_atual !== "casa") {
    const total = Object.values(producao).reduce((a, b) => a + b, 0)
                + Object.values(estado.inventario.prontos ?? {}).reduce((a, b) => a + b, 0);
    plano.gelo = Math.max(1, Math.ceil(total / 50));
  }
  const out = eng.jogarDia(estado, plano);
  estado = out.estado;
  telaRelatorio(out.resultado, out.desbloqueou);
}

function telaRelatorio(r, desbloqueou) {
  const app = $("#app");
  app.innerHTML = "";
  app.append(cabecalho());

  const c = el("div", "cartao");
  c.append(el("h2", null, `Como foi o dia ${r.dia}`));

  const cl = el("div", "clima");
  cl.innerHTML = `<div class="icone">${ICONE[r.clima.kind] ?? "☀️"}</div>
    <div><div class="temp">${Math.round(r.clima.temp_c)}°C</div>
    <div class="desc">${t("clima." + r.clima.kind)}</div></div>`;
  c.append(cl);

  if (r.eventos?.length) {
    const ev = el("div", "eventos");
    for (const e of r.eventos) {
      ev.append(el("div", "evento", t(e.text_key, e.params)));
    }
    c.append(ev);
  }

  const tab = el("table");
  tab.innerHTML = `<thead><tr><th>Sabor</th><th class="num">Levou</th>
    <th class="num">Vendeu</th><th class="num">Queriam</th>
    <th class="num">Receita</th></tr></thead>`;
  const tb = el("tbody");
  for (const f of r.por_sabor) {
    const faltou = f.demanda_potencial > f.ofertados;
    const nome = catalogo.sabores.find((s) => s.key === f.flavor)?.nome ?? f.flavor;
    const tr = el("tr");
    tr.innerHTML = `<td>${nome}</td><td class="num">${f.ofertados}</td>
      <td class="num">${f.vendidos}</td>
      <td class="num ${faltou ? "destaque" : ""}">${f.demanda_potencial}</td>
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

  const tiles = el("div", "tiles");
  const tile = (rot, val, cls) => {
    const d = el("div", "tile");
    d.append(el("span", null, rot), el("b", cls, val));
    tiles.append(d);
  };
  tile("Receita", money(r.receita));
  tile("Custos", money(r.custo_insumos + r.custo_fixo));
  tile("Lucro", money(r.lucro), r.lucro >= 0 ? "lucro" : "prejuizo");
  tile("Caixa", money(r.caixa_final));
  c.append(tiles);

  const local = catalogo.locais.find((l) => l.key === estado.local_atual);
  const pct = Math.min(100, Math.round(100 * estado.caixa / local.meta));
  c.append(el("p", "sub",
    `Meta do capítulo: ${money(estado.caixa)} / ${money(local.meta)}`));
  const bm = el("div", "barra-meta");
  bm.innerHTML = `<i style="width:${pct}%"></i>`;
  c.append(bm);

  if (r.barks?.length) {
    const f = el("div", "falas");
    r.barks.slice(0, 5).forEach((b, i) => {
      const tag = Array.isArray(b) ? b[0] : b;
      const d = el("div", "fala" + (String(tag).includes("preco_alto") ? " caro" : ""));
      d.textContent = "— " + falaDe(String(tag));
      d.style.animationDelay = i * 90 + "ms";
      f.append(d);
    });
    c.append(f);
  }
  app.append(c);

  const acoes = el("div", "linha-acoes");
  if (desbloqueou) {
    const nome = t(`local.${desbloqueou}`);
    const info = catalogo.locais.find((l) => l.key === desbloqueou);
    const av = el("div", "aviso");
    av.innerHTML = `<b>${t("cap.desbloqueou")}</b> ${nome} —
      entrada ${money(info.entrada)}, movimento ${info.trafego}/dia.`;
    app.append(av);
    const b = el("button", "principal", `Mudar pra ${nome}`);
    b.onclick = () => {
      const o = eng.mudarDePonto(estado, desbloqueou);
      if (o.ok) {
        estado = o.estado;
        // Ponto novo abre sabores e insumos novos.
        catalogo = eng.catalogo(estado.regiao, estado.locais_desbloqueados);
      }
      telaDia();
    };
    acoes.append(b);
  }
  const seg = el("button", desbloqueou ? "secundaria" : "principal", "Próximo dia →");
  seg.onclick = () => {
    if (estado.encerrado) telaFim();
    else telaDia();
  };
  acoes.append(seg);
  app.append(acoes);
}

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
const falaDe = (tag) => FALAS[tag] ?? "Me vê um aí!";

function telaFim() {
  const app = $("#app");
  app.innerHTML = "";
  const c = el("div", "cartao");
  const venceu = estado.encerrado === "vitoria";
  c.append(el("h2", null, venceu ? t("cap.vitoria") : t("cap.falencia")));
  c.append(el("p", "sub",
    `${estado.dia - 1} dias · caixa ${money(estado.caixa)} · fama ${Math.round(estado.reputacao)}`));
  const b = el("button", "principal", "Jogar de novo");
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
