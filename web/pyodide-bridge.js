/**
 * Ponte JS -> Pyodide -> dindin.bridge
 *
 * Carrega o interpretador Python no navegador, monta o codigo do jogo no
 * filesystem virtual e expoe a simulacao como funcoes JS normais.
 *
 * O ponto de tudo isso: sim/, content/ e i18n/ vao pro navegador SEM
 * NENHUMA alteracao. A economia que roda aqui e a mesma que os 117 testes
 * conferem no terminal.
 */

const PYODIDE_VERSION = "0.28.0";
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

// Arquivos do jogo que precisam ir pro FS virtual do Pyodide.
const MODULOS = [
  "__init__.py",
  "bridge.py",
  "sim/__init__.py", "sim/types.py", "sim/models.py", "sim/state.py",
  "sim/rng.py", "sim/demand.py", "sim/weather.py", "sim/calendar.py",
  "sim/freezer.py", "sim/events.py", "sim/economy.py", "sim/engine.py",
  "sim/progression.py",
  "content/__init__.py", "content/regions.py", "content/flavors.py",
  "content/ingredients.py", "content/locations.py", "content/event_pool.py",
  "i18n/__init__.py", "i18n/base_ptbr.py", "i18n/barks.py",
  "i18n/overrides/__init__.py", "i18n/overrides/ce.py", "i18n/overrides/rj.py",
  "i18n/overrides/mg.py", "i18n/overrides/sp.py", "i18n/overrides/rs.py",
  "i18n/overrides/pa.py",
];

export class DindinEngine {
  constructor() {
    this.pyodide = null;
    this.bridge = null;
    this.tempos = {};
  }

  /** Carrega o interpretador e o codigo do jogo. onProgresso(texto, pct). */
  async iniciar(onProgresso = () => {}) {
    const t0 = performance.now();

    onProgresso("Baixando o Python...", 5);
    if (!globalThis.loadPyodide) {
      await this._carregarScript(`${PYODIDE_CDN}pyodide.js`);
    }
    this.pyodide = await globalThis.loadPyodide({ indexURL: PYODIDE_CDN });
    this.tempos.interpretador = performance.now() - t0;

    onProgresso("Montando o jogo...", 70);
    const t1 = performance.now();
    await this._montarCodigo();
    this.tempos.modulos = performance.now() - t1;

    onProgresso("Ligando o fogão...", 92);
    const t2 = performance.now();
    this.bridge = this.pyodide.pyimport("dindin.bridge");
    this.tempos.importacao = performance.now() - t2;
    this.tempos.total = performance.now() - t0;

    onProgresso("Pronto!", 100);
    return this.tempos;
  }

  _carregarScript(src) {
    return new Promise((ok, erro) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = ok;
      s.onerror = () => erro(new Error(`falhou ao carregar ${src}`));
      document.head.appendChild(s);
    });
  }

  /** Escreve os .py no filesystem virtual, preservando a hierarquia. */
  async _montarCodigo() {
    const FS = this.pyodide.FS;
    for (const dir of ["/jogo", "/jogo/dindin", "/jogo/dindin/sim",
                       "/jogo/dindin/content", "/jogo/dindin/i18n",
                       "/jogo/dindin/i18n/overrides"]) {
      try { FS.mkdir(dir); } catch { /* ja existe */ }
    }

    const buscas = MODULOS.map(async (rel) => {
      const resp = await fetch(`./py/${rel}`);
      if (!resp.ok) throw new Error(`nao achei ${rel}`);
      return [rel, await resp.text()];
    });

    for (const [rel, codigo] of await Promise.all(buscas)) {
      FS.writeFile(`/jogo/dindin/${rel}`, codigo);
    }

    this.pyodide.runPython(`
import sys
if "/jogo" not in sys.path:
    sys.path.insert(0, "/jogo")
`);
  }

  /** Chama uma funcao da bridge e converte o retorno pra JS puro. */
  _call(nome, ...args) {
    const fn = this.bridge[nome];
    const py = fn(...args.map((a) => this.pyodide.toPy(a)));
    if (py && typeof py.toJs === "function") {
      const js = py.toJs({ dict_converter: Object.fromEntries });
      py.destroy();
      return js;
    }
    return py;
  }

  regioes() { return this._call("regioes"); }
  catalogo(regiao, desbloqueados) { return this._call("catalogo", regiao, desbloqueados ?? null); }
  novoJogo(regiao, seed) { return this._call("novo_jogo", regiao, seed); }
  previsao(estado) { return this._call("previsao", estado); }
  sabores(estado, carrinho, producao) {
    return this._call("sabores_do_jogador", estado, carrinho ?? {}, producao ?? {});
  }
  curvaDePreco(estado, flavor) { return this._call("curva_de_preco", estado, flavor); }
  jogarDia(estado, plano) { return this._call("jogar_dia", estado, plano); }
  mudarDePonto(estado, local) { return this._call("mudar_de_ponto", estado, local); }
  isopores(estado) { return this._call("isopores", estado); }
  comprarIsopor(estado, key) { return this._call("comprar_isopor", estado, key); }
  infoDoGelo(estado, unidades) { return this._call("info_do_gelo", estado, unidades); }

  /** Mede quanto custa simular N dias -- pra provar que velocidade nao e o gargalo. */
  benchmark(n = 200) {
    const estado = this.novoJogo("pa", 1);
    const plano = {
      compras: { polpa_comum: 3, acucar: 1, saquinho: 1 },
      producao: { coco: 40 }, precos: { coco: 190 }, gelo: 0,
    };
    const t0 = performance.now();
    for (let i = 0; i < n; i++) this.jogarDia(estado, plano);
    const dt = performance.now() - t0;
    return { dias: n, totalMs: +dt.toFixed(1), porDiaMs: +(dt / n).toFixed(3) };
  }
}
