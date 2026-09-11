# DinDin — instructions for AI contributors

Terminal + web game about selling homemade popsicles ("dindin") across Brazil.
Python 3.14, managed with `uv`. TUI in Textual; web version runs the SAME
Python simulation in the browser via Pyodide.

## Commands

```bash
uv run pytest                        # full Python suite — must pass before any commit
uv run python tools/build_web.py     # copies sim/content/i18n into web/py (required before web tests)
node tests/web/dom_test.mjs          # web UI in a real DOM (jsdom + real Pyodide)
node tests/web/isopor_gelo_test.mjs  # web cooler/ice flow
uv run dindin                        # play the TUI
uv run python tools/serve_web.py     # serve web version on the LAN
uv run python tools/balance_sim.py   # balance harness (auto-players over many seeds)
```

Run `uv run pytest` after every change. Run the two `node` tests whenever you
touch `web/`, `bridge.py`, or anything the web bundle ships (`sim/`,
`content/`, `i18n/`) — and build `web/py` first or they test stale code.

## Architecture (load-bearing — do not violate)

```
src/dindin/
  sim/          pure simulation. NEVER import textual/rich here (AST test enforces it).
  content/      data only: regions, flavors, ingredients, locations, coolers, events.
  i18n/         base pt-BR strings + per-state overrides. sim/ returns KEYS, never text.
  ui/           Textual screens/widgets. No game rules here — call sim/.
  bridge.py     JSON-only boundary for the browser. Only dict/list/str/int/float/bool/None.
  persistence/  save/load to JSON (not shipped to web; web keeps state in JS).
web/            static site. app.js draws what bridge returns; knows NO game rules.
tools/          build_web.py, serve_web.py, balance_sim.py.
```

### Hard rules

1. **`sim/` is pure.** No I/O, no `textual`/`rich` imports, no global `random`.
   All randomness goes through `sim/rng.stream(seed, dia, canal)`.
2. **Never use `hash()` for RNG or anything persisted.** Python randomizes str
   hashes per process; it breaks seed replay. `rng.py` uses blake2b; a test
   asserts `hash` is never called there.
3. **Determinism:** same seed + same plans ⇒ identical game, in any process.
   If you add a new source of randomness, derive it from `stream()` with its
   own channel name (e.g. `stream(seed, dia, "meu_canal")`).
4. **The bridge speaks JSON only.** No dataclass, enum, or Python object may
   cross `bridge.py`. Anything added to `estado_para_json` MUST be read back
   in `estado_de_json` (round-trip), or the browser silently loses state every
   day — this exact bug class happened with `socorro_usado` and lot expiry.
5. **sim/ emits i18n keys, never text.** Events carry `text_key` like
   `"evento.chuva_das_duas"`; the UI translates via `Translator.t()`. New keys
   go in `i18n/base_ptbr.py`; regional flavor goes in `i18n/overrides/<uf>.py`
   (only keys that exist in BASE — a test enforces this).
   **Every new BASE key needs its English twin in `i18n/base_en.py`**
   (`tests/i18n/test_en.py` enforces exact key parity). The web UI supports
   `lang="pt"|"en"` (picker on the splash, `?lang=en` in the URL); the TUI is
   pt-only. Regional product names (dindin, sacolé…) and street slang are
   diegetic — never translate them. Content names (flavors, ingredients,
   coolers) resolve via `sabor.<key>` / `insumo.<key>` / `isopor.nome.<key>`
   keys: pt is auto-generated from `content/`, EN is written by hand.
   No hardcoded user-facing strings in `web/app.js` — always `t()`.
6. **New file under `sim/`, `content/`, or `i18n/`?** Add it to `MODULOS` in
   `web/pyodide-bridge.js`. `tests/test_web_bundle.py` fails if you forget —
   without it the browser 404s at runtime.
7. **Money is `int` centavos everywhere** (`Centavos` type alias). Format only
   at the edge with `i18n.money()`.
8. **State changes must round-trip through BOTH persisted forms:** the save
   file (`persistence/save.py`, read old saves with `.get(...)` defaults) and
   the bridge JSON (`estado_para_json`/`estado_de_json`). Add a round-trip
   test for every new `GameState` field.

## Conventions

- Code, comments, tests, and commit messages are in Portuguese. Comments use
  plain ASCII (no accents: "nao", "e" for "é"); player-facing strings use full
  accents.
- Comments explain design intent ("why"), not mechanics. Keep that style.
- Dataclasses: content/models are `frozen=True, slots=True`; mutable game
  state lives in `sim/state.py`.
- Test names are sentences: `test_sem_isopor_nao_vende_na_rua`. Docstrings on
  tests explain the bug or invariant they guard.
- The TUI and web are parallel UIs over the same sim. A gameplay fix belongs
  in `sim/` or `bridge.py` so both get it; if you must change UI flow, check
  whether `ui/app.py` (terminal) and `web/app.js` (browser) both need it.

## Recipes

- **New flavor:** add a `Flavor` in `content/flavors.py` (recipe = ingredients
  per 10 units, `desbloqueio` = location key or None). If it needs a new
  ingredient, add it to `content/ingredients.py` AND `DESBLOQUEIO_INSUMO`
  (unlock no later than the flavor, or `test_cadencia` fails).
- **New event:** add a `GameEvent` in `content/event_pool.py` + a
  `evento.<key>` string in `base_ptbr.py`. Regional events list their
  `regioes`; location-bound events list `locais`.
- **New region:** `content/regions.py` (climate per season must be a
  probability dist), `i18n/overrides/<uf>.py`, barks in `i18n/barks.py`,
  add to `REGIOES_I18N`, and difficulty/climate blurbs in
  `ui/screens/region_select.py`. Tests enforce a unique product name.
- **Balance change:** run `uv run python tools/balance_sim.py 30` before and
  after. `tests/sim/test_balance.py` is the guard-rail: a competent player
  wins in 30–75 days on 8 seeds, a naive one survives.

## Gotchas

- `pyproject.toml` disables the pytest cache on purpose (stale `.pyc` from
  `tools/` caused phantom failures) — don't re-enable it.
- `plan.gelo` is bought by the engine itself (clamped to cash); ice is NOT a
  market item — keep it out of `insumos_disponiveis` (test enforces).
- Web tests need `node_modules` (`npm ci` if missing) and a fresh
  `web/py` build.
- The day always starts at `progression.melhor_local(state)` (furthest
  unlocked point); falling back to "casa" for a day must never overwrite the
  player's real point permanently, or they get stuck at home.
- `DATA_INICIAL` in `engine.py` anchors day numbers to real calendar dates
  (seasons, holidays). Changing it changes every seeded game.
