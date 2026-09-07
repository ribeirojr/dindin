"""Guarda-corpo de balanceamento: a campanha tem que ser vencivel e a pericia
tem que compensar. Se um dia esses testes quebrarem, o jogo desbalanceou."""

import pytest

from dindin.content.regions import ORDEM_REGIOES
from tools.balance_sim import politica_competente, politica_ingenua, rodar

SEMENTES = range(8)


@pytest.mark.parametrize("regiao", ORDEM_REGIOES)
def test_jogador_competente_termina_a_campanha(regiao):
    dias = []
    for seed in SEMENTES:
        estado, dia, _ = rodar(regiao, seed, politica_competente)
        assert estado != "falencia", f"{regiao}/{seed} faliu jogando bem"
        if estado == "vitoria":
            dias.append(dia)
    assert len(dias) >= len(SEMENTES) - 1, f"{regiao}: so {len(dias)} vitorias"
    media = sum(dias) / len(dias)
    assert 30 <= media <= 75, f"{regiao}: campanha em {media:.0f} dias"


@pytest.mark.parametrize("regiao", ORDEM_REGIOES)
def test_jogar_bem_e_melhor_do_que_jogar_no_automatico(regiao):
    """A politica competente tem que vencer mais rapido que a ingenua."""
    def media_dias(pol):
        dias = [d for st, d, _ in (rodar(regiao, s, pol) for s in SEMENTES)
                if st == "vitoria"]
        return sum(dias) / len(dias) if dias else 999

    assert media_dias(politica_competente) < media_dias(politica_ingenua), regiao


@pytest.mark.parametrize("regiao", ORDEM_REGIOES)
def test_quase_ninguem_quebra_jogando_no_basico(regiao):
    """O piso suave e o socorro seguram quem joga no automatico.

    Nao e garantia absoluta: jogar mal numa regiao cara (SP) numa sequencia
    ruim de clima ainda pode custar o jogo -- e deve mesmo. O que nao pode
    e quebrar por travamento, que era o caso antes do socorro existir.
    """
    quebrou = sum(1 for seed in SEMENTES
                  if rodar(regiao, seed, politica_ingenua)[0] == "falencia")
    assert quebrou <= 1, f"{regiao}: {quebrou} falencias jogando no basico"


@pytest.mark.parametrize("regiao", ORDEM_REGIOES)
def test_jogador_competente_nunca_quebra(regiao):
    """Quem le a previsao e precifica direito nao pode perder."""
    for seed in SEMENTES:
        estado, _, _ = rodar(regiao, seed, politica_competente)
        assert estado != "falencia", f"{regiao}/{seed}"
