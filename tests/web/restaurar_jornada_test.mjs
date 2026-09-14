/** Restaurar jornada: o save do dia tem que devolver o jogador DENTRO do dia,
 *  com o estado real (caixa, dia, estoque, ponto), e deixar jogar o dia seguinte.
 *  O bug: restaurarDeDump voltava pra tela de regioes; clicar na regiao chamava
 *  novoJogo e apagava a jornada — o jogador reabria Brasilia e nao conseguia
 *  continuar de onde parou. Mesmo bootstrap do dom_test. */
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
                 "localStorage","Blob","URL","File","FileList","DataTransfer"]) {
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
    "\nglobalThis.__api = { telaRegioes, telaDia, comecar, rodarDia, dumpJornada, restaurarDeDump,"
    + " setEstado: (e)=>{estado=e;}, getEstado: ()=>estado, getCatalogo: ()=>catalogo };\n");
const mod = new Function("eng", "__t", "CENA_HERO", "CENA_RELATORIO", "CENA_FILA", "cenaLocal", "cenaRegiao",
  src.replace("tempos = null", "tempos = __t") + "\nreturn globalThis.__api;");
const api = mod(eng, eng.tempos, svgArt.CENA_HERO, svgArt.CENA_RELATORIO, svgArt.CENA_FILA, svgArt.cenaLocal, svgArt.cenaRegiao);

const $ = (s) => window.document.querySelector(s);
const $$ = (s) => [...window.document.querySelectorAll(s)];
const falhas = [];
const checa = (cond, msg) => { console.log(`  ${cond ? "✓" : "✗"} ${msg}`); if (!cond) falhas.push(msg); };

console.log("=== 1. abrir Brasilia e jogar o dia 1 ===");
api.telaRegioes();
const cardDF = $$(".regiao").find((c) => /Bras|DF|geladinho/i.test(c.textContent));
checa(!!cardDF, "tela de regioes tem o card do DF");
cardDF.click();
checa(!!$("header .marca"), "entrou no dia depois de escolher a regiao");
api.rodarDia();   // vende o dia 1 (plano vazio, mas fecha o dia de verdade)
const depoisDoDia = JSON.parse(JSON.stringify(api.getEstado()));
console.log(`  dia=${depoisDoDia.dia} caixa=${depoisDoDia.caixa} ponto=${depoisDoDia.local_atual}`);
checa(depoisDoDia.dia === 2, "o dia avancou para 2");

console.log("\n=== 2. salvar a jornada ===");
// Estado com progresso de verdade: caixa e estoque que precisam sobreviver.
let e = api.getEstado();
e.caixa = 123456;
e.inventario.prontos = { coco: 25 };
api.setEstado(e);
const dump = api.dumpJornada(api.getEstado());
checa(!!dump && !!dump.estado, "dumpJornada produziu um dump com estado");
console.log(`  dump: dia=${dump?.estado?.dia} caixa=${dump?.estado?.caixa} seed=${dump?.estado?.seed}`);

console.log("\n=== 3. 'fechar o jogo' e restaurar o save ===");
api.setEstado(null);
api.telaRegioes();                       // jogador reabre o jogo na tela inicial
api.restaurarDeDump(JSON.parse(JSON.stringify(dump)));
const rest = api.getEstado();
checa(!!rest, "restaurou algum estado");
checa(rest?.dia === dump.estado.dia, `dia restaurado (${rest?.dia} == ${dump.estado.dia})`);
checa(rest?.caixa === 123456, `caixa restaurada (${rest?.caixa} == 123456)`);
checa(rest?.regiao === dump.estado.regiao, "regiao restaurada");
checa(rest?.seed === dump.estado.seed, "seed restaurada");
checa((rest?.inventario?.prontos?.coco ?? 0) === 25, "estoque pronto sobreviveu");

console.log("\n=== 4. O BUG: restaurar tem que cair DENTRO do dia, nao na tela de regioes ===");
const naTelaDeRegioes = $$(".regiao").length > 0;
checa(!naTelaDeRegioes, "nao voltou para a tela de escolha de regiao");
checa(!!$("header .marca"), "desenhou o cabecalho do dia");
const cab = window.document.body.textContent;
checa(cab.includes(String(rest?.dia)), "cabecalho mostra o dia restaurado");
checa(!!api.getCatalogo()?.locais, "catalogo da regiao foi recarregado (tem locais)");

console.log("\n=== 5. dar pra jogar o dia seguinte depois de restaurar ===");
const diaAntes = api.getEstado().dia;
let deuErro = null;
try { api.rodarDia(); } catch (err) { deuErro = err; }
checa(!deuErro, `rodarDia apos restaurar nao explode${deuErro ? " (" + deuErro.message + ")" : ""}`);
const diaDepois = api.getEstado()?.dia;
checa(diaDepois === diaAntes + 1, `o dia avancou apos restaurar (${diaAntes} -> ${diaDepois})`);
checa(/Como foi o dia|How the day/.test(window.document.body.textContent),
      "chegou no relatorio do dia restaurado");

console.log("\n=== 6. save antigo (version 1) ainda carrega ===");
const antigo = { estado: JSON.parse(JSON.stringify(dump.estado)), conquistas: [], tema: "escuro" };
api.setEstado(null);
let erroAntigo = null;
try { api.restaurarDeDump(antigo); } catch (err) { erroAntigo = err; }
checa(!erroAntigo, `save v1 carrega sem explodir${erroAntigo ? " (" + erroAntigo.message + ")" : ""}`);
checa(api.getEstado()?.dia === dump.estado.dia, "save v1 restaurou o dia");
checa($$(".regiao").length === 0, "save v1 tambem cai dentro do dia");

console.log("\n=== 7. arquivo invalido nao destroi a partida em andamento ===");
api.telaDia();
const antesDoLixo = JSON.parse(JSON.stringify(api.getEstado()));
try { api.restaurarDeDump({ version: 2, lixo: true }); } catch { /* pode recusar */ }
checa(api.getEstado()?.dia === antesDoLixo.dia,
      "dump sem estado nao apagou a partida em andamento");

console.log("\n=== 8. lote sem validade (null) nao derruba o restore ===");
// Bug real: pyodide.toPy() converte JS null num sentinela JsNull, nao em
// None -- "lote.dia_validade is not None" fica sempre verdadeiro pra dados
// vindos de um arquivo de save de verdade, e expirar() quebra comparando
// JsNull < int. Um save com um insumo nao-perecivel (ex: saquinho) sempre
// tem dia_validade: null nos lotes -- e um arquivo carregado do disco
// (JSON.parse de verdade) e o unico jeito de reproduzir: um objeto JS
// escrito a mao (`dia_validade: null` literal na fonte) e o mesmo null,
// entao basta vir de dados, nao de codigo, pra bater o caminho real.
const dumpComLoteSemValidade = JSON.parse(JSON.stringify({
  version: 2,
  estado: {
    ...JSON.parse(JSON.stringify(dump.estado)),
    inventario: {
      ingredientes: { saquinho: 5 },
      lotes: { saquinho: [[5, null]] },
      prontos: {},
    },
  },
}));
let erroLoteNulo = null;
try {
  eng.restaurarEstado(dumpComLoteSemValidade.estado);
} catch (err) { erroLoteNulo = err; }
checa(!erroLoteNulo,
  `restaurarEstado com lote sem validade (null) nao quebra o motor${erroLoteNulo ? " (" + erroLoteNulo.message + ")" : ""}`);

api.setEstado(null);
let erroRestoreUI = null;
try { api.restaurarDeDump(dumpComLoteSemValidade); } catch (err) { erroRestoreUI = err; }
checa(!erroRestoreUI, `restaurarDeDump (fluxo da UI) com lote sem validade nao quebra${erroRestoreUI ? " (" + erroRestoreUI.message + ")" : ""}`);
checa(api.getEstado()?.inventario?.ingredientes?.saquinho === 5,
  "insumo nao-perecivel sobreviveu ao restore");
let erroDiaLoteNulo = null;
try { api.rodarDia(); } catch (err) { erroDiaLoteNulo = err; }
checa(!erroDiaLoteNulo,
  `jogar o dia com esse insumo nao explode${erroDiaLoteNulo ? " (" + erroDiaLoteNulo.message + ")" : ""}`);

console.log("\n=== erros de JS ===");
console.log(erros.length ? erros : "  nenhum ✓");
if (erros.length) falhas.push("erros de JS: " + erros.join("; "));

console.log("\n" + "=".repeat(46));
if (falhas.length) {
  console.log("FALHOU:");
  for (const f of falhas) console.log("  ✗ " + f);
  process.exit(1);
}
console.log("RESTAURAR JORNADA: TUDO PASSOU ✓");
