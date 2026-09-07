# DinDin na web (Pyodide)

Protótipo: o jogo rodando no navegador **sem reescrever a simulação**.

## Rodar

```bash
uv run python tools/build_web.py     # copia sim/ content/ i18n/ pro web/py
cd web && python3 -m http.server 8765
# abre http://localhost:8765
```

## Como funciona

```
React/JS  ──┐
            ├─ pyodide-bridge.js ─ Pyodide (CPython em WASM) ─ dindin/bridge.py
CSS/SVG   ──┘                                                        │
                                                    sim/ content/ i18n/  ← INTACTOS
```

`web/py/` é **cópia literal** de `src/dindin/{sim,content,i18n}` — sem
nenhuma alteração. Os mesmos 131 testes que rodam no terminal cobrem
exatamente o código que vai pro navegador. `ui/` (Textual) e
`persistence/` (arquivo) ficam de fora: um não roda no browser, o outro
vira `localStorage`.

A única peça nova do lado Python é `bridge.py` (~230 linhas), que só faz
serialização: entra e sai JSON puro, nada de dataclass ou enum atravessa
a fronteira.

## Medições reais (Pyodide 0.28, Node)

| | |
|---|---|
| Boot do interpretador | 932 ms |
| Montar 31 módulos no FS virtual | 7 ms |
| Importar a bridge | 48 ms |
| **Simular um dia** | **0.183 ms** |
| Orçamento de um frame a 60fps | 16.7 ms |
| **Uso da simulação por frame** | **1.1%** |

A lentidão do Pyodide (3–10x nativo) é irrelevante aqui: o jogo é por
turnos e a conta mais pesada é aritmética sobre ~20 sabores. O custo real
é o download (~6MB) e o boot, que a tela de carregamento absorve.

## O que a web ganha

O **gráfico da curva de preço** — no terminal era uma barra de 20
caracteres; aqui é a curva de demanda de verdade, com a área de lucro
sombreada, a linha do custo e um losango no preço de lucro máximo. É o
elemento mais importante do ensino do jogo, e é o que justifica o porte.

## O que falta pra virar produto

- [ ] Service worker pra cachear o Pyodide (segunda visita = instantâneo)
- [ ] `localStorage` no lugar de `persistence/save.py`
- [ ] Seeds na URL pra comparar partidas (`?r=pa&seed=77`)
- [ ] Upgrades e escolha de ponto no capítulo 5
- [ ] Rodar o Pyodide num Web Worker (não travar a UI no boot)
