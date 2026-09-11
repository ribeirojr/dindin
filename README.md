# DinDin

Um jogo de terminal sobre a vida de quem vende gelado no Brasil — tipo o
*Lemonade Stand* de 1979, mas com dindin, isopor e chuva das duas.

```
   ___  _         ___  _
  |   \(_)_ _  __| (_)_ _
  | |) | | ' \/ _` | | ' \
  |___/|_|_||_\__,_|_|_||_|
```

## Como jogar

```bash
uv run dindin
```

## O que é um dindin?

É o picolé caseiro de saquinho: você enche o plástico com polpa de fruta,
leite condensado ou açaí, amarra, congela e vende no isopor. Só que o nome
muda de estado pra estado — e é aí que mora a graça do jogo.

Ao começar, você escolhe de onde é. **Isso muda o vocabulário e a economia:**

| Estado | O doce se chama | Gíria | Como é vender lá |
| --- | --- | --- | --- |
| Ceará | **dindin** | vixe, arretado, ma broca | Calor o ano inteiro, mas o povo não paga caro |
| Rio de Janeiro | **sacolé** | caraca, sinistro, mermão | Praia cheia, temporal sem avisar |
| Minas Gerais | **laranjinha** | uai, trem bão, sô | Milho verde é rei, inverno atrapalha |
| São Paulo | **geladinho** | meu, mano, da hora | Aceita preço alto, mas insumo é caro |
| Rio Grande do Sul | **gelinho** | bah, tchê, guria | Verão ótimo, inverno congela as vendas |
| Pará | **chup-chup** | égua, maninho, pai d'égua | Açaí vende sozinho, chove toda tarde |

O mesmo acontecimento sai diferente em cada estado:

```
CE:  Arretado! Vendeu tudim — 42 ficaram na vontade.
PA:  Pai d'égua! Vendeu tudo — 42 ficaram na vontade.
RS:  Bah, tri! Vendeu tudo — 42 ficaram na vontade.
```

## O dia a dia

O dia se divide em **planejar** e **executar**. Primeiro você vê o seu ponto
desenhado, a previsão do tempo, quanto tem no caixa e quanto falta pra meta.
Só depois começa a gastar dinheiro:

1. **Feira** — compra polpa, açúcar e saquinho. Comprando mais, sai mais barato.
2. **Cozinha** — decide quantos vai fazer. O que passar da capacidade do freezer derrete.
3. **Gelo** — fora de casa, quanto gelo levar pro isopor. No calor o gelo rende
   menos (um saco segura 50 num dia ameno, 30 num sol de rachar), então o dia
   que mais vende é o que mais exige gelo.
4. **Preço** — o *termômetro* mostra o que a freguesia acha do valor.
5. **Vender** — o dia acontece e sai o relatório.

### Aprendendo aos poucos

O jogo não joga tudo na sua cara de uma vez. No dia 1 são **3 sabores e 4
insumos** — dá pra entender o ciclo inteiro sem se perder. Cada ponto novo
abre mais:

| Ponto | Sabores | Insumos | O que aparece |
| --- | --- | --- | --- |
| Freezer de casa | 3 | 4 | Coco, limão, maracujá |
| Isopor na rua | 9 | 7 | Leite condensado, polpa premium → os cremosos |
| Praia | 15 | 7 | Doce de leite, tapioca, bacuri |
| Escola | 17 | 8 | Creme de avelã → Ninho com Nutella |

### O isopor

Vender na rua exige uma caixa de isopor — e caixa de isopor não dura pra
sempre. É **compra única que cobre vários dias**, não um custo diário:

| Caixa | Preço | Dura | Cabe | Derrete | Sai por |
| --- | --- | --- | --- | --- | --- |
| Isopor simples | R$ 25 | 14 dias | 100 | 100% | R$ 1,79/dia |
| Isopor reforçado | R$ 60 | 28 dias | 130 | 55% | R$ 2,14/dia |
| Caixa térmica | R$ 130 | 45 dias | 150 | 40% | R$ 2,89/dia |

A caixa cara sai um pouco mais por dia, mas **cabe mais e derrete menos** —
então a decisão é de capital: tenho R$130 sobrando agora pra ganhar mais
depois, ou compro a barata e reponho toda quinzena? Quando ela racha, o
jogo avisa na gíria da região ("Égua, o Isopor simples rachou de vez,
maninho") e sem caixa nova você não abre o ponto.

O número mais importante do relatório é **"queriam comprar"**. Se ele for
maior que o que você levou, faltou mercadoria — faça mais amanhã. Se sobrou,
você fez demais. É esse número que transforma o jogo em algo que se aprende
em vez de adivinhar.

O calor manda em tudo: dia de sol de rachar vende o dobro, e ainda dá pra
cobrar mais caro. Chuva mata a venda na rua.

## A campanha

Cinco pontos de venda, cada um com uma meta em caixa:

| # | Ponto | Meta | O que muda |
| --- | --- | --- | --- |
| 1 | Freezer de casa | R$ 150 | Seguro e pequeno. Aprende o básico sem risco. |
| 2 | Isopor na rua | R$ 400 | Precisa comprar (e repor) a caixa; gelo vira despesa e a chuva dói. |
| 3 | Praia | R$ 1.000 | Onde o gourmet finalmente compensa. E onde a chuva arrasa. |
| 4 | Portão da escola | R$ 2.000 | Criança não paga caro: a estratégia da praia não serve mais. |
| 5 | Carrinho próprio | R$ 5.000 | Escolhe o ponto a cada dia conforme a previsão. |

O capítulo da escola é de propósito um passo atrás em preço e gourmet — ele
existe pra invalidar a estratégia que ganhou na praia.

## Versão web (protótipo)

O mesmo jogo roda no navegador via **Pyodide** — CPython compilado pra
WebAssembly. A camada `sim/`, `content/` e `i18n/` vai pro browser **sem
uma linha alterada**; só entra um módulo novo de serialização JSON
(`bridge.py`). Simular um dia custa **0.183 ms** lá dentro, ou 1.1% de um
frame — velocidade nunca é o gargalo num jogo por turnos.

```bash
uv run python tools/build_web.py
cd web && python3 -m http.server 8765
```

Detalhes e medições em [`web/README.md`](web/README.md).

## Desenvolvimento

```bash
uv sync                              # instala tudo
uv run pytest                        # 202 testes
npm test                             # testa a versão web num DOM real
uv run python tools/balance_sim.py   # confere o balanceamento
```

### Como o código é dividido

```
src/dindin/
  sim/        simulação pura — não importa textual, roda sem terminal
  content/    dados: regiões, sabores, insumos, pontos, eventos
  i18n/       tradutor regional (base pt-BR + override por estado)
  ui/         Textual: telas e widgets
  bridge.py   ponte JSON pro navegador (Pyodide)
```

A regra que segura o projeto: **`sim/` é uma função pura**. Isso deixa a
economia inteira testável sem abrir terminal — dá pra rodar milhares de dias
com semente fixa pra balancear. Tem um teste que faz parse da AST e falha se
alguém importar `textual` lá dentro.

O `tools/balance_sim.py` roda duas políticas automáticas (um jogador
competente e um no automático) em várias sementes. Hoje o competente fecha a
campanha em 38–56 dias e o ingênuo em ~70 — ou seja, jogar bem compensa, mas
jogar mal não te elimina.
