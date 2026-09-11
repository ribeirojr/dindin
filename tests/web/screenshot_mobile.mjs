/** Fotografa a versao web num viewport de celular de verdade (CDP).
 *
 * Uso: node tests/web/screenshot_mobile.mjs [url] [dirSaida]
 * Precisa do Chrome instalado; sobe o proprio Chrome headless com
 * --remote-debugging-port e conversa via DevTools Protocol.
 * Gera: 1-splash, 2-dia (feira/cozinha/preco), 3-relatorio.
 */
import { spawn, execSync } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import WebSocket from "ws";

const URL_JOGO = process.argv[2] ?? "http://localhost:8899/?seed=7";
const DIR = process.argv[3] ?? ".";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORTA = 9333;

const perfil = mkdtempSync(join(tmpdir(), "dindin-chrome-"));
const chrome = spawn(CHROME, [
  "--headless=new", "--disable-gpu", `--remote-debugging-port=${PORTA}`,
  `--user-data-dir=${perfil}`, "about:blank",
], { stdio: "ignore" });
process.on("exit", () => chrome.kill());

const espera = (ms) => new Promise((r) => setTimeout(r, ms));

// Acha o alvo websocket da primeira aba.
let alvo = null;
for (let i = 0; i < 50 && !alvo; i++) {
  await espera(200);
  try {
    const res = await fetch(`http://localhost:${PORTA}/json/list`);
    alvo = (await res.json()).find((t) => t.type === "page");
  } catch { /* chrome ainda subindo */ }
}
if (!alvo) { console.error("chrome nao respondeu"); process.exit(1); }

const ws = new WebSocket(alvo.webSocketDebuggerUrl, { maxPayload: 64 * 1024 * 1024 });
await new Promise((r) => ws.on("open", r));
let idMsg = 0;
const pendentes = new Map();
ws.on("message", (d) => {
  const m = JSON.parse(d);
  if (m.id && pendentes.has(m.id)) { pendentes.get(m.id)(m); pendentes.delete(m.id); }
});
const cdp = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++idMsg;
  pendentes.set(id, (m) => m.error ? reject(new Error(m.error.message)) : resolve(m.result));
  ws.send(JSON.stringify({ id, method, params }));
});
const js = async (expr) =>
  (await cdp("Runtime.evaluate", { expression: expr, returnByValue: true })).result.value;

// iPhone SE/13-mini: o menor viewport que ainda importa.
await cdp("Emulation.setDeviceMetricsOverride",
          { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
await cdp("Emulation.setTouchEmulationEnabled", { enabled: true });
await cdp("Page.enable");
await cdp("Page.navigate", { url: URL_JOGO });

// Espera o Pyodide carregar e a tela de regioes aparecer.
for (let i = 0; i < 120; i++) {
  await espera(500);
  if (await js("!!document.querySelector('.regiao')")) break;
}
if (!(await js("!!document.querySelector('.regiao')"))) {
  console.error("o jogo nao carregou (Pyodide?)"); process.exit(1);
}

const foto = async (nome) => {
  const { data } = await cdp("Page.captureScreenshot", { format: "png" });
  writeFileSync(join(DIR, nome), Buffer.from(data, "base64"));
  const overflow = await js(
    "document.documentElement.scrollWidth - document.documentElement.clientWidth");
  console.log(`${nome}  overflow-horizontal=${overflow}px`);
  return overflow;
};

let vazou = 0;
vazou += await foto("mobile-1-splash.png");

// Entra no Para e fotografa o dia (feira/cozinha no topo).
await js("[...document.querySelectorAll('.regiao')].find(c=>c.textContent.includes('chup-chup')).click()");
await espera(800);
vazou += await foto("mobile-2-dia.png");

// Compra, produz e vende pra chegar no relatorio.
await js(`
  const clicar = (nome, vezes) => {
    const tr = [...document.querySelectorAll("tr")]
      .find(r => r.textContent.includes(nome) && r.querySelector(".passo"));
    const mais = tr.querySelectorAll(".passo button")[1];
    for (let i = 0; i < vezes; i++) mais.click();
  };
  clicar("Polpa", 3); clicar("Açúcar", 1); clicar("Saquinho", 1);
`);
await espera(400);
await js(`
  const tr = [...document.querySelectorAll("#corpo-cozinha tr")][0];
  const mais = tr.querySelectorAll(".passo button")[1];
  for (let i = 0; i < 8; i++) mais.click();
`);
await espera(400);
await js("[...document.querySelectorAll('button')].find(b=>/Vender!|Sell!/.test(b.textContent)).click()");
await espera(800);
vazou += await foto("mobile-3-relatorio.png");

ws.close(); chrome.kill();
await espera(800);   // o Chrome ainda grava cache ao morrer; espera antes de varrer
try { execSync(`rm -rf ${JSON.stringify(perfil)} 2>/dev/null`); } catch {}

if (vazou > 0) { console.log("FALHOU: tem vazamento horizontal"); process.exit(1); }
console.log("VIEWPORT 375px SEM VAZAMENTO ✓");
