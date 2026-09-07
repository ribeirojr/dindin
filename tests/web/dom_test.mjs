/** Roda app.js num DOM real (jsdom) com Pyodide de verdade por tras.
 *  E o mais perto do navegador que da sem abrir o navegador. */
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
                 "requestAnimationFrame","cancelAnimationFrame","location","history"]) {
  try { Object.defineProperty(globalThis, k, { value: window[k], configurable: true, writable: true }); }
  catch { /* read-only no Node 26, tudo bem */ }
}
Object.defineProperty(globalThis, "window", { value: window, configurable: true, writable: true });

// Pyodide real
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

// injeta o motor pronto pra nao baixar o pyodide de novo
const { DindinEngine } = await import(new URL("../../web/pyodide-bridge.js", import.meta.url).href);
const eng = new DindinEngine();
eng.pyodide = py;
eng.bridge = py.pyimport("dindin.bridge");
eng.tempos = { interpretador: 900, modulos: 7, importacao: 40, total: 950 };

const erros = [];
window.addEventListener("error", (e) => erros.push(e.message));

// carrega app.js trocando o boot automatico por um controlado
let src = readFileSync("web/app.js", "utf8")
  .replace('import { DindinEngine } from "./pyodide-bridge.js";', "")
  .replace("const eng = new DindinEngine();", "")
  .replace(/\nboot\(\);\s*$/, "\nglobalThis.__api = { telaRegioes, telaDia, comecar, recarregarCozinha, dicaReceita };\n");
const mod = new Function("eng", "__t", src.replace("tempos = null", "tempos = __t") + "\nreturn globalThis.__api;");
const api = mod(eng, eng.tempos);

const $ = (s) => window.document.querySelector(s);
const $$ = (s) => [...window.document.querySelectorAll(s)];

console.log("=== 1. tela de regioes ===");
api.telaRegioes();
const cards = $$(".regiao");
console.log(`  ${cards.length} regioes:`, cards.map(c=>c.querySelector(".produto").textContent).join(", "));

console.log("\n=== 2. escolher Para e entrar no dia ===");
cards.find(c=>c.textContent.includes("chup-chup")).click();
console.log("  cabecalho:", $("header .marca")?.textContent);
console.log("  cartoes na tela:", $$(".cartao h2").map(h=>h.textContent).join(" | "));

console.log("\n=== 3. O BUG: 'Da pra fazer' antes de comprar ===");
const linhasAntes = $$("#corpo-cozinha tr").slice(0,3).map(tr=>{
  const td=[...tr.querySelectorAll("td")];
  return `${td[0].textContent.trim().replace("?","")} -> ${td[2].textContent}`;
});
console.log("  " + linhasAntes.join("\n  "));

console.log("\n=== 4. clicar '+' na feira (polpa, acucar, saquinho) ===");
const feira = $$(".cartao")[1];
const linhasFeira = $$("table tr");
// acha as linhas da feira pelo nome do insumo
const clicar = (nome, vezes) => {
  const tr = $$("tr").find(r => r.textContent.includes(nome) && r.querySelector(".passo"));
  if (!tr) { console.log(`  !! nao achei linha de ${nome}`); return; }
  const mais = tr.querySelectorAll(".passo button")[1];
  for (let i=0;i<vezes;i++) mais.click();
};
clicar("Polpa de fruta comum", 3);
clicar("Açúcar", 1);
clicar("Saquinhos", 1);
console.log("  total da feira:", $("#total-feira")?.textContent.trim());

console.log("\n=== 5. 'Da pra fazer' DEPOIS de encher o carrinho ===");
const linhasDepois = $$("#corpo-cozinha tr").slice(0,3).map(tr=>{
  const td=[...tr.querySelectorAll("td")];
  return `${td[0].textContent.trim().replace("?","")} -> ${td[2].textContent}`;
});
console.log("  " + linhasDepois.join("\n  "));
console.log("\n  MUDOU?", JSON.stringify(linhasAntes)!==JSON.stringify(linhasDepois) ? "SIM ✓" : "NAO ✗");

console.log("\n=== 6. tooltip de receita ===");
const ajuda = $("#corpo-cozinha .ajuda");
console.log("  existe botao '?':", !!ajuda);
const balao = ajuda?.querySelector(".balao");
console.log("  conteudo do balao:");
console.log("   ", balao?.innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim().slice(0,200));

console.log("\n=== 7. limite do '+' na cozinha ===");
const trCoco = $$("#corpo-cozinha tr")[0];
const maisCoco = trCoco.querySelectorAll(".passo button")[1];
const maxCoco = parseInt(trCoco.querySelectorAll("td")[2].textContent);
for (let i=0;i<40;i++) maisCoco.click();
const valor = parseInt(trCoco.querySelector(".passo .v").textContent);
console.log(`  max=${maxCoco}, cliquei 40x(+5) -> valor=${valor}, botao disabled=${maisCoco.disabled}`);
console.log("  respeitou o limite?", valor<=maxCoco ? "SIM ✓" : "NAO ✗");

console.log("\n=== 8. grafico de preco apareceu? ===");
console.log("  SVGs na area de preco:", $$("#area-preco svg").length);
console.log("  sliders:", $$("#area-preco input[type=range]").length);

console.log("\n=== 9. cadencia: dia 1 abre pouca coisa ===");
const nInsumos = $$("tr").filter(r=>r.querySelector(".passo") && !r.closest("#corpo-cozinha")).length;
const nSabores = $$("#corpo-cozinha tr").length;
console.log(`  feira: ${nInsumos} insumos · cozinha: ${nSabores} sabores`);

console.log("\n=== 10. desenho do ponto ===");
const cena = $(".cena");
console.log("  tem cena:", !!cena);
console.log("  " + (cena?.textContent.split("\n")[2] ?? "").trim());
const resumo = $(".plano-resumo");
console.log("  resumo:", resumo?.textContent.replace(/\s+/g," ").trim().slice(0,90));

console.log("\n=== erros de JS ===");
console.log(erros.length ? erros : "  nenhum ✓");

// --- veredito ---
const falhas = [];
if (cards.length !== 6) falhas.push("deviam ser 6 regioes");
if (!linhasAntes.length) falhas.push("cozinha nasceu vazia");
if (!linhasAntes.some(l => l.endsWith("-> 0"))) falhas.push("sem insumo devia mostrar 0");
if (JSON.stringify(linhasAntes) === JSON.stringify(linhasDepois))
  falhas.push("BUG: 'Da pra fazer' nao mudou ao encher o carrinho");
if (!linhasDepois.some(l => /-> [1-9]/.test(l))) falhas.push("carrinho nao liberou producao");
if (!ajuda) falhas.push("faltou o botao '?' do tooltip");
if (!balao?.innerHTML.includes("Pra fazer 10")) falhas.push("tooltip sem a receita");
if (valor > maxCoco) falhas.push("'+' passou do limite");
if (!maisCoco.disabled) falhas.push("'+' devia desabilitar no limite");
if ($$("#area-preco svg").length < 1) falhas.push("grafico de preco nao apareceu");
if (nSabores !== 3) falhas.push(`dia 1 devia ter 3 sabores, tem ${nSabores}`);
if (nInsumos !== 4) falhas.push(`dia 1 devia ter 4 insumos, tem ${nInsumos}`);
if (!cena) falhas.push("faltou o desenho do ponto");
if (!resumo?.textContent.includes("Meta")) falhas.push("resumo do plano sem a meta");
if (erros.length) falhas.push("erros de JS: " + erros.join("; "));

console.log("\n" + "=".repeat(46));
if (falhas.length) {
  console.log("FALHOU:");
  for (const f of falhas) console.log("  ✗ " + f);
  process.exit(1);
}
console.log("TODOS OS TESTES DE DOM PASSARAM ✓");
