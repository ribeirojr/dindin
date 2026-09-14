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
  "sim/progression.py", "sim/campaign.py",
  "content/__init__.py", "content/regions.py", "content/flavors.py",
  "content/ingredients.py", "content/locations.py", "content/event_pool.py",
  "content/coolers.py",
  "i18n/__init__.py", "i18n/base_ptbr.py", "i18n/base_en.py", "i18n/barks.py",
  "i18n/overrides/__init__.py", "i18n/overrides/ce.py", "i18n/overrides/rj.py",
  "i18n/overrides/mg.py", "i18n/overrides/sp.py", "i18n/overrides/rs.py",
  "i18n/overrides/pa.py", "i18n/overrides/df.py",
];

/** pyodide.toPy() converte `null` num sentinela JsNull, nao em None -- entao
 * todo `is None`/`is not None` do lado Python fica sempre falso pra dados
 * que vieram de JSON.parse (ex: validade de lote sem vencimento, isopor
 * vazio). `undefined` converte certo pra None, entao troca antes de mandar.
 * Bug real: um save salvo (JSON no disco) restaurado derrubava o bridge
 * com "'<' not supported between instances of 'JsNull' and 'int'". */
function semNull(valor) {
  if (valor === null) return undefined;
  if (Array.isArray(valor)) return valor.map(semNull);
  if (valor && typeof valor === "object") {
    const out = {};
    for (const [k, v] of Object.entries(valor)) out[k] = semNull(v);
    return out;
  }
  return valor;
}

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
    const py = fn(...args.map((a) => this.pyodide.toPy(semNull(a))));
    if (py && typeof py.toJs === "function") {
      const js = py.toJs({ dict_converter: Object.fromEntries });
      py.destroy();
      return js;
    }
    return py;
  }

  regioes(lang, conquistas) {
    return this._call("regioes", lang ?? "pt", conquistas ?? []);
  }
  placarCampanha(conquistas) {
    return this._call("placar_campanha", conquistas ?? []);
  }
  registrarVitoria(conquistas, regiao) {
    return this._call("registrar_vitoria", conquistas ?? [], regiao);
  }
  textosBase(lang) { return this._call("textos_base", lang ?? "pt"); }
  catalogo(regiao, desbloqueados, lang) {
    return this._call("catalogo", regiao, desbloqueados ?? null, lang ?? "pt");
  }
  novoJogo(regiao, seed) { return this._call("novo_jogo", regiao, seed); }
  previsao(estado) { return this._call("previsao", estado); }
  sabores(estado, carrinho, producao, lang) {
    return this._call("sabores_do_jogador", estado, carrinho ?? {},
                      producao ?? {}, lang ?? "pt");
  }
  curvaDePreco(estado, flavor) { return this._call("curva_de_preco", estado, flavor); }
  jogarDia(estado, plano) { return this._call("jogar_dia", estado, plano); }
  mudarDePonto(estado, local) { return this._call("mudar_de_ponto", estado, local); }
  restaurarEstado(estado) { return this._call("restaurar_estado", estado); }
  isopores(estado, lang) { return this._call("isopores", estado, lang ?? "pt"); }
  comprarIsopor(estado, key) { return this._call("comprar_isopor", estado, key); }
  infoDoGelo(estado, unidades) { return this._call("info_do_gelo", estado, unidades); }

  /** Prepara um namespace Python isolado pro REPL de aprendizado -- nao
   * compartilha nada com dindin.bridge, entao o aluno nao consegue nem
   * atrapalhar o jogo nem "trapacear" mexendo no estado por dentro. */
  _replNamespace() {
    if (!this._replNs) {
      this._replNs = this.pyodide.runPython(
        "import code as _code, sys\n" +
        "_repl_ns = {'__name__': '__console__', '__doc__': None}\n" +
        "_repl_ns"
      );
    }
    return this._replNs;
  }

  /** Roda uma linha (ou bloco) de codigo como um REPL de verdade: se a
   * ultima linha for uma expressao, mostra o repr() dela (igual o >>> do
   * terminal). Devolve { saida, erro }. */
  rodarRepl(codigoFonte) {
    this._replNamespace();
    this.pyodide.globals.set("_repl_fonte", codigoFonte);
    const resultado = this.pyodide.runPython(`
import contextlib, io, traceback

_saida_buf = io.StringIO()
_erro = None
try:
    try:
        _compilado = compile(_repl_fonte, "<repl>", "single")
    except SyntaxError:
        _compilado = compile(_repl_fonte, "<repl>", "exec")
    with contextlib.redirect_stdout(_saida_buf), contextlib.redirect_stderr(_saida_buf):
        exec(_compilado, _repl_ns)
except SystemExit:
    _erro = None
except BaseException:
    _erro = "".join(traceback.format_exception_only(*sys.exc_info()[:2])).strip()

(_saida_buf.getvalue(), _erro)
`);
    const [saida, erro] = resultado.toJs();
    resultado.destroy();
    return { saida, erro };
  }

  /** Zera o namespace do REPL (comando "reiniciar"). */
  reiniciarRepl() {
    this._replNs = null;
    this._replNamespace();
  }

  versaoPython() {
    return this.pyodide.runPython("import sys; '.'.join(map(str, sys.version_info[:3]))");
  }

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
