import pytest
from src.algorithms.genetic_algorithm import AlgoritmoGenetico
from src.utils.data_manager import GerenciadorDados
from src.core.validator import ValidadorSolucao
from src.core.cost_calculator import CalculadorCusto

@pytest.fixture
def algoritmo_genetico():
    """Fixture para criar instância de algoritmo genético"""
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    validador = ValidadorSolucao(gerenciador)
    calculador = CalculadorCusto(gerenciador)
    algoritmo = AlgoritmoGenetico(gerenciador, validador, calculador)
    return algoritmo

def test_algoritmo_cria_individuo(algoritmo_genetico):
    """Testa criação de indivíduo válido"""
    rota_ids, velocidades, tempos_pouso = algoritmo_genetico.criar_individuo()
    
    # Verificar estrutura
    assert len(rota_ids) > 2
    assert len(velocidades) == len(rota_ids) - 1
    assert len(tempos_pouso) == len(rota_ids) - 1
    
    # Verificar que inicia e termina em Unibrasil
    unibrasil_id = algoritmo_genetico.unibrasil_id
    assert rota_ids[0] == unibrasil_id
    assert rota_ids[-1] == unibrasil_id

def test_algoritmo_cria_individuo_vizinho_mais_proximo(algoritmo_genetico):
    """Testa criação de indivíduo com estratégia do vizinho mais próximo"""
    rota_ids, velocidades, tempos_pouso = algoritmo_genetico.criar_individuo_vizinho_mais_proximo()
    
    assert len(rota_ids) > 2
    assert len(velocidades) == len(rota_ids) - 1
    assert len(tempos_pouso) == len(rota_ids) - 1
    
    # Verificar que inicia e termina em Unibrasil
    unibrasil_id = algoritmo_genetico.unibrasil_id
    assert rota_ids[0] == unibrasil_id
    assert rota_ids[-1] == unibrasil_id
    
    # Todos os CEPs devem estar presentes
    ids_ceps = algoritmo_genetico.ids_ceps
    assert len(rota_ids) == len(ids_ceps) + 2  # +2 para Unibrasil no início e fim

def test_algoritmo_muta_individuo(algoritmo_genetico):
    """Testa mutação de indivíduo"""
    individuo_original = algoritmo_genetico.criar_individuo()
    individuo_mutado = algoritmo_genetico.mutar(individuo_original)
    
    # Estrutura deve ser mantida
    assert len(individuo_original[0]) == len(individuo_mutado[0])
    assert len(individuo_original[1]) == len(individuo_mutado[1])
    assert len(individuo_original[2]) == len(individuo_mutado[2])

def test_algoritmo_crossover(algoritmo_genetico):
    """Testa operação de crossover"""
    pai1 = algoritmo_genetico.criar_individuo()
    pai2 = algoritmo_genetico.criar_individuo()
    
    filho1, filho2 = algoritmo_genetico.crossover(pai1, pai2)
    
    # Filhos devem ter mesma estrutura
    assert len(filho1[0]) == len(pai1[0])
    assert len(filho2[0]) == len(pai2[0])
    
    # Verificar que filhos também iniciam e terminam em Unibrasil
    unibrasil_id = algoritmo_genetico.unibrasil_id
    assert filho1[0][0] == unibrasil_id
    assert filho1[0][-1] == unibrasil_id
    assert filho2[0][0] == unibrasil_id
    assert filho2[0][-1] == unibrasil_id

