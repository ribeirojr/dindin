"""Mesma semente + mesmos planos = mesmo resultado, sempre."""

from dataclasses import asdict

from dindin.sim.engine import advance_day
from dindin.sim.state import DayPlan, GameState


def _rodar(seed: int, regiao: str = "pa"):
    s = GameState(seed=seed, regiao=regiao, local_atual="casa")
    saida = []
    for _ in range(20):
        plan = DayPlan(
            producao={"coco": 25}, precos={"coco": 210}, local="casa",
            compras={"polpa_comum": 2, "acucar": 1, "saquinho": 1},
        )
        saida.append(asdict(advance_day(s, plan)))
    return saida, s


def test_mesma_semente_mesmo_resultado():
    a, sa = _rodar(1234)
    b, sb = _rodar(1234)
    assert a == b
    assert sa.caixa == sb.caixa
    assert sa.reputacao == sb.reputacao


def test_sementes_diferentes_divergem():
    a, _ = _rodar(1)
    b, _ = _rodar(2)
    assert a != b


def test_clima_e_estavel_para_a_mesma_semente():
    from dindin.sim.engine import clima_do_dia

    s = GameState(seed=42, regiao="ce")
    primeiro = [clima_do_dia(s, d).kind for d in range(1, 30)]
    segundo = [clima_do_dia(s, d).kind for d in range(1, 30)]
    assert primeiro == segundo


def test_semente_da_o_mesmo_jogo_em_qualquer_processo():
    """hash() de str e randomizado por processo: usar isso no rng fazia a
    mesma semente virar jogos diferentes a cada execucao."""
    import subprocess
    import sys
    from pathlib import Path

    raiz = Path(__file__).resolve().parents[2]
    codigo = (
        "import sys; sys.path.insert(0, 'src');"
        "from dindin.sim.rng import stream;"
        "print(stream(77, 1, 'clima').random())"
    )
    saidas = {
        subprocess.run([sys.executable, "-c", codigo], cwd=raiz,
                       capture_output=True, text=True, check=True).stdout.strip()
        for _ in range(3)
    }
    assert len(saidas) == 1, f"rng mudou entre processos: {saidas}"


def test_rng_nao_usa_hash_de_string():
    """Guarda-corpo: hash() aqui reintroduz o bug de forma silenciosa."""
    import ast
    from pathlib import Path

    fonte = (Path(__file__).resolve().parents[2]
             / "src" / "dindin" / "sim" / "rng.py").read_text(encoding="utf-8")
    chamadas = {
        n.func.id for n in ast.walk(ast.parse(fonte))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    assert "hash" not in chamadas
