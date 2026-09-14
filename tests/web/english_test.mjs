/** Ingles na web: o seletor da tela inicial troca a interface inteira,
 *  mas o produto continua com o nome regional e a giria fica em portugues. */
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
    "\nglobalThis.__api = { telaRegioes, recarregarCozinha, getEstado: ()=>estado, getLang: ()=>lang };\n");
const mod = new Function("eng", "__t", "CENA_HERO", "CENA_RELATORIO", "CENA_FILA", "cenaLocal", "cenaRegiao",
  src.replace("tempos = null", "tempos = __t") + "\nreturn globalThis.__api;");
const api = mod(eng, eng.tempos, svgArt.CENA_HERO, svgArt.CENA_RELATORIO, svgArt.CENA_FILA, svgArt.cenaLocal, svgArt.cenaRegiao);

const $ = (s) => window.document.querySelector(s);
const $$ = (s) => [...window.document.querySelectorAll(s)];
const falhas = [];
const titulos = () => $$(".cartao h2, .hero-texto h1").map(h => h.textContent);

console.log("=== 1. o seletor existe e comeca em portugues ===");
api.telaRegioes();
// .lang-chip tambem inclui o link do REPL de Python (easter egg), que nao
// e um idioma -- so os idiomas de verdade tem o data-idioma marcado com pt/en.
const chips = $$(".lang-chip:not(.repl-link)");
console.log("  chips:", chips.map(c => c.textContent).join(" / "),
            "| ativo:", $(".lang-chip.ativa")?.textContent);
if (chips.length !== 2) falhas.push("deviam ser 2 idiomas no seletor");
if (!$(".lang-chip.ativa")?.textContent.includes("Português"))
  falhas.push("o padrao devia ser portugues");
if (!titulos().some(t => t.includes("Escolha uma cidade")))
  falhas.push("titulo pt errado");

console.log("\n=== 2. clicar English troca a tela inteira ===");
chips.find(c => c.textContent.includes("English")).click();
console.log("  titulo:", titulos()[0]);
console.log("  url:", window.location.search || "(sem query)");
if (api.getLang() !== "en") falhas.push("lang nao virou en");
if (!titulos().some(t => t.includes("Pick a city to play at")))
  falhas.push("titulo nao traduziu");
if (!window.location.search.includes("lang=en"))
  falhas.push("lang=en devia ir pra URL (link compartilhavel)");

console.log("\n=== 3. o produto continua regional; a giria continua pt ===");
const card = $$(".regiao").find(c => c.textContent.includes("chup-chup"));
console.log("  card do Pará:", card?.textContent.replace(/\s+/g, " ").slice(0, 110));
if (!card) falhas.push("chup-chup sumiu no modo ingles");
if (!card?.textContent.includes("égua") && !card?.textContent.includes("Égua"))
  falhas.push("a giria devia continuar em portugues");
if (!card?.textContent.includes("Big sellers"))
  falhas.push("o rotulo dos favoritos devia estar em ingles");

console.log("\n=== 4. jogar um dia inteiro em ingles ===");
card.click();
console.log("  cartoes:", titulos().join(" | "));
if (!titulos().some(t => t.includes("Market"))) falhas.push("Feira nao virou Market");
if (!titulos().some(t => t.includes("Kitchen"))) falhas.push("Cozinha nao virou Kitchen");
if (!titulos().some(t => t.includes("Price"))) falhas.push("Preço nao virou Price");
const header = $("header")?.textContent ?? "";
if (!header.includes("chup-chup")) falhas.push("cabecalho perdeu o nome regional");
if (!/Cash/.test(header)) falhas.push("cabecalho sem Cash");

// sabores em ingles na cozinha (a tabela so se popula no recarregarCozinha)
api.recarregarCozinha();
const cozinha = $$("#corpo-cozinha tr").map(tr => tr.textContent).join(" ");
console.log("  cozinha:", cozinha.replace(/\s+/g, " ").slice(0, 90));
if (!cozinha.includes("Coconut")) falhas.push("sabor nao traduziu (Coconut)");

$$("button").find(b => /Sell!/.test(b.textContent))?.click();
console.log("  relatorio:", titulos().join(" | "));
if (!titulos().some(t => t.includes("How the day went")))
  falhas.push("relatorio nao veio em ingles");
const ths = $$("table th").map(h => h.textContent);
console.log("  colunas:", ths.join(" | "));
if (!ths.includes("Sold")) falhas.push("colunas do relatorio sem Sold");

console.log("\n=== 5. sem marcador de traducao faltando ===");
const corpo = window.document.body.textContent;
if (corpo.includes("⟨missing:")) falhas.push("tem chave sem traducao na tela");

console.log("\n=== erros de JS ===");
console.log(erros.length ? erros : "  nenhum ✓");
if (erros.length) falhas.push("erros de JS: " + erros.join("; "));

console.log("\n" + "=".repeat(46));
if (falhas.length) {
  console.log("FALHOU:");
  for (const f of falhas) console.log("  ✗ " + f);
  process.exit(1);
}
console.log("INGLES NA WEB: TUDO PASSOU ✓");
