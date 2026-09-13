/** Isopor e gelo na versao web: os dois passos que so existiam no terminal.
 *  Mesmo bootstrap do dom_test, mas jogando ate a rua, onde eles aparecem. */
import { JSDOM } from "jsdom";
import { loadPyodide } from "pyodide";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const RAIZ_PROJ = new URL("../..", import.meta.url).pathname;
process.chdir(RAIZ_PROJ);
const dom = new JSDOM(readFileSync("web/index.html", "utf8"),
  { url: "http://localhost:8765/", pretendToBeVisual: true });
const { window } = dom;
for (const k of ["document","HTMLElement","Element","Node","getComputedStyle",
                 "requestAnimationFrame","cancelAnimationFrame","location","history",
                 "localStorage"]) {
  try { Object.defineProperty(globalThis, k, { value: window[k], configurable: true, writable: true }); }
  catch { /* read-only no Node 26 */ }
}
Object.defineProperty(globalThis, "window", { value: window, configurable: true, writable: true });

const RAIZ = "web/py";
const listar = (d) => readdirSync(d).flatMap((n) => {
  const p = join(d, n);
  return statSync(p).isDirectory() ? listar(p) : (n.endsWith(".py") ? [p] : []);
});
const py = await loadPyodide();
for (const d of ["/jogo","/jogo/dindin","/jogo/dindin/sim","/jogo/dindin/content",
                 "/jogo/dindin/i18n","/jogo/dindin/i18n/overrides"]) { try { py.FS.mkdir(d); } catch {} }
for (const abs of listar(RAIZ)) py.FS.writeFile(`/jogo/dindin/${relative(RAIZ, abs)}`, readFileSync(abs,"utf8"));
py.runPython(`import sys; sys.path.insert(0,"/jogo")`);

const { DindinEngine } = await import(new URL("../../web/pyodide-bridge.js", import.meta.url).href);
const eng = new DindinEngine();
eng.pyodide = py;
eng.bridge = py.pyimport("dindin.bridge");
eng.tempos = { interpretador: 900, modulos: 7, importacao: 40, total: 950 };

const erros = [];
window.addEventListener("error", (e) => erros.push(e.message));

const svgArt = await import(new URL("../../web/svg-art.js", import.meta.url).href);
let src = readFileSync("web/app.js", "utf8")
  .replace('import { DindinEngine } from "./pyodide-bridge.js";', "")
  .replace('import { CENA_HERO, CENA_RELATORIO, CENA_FILA, cenaLocal, cenaRegiao } from "./svg-art.js";', "")
  .replace("const eng = new DindinEngine();", "")
  .replace(/\nboot\(\);\s*$/,
    "\nglobalThis.__api = { telaRegioes, telaDia, comecar, setEstado: (e)=>{estado=e;}, getEstado: ()=>estado, getGelo: ()=>gelo };\n");
const mod = new Function("eng", "__t", "CENA_HERO", "CENA_RELATORIO", "CENA_FILA", "cenaLocal", "cenaRegiao",
  src.replace("tempos = null", "tempos = __t") + "\nreturn globalThis.__api;");
const api = mod(eng, eng.tempos, svgArt.CENA_HERO, svgArt.CENA_RELATORIO, svgArt.CENA_FILA, svgArt.cenaLocal, svgArt.cenaRegiao);

const $ = (s) => window.document.querySelector(s);
const $$ = (s) => [...window.document.querySelectorAll(s)];
const falhas = [];
const titulos = () => $$(".cartao h2").map(h => h.textContent);

console.log("=== 1. em casa: sem isopor, sem gelo ===");
api.telaRegioes();
$$(".regiao").find(c => c.textContent.includes("chup-chup")).click();
console.log("  passos:", titulos().join(" | "));
if (titulos().some(t => /Isopor/.test(t))) falhas.push("isopor nao devia aparecer em casa");
if (titulos().some(t => /Gelo/.test(t)))   falhas.push("gelo nao devia aparecer em casa");
if (!titulos().includes("1. Feira")) falhas.push("em casa a Feira devia ser o passo 1");

console.log("\n=== 2. ir pra rua com dinheiro no bolso ===");
let e = api.getEstado();
e.caixa = 30000;                      // R$300: da pra isopor + insumos
e.locais_desbloqueados = ["casa", "isopor"];
e.local_atual = "isopor";
api.setEstado(e);
api.telaDia();
console.log("  passos:", titulos().join(" | "));
if (!titulos().includes("1. Isopor")) falhas.push("na rua o Isopor devia ser o passo 1");
if (!titulos().some(t => /Gelo/.test(t))) falhas.push("na rua devia ter passo de Gelo");

console.log("\n=== 3. vitrine de isopores ===");
const ops = $$(".isopor-op");
console.log(`  ${ops.length} opcoes:`, ops.map(o => o.querySelector("b").textContent).join(", "));
if (ops.length < 2) falhas.push("deviam aparecer varias opcoes de isopor");

console.log("\n=== 4. comprar o isopor simples ===");
const caixaAntes = api.getEstado().caixa;
const btn = ops[0].querySelector("button");
console.log("  botao:", btn.textContent, "| disabled:", btn.disabled);
btn.click();
const depois = api.getEstado();
console.log(`  caixa ${caixaAntes} -> ${depois.caixa} | isopor=${depois.isopor} dias=${depois.isopor_dias}`);
if (!depois.isopor) falhas.push("comprar nao registrou o isopor no estado");
if (depois.caixa >= caixaAntes) falhas.push("comprar nao descontou do caixa");

console.log("\n=== 5. depois de comprar mostra o que esta em uso ===");
console.log("  em uso:", $(".isopor-atual")?.textContent.replace(/\s+/g," ").trim());
if (!$(".isopor-atual")) falhas.push("faltou o painel do isopor em uso");

console.log("\n=== 6. gelo reage ao que foi produzido ===");
const corpo = $(".gelo-corpo");
console.log("  topo:", $(".gelo-topo")?.textContent.replace(/\s+/g," ").trim());
console.log("  veredito:", $(".gelo-resultado")?.textContent.trim());
console.log("  sacos sugeridos:", api.getGelo());
if (!corpo) falhas.push("faltou o cartao de gelo");

console.log("\n=== 7. com estoque de verdade: pouco gelo => derrete ===");
// Poe 100 prontos no inventario e remonta: agora ha o que gelar.
let e2 = api.getEstado();
e2.inventario.prontos = { coco: 100 };
api.setEstado(e2);
api.telaDia();
const sugerido = api.getGelo();
console.log("  sugestao pra 100 unidades:", sugerido,
            "|", $(".gelo-resultado")?.textContent.trim());
if (!(sugerido >= 3)) falhas.push(`no calor 100 unidades pediam >=3 sacos, veio ${sugerido}`);
if (!/Nada derrete/.test($(".gelo-resultado")?.textContent ?? ""))
  falhas.push("a sugestao devia cobrir tudo");

const menos = $(".gelo-linha .passo button");
for (let i = 0; i < 10; i++) menos.click();
const txt = $(".gelo-resultado")?.textContent.trim();
console.log("  com 0 sacos:", txt);
if (api.getGelo() !== 0) falhas.push("o '-' devia chegar a zero");
if (!/Derrete 100/.test(txt ?? "")) falhas.push("com 0 sacos as 100 unidades deviam derreter");
if (!$("button.sugestao")) falhas.push("faltou o atalho de corrigir o gelo");
$("button.sugestao").click();
console.log("  depois do atalho:", api.getGelo(), "|", $(".gelo-resultado")?.textContent.trim());
if (api.getGelo() !== sugerido) falhas.push("o atalho devia voltar pra sugestao");

console.log("\n=== 8. cobertura cai no calor? (via bridge) ===");
const infoQ = eng.infoDoGelo(api.getEstado(), 100);
console.log(`  cobertura hoje=${infoQ.cobertura} (normal ${infoQ.cobertura_normal}) sugestao=${infoQ.sugestao}`);
if (!(infoQ.cobertura > 0)) falhas.push("cobertura do saco veio zerada");

console.log("\n=== 9. o dia roda com o gelo escolhido ===");
// Producao de verdade + gelo insuficiente de proposito: o relatorio tem que
// mostrar derretimento em vez de simplesmente ignorar a escolha.
let e3 = api.getEstado();
e3.inventario.prontos = { coco: 100 };
api.setEstado(e3);
api.telaDia();
for (let i = 0; i < 10; i++) $(".gelo-linha .passo button").click();  // zera o gelo
console.log("  sacos escolhidos:", api.getGelo());
$$("button").find(b => /Vender/.test(b.textContent))?.click();
const rel = $$(".cartao h2").map(h => h.textContent).join(" | ");
console.log("  tela apos vender:", rel);
if (!/Como foi o dia/.test(rel)) falhas.push("nao chegou no relatorio");
const txtRel = window.document.body.textContent;
console.log("  avisa a perda total:", /Nada chegou ao ponto|Derreteu/.test(txtRel));
if (!/Nada chegou ao ponto|Derreteu/.test(txtRel))
  falhas.push("perda total sem explicacao no relatorio");

// Agora um dia que da certo: estoque dentro da capacidade + gelo suficiente.
let e4 = api.getEstado();
e4.inventario.prontos = { coco: 40 };
e4.precos = { coco: 50 };
api.setEstado(e4);
globalThis.precos = { coco: 50 };
api.telaDia();
console.log("  gelo sugerido pra 40:", api.getGelo());
$$("button").find(b => /Vender/.test(b.textContent))?.click();
const cab = $$("table th").map(h => h.textContent);
console.log("  colunas do relatorio:", cab.join(" | "));
if (!cab.includes("Derreteu")) falhas.push("relatorio sem a coluna Derreteu");
const linhasRel = $$("table tbody tr").map(tr =>
  [...tr.querySelectorAll("td")].map(td => td.textContent.trim()).join(" "));
  console.log("  linhas:", linhasRel.slice(0, 3).join(" / ") || "(nenhuma)");
  console.log("  caixa final:", api.getEstado().caixa);
if (api.getEstado().caixa < 0) falhas.push("caixa ficou negativo");

console.log("\n=== erros de JS ===");
console.log(erros.length ? erros : "  nenhum ✓");
if (erros.length) falhas.push("erros de JS: " + erros.join("; "));

console.log("\n" + "=".repeat(46));
if (falhas.length) {
  console.log("FALHOU:");
  for (const f of falhas) console.log("  ✗ " + f);
  process.exit(1);
}
console.log("ISOPOR + GELO NA WEB: TUDO PASSOU ✓");
