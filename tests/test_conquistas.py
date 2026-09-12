"""Persistencia das conquistas: o placar da campanha sobrevive a partida."""

import json

from dindin.persistence import conquistas


def test_sem_arquivo_comeca_zerado(tmp_path):
    assert conquistas.carregar(tmp_path / "nao_existe.json") == set()


def test_salvar_e_carregar(tmp_path):
    alvo = tmp_path / "c.json"
    conquistas.salvar({"ce", "df"}, alvo)
    assert conquistas.carregar(alvo) == {"ce", "df"}


def test_registrar_vitoria_soma_sem_apagar_o_que_tinha(tmp_path):
    alvo = tmp_path / "c.json"
    conquistas.registrar_vitoria("ce", alvo)
    depois = conquistas.registrar_vitoria("rj", alvo)
    assert depois == {"ce", "rj"}
    assert conquistas.carregar(alvo) == {"ce", "rj"}


def test_arquivo_corrompido_nao_derruba_o_jogo(tmp_path):
    """Melhor comecar a campanha do zero do que nao abrir o jogo."""
    alvo = tmp_path / "c.json"
    alvo.write_text("{isso nao e json", encoding="utf-8")
    assert conquistas.carregar(alvo) == set()


def test_versao_desconhecida_e_ignorada(tmp_path):
    alvo = tmp_path / "c.json"
    alvo.write_text(json.dumps({"versao": 99, "regioes": ["ce"]}),
                    encoding="utf-8")
    assert conquistas.carregar(alvo) == set()


def test_regiao_que_nao_existe_mais_nao_conta(tmp_path):
    alvo = tmp_path / "c.json"
    alvo.write_text(json.dumps({"versao": 1, "regioes": ["ce", "atlantida"]}),
                    encoding="utf-8")
    assert conquistas.carregar(alvo) == {"ce"}


def test_o_arquivo_gravado_e_json_legivel(tmp_path):
    alvo = tmp_path / "c.json"
    conquistas.salvar({"df"}, alvo)
    dados = json.loads(alvo.read_text(encoding="utf-8"))
    assert dados == {"versao": 1, "regioes": ["df"]}
