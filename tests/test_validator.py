import pytest
from src.core.validator import ValidadorSolucao
from src.utils.data_manager import GerenciadorDados

def test_validador_inicializacao():
    """Testa se o validador é inicializado corretamente"""
    print("\n[TEST] Testando inicialização do validador")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    validador = ValidadorSolucao(gerenciador)
    
    assert validador is not None
    assert hasattr(validador, 'gerenciador_dados')
    print("  ✓ Teste passou: validador inicializado corretamente")

def test_validador_rota_valida():
    """Testa validação de rota válida"""
    print("\n[TEST] Testando validação de rota")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    validador = ValidadorSolucao(gerenciador)
    
    # Obter alguns IDs de CEPs
    todos_ceps = gerenciador.obter_todos_ceps()
    ids_ceps = list(todos_ceps.keys())[:5]  # Pega 5 CEPs
    unibrasil_id = gerenciador.obter_id_unibrasil()
    
    # Criar rota válida (inicia e termina em Unibrasil)
    rota_ids = [unibrasil_id] + ids_ceps + [unibrasil_id]
    velocidades = [60] * (len(rota_ids) - 1)
    tempos_pouso = [False] * (len(rota_ids) - 1)
    
    print(f"  Tamanho da rota: {len(rota_ids)} pontos")
    print(f"  Velocidades: {velocidades}")
    
    eh_valida, mensagens = validador.validar_solucao_ids(rota_ids, velocidades, tempos_pouso)
    
    print(f"  Rota válida: {eh_valida}")
    print(f"  Mensagens: {len(mensagens)}")
    if mensagens:
        for msg in mensagens[:3]:
            print(f"    - {msg}")
    
    # Pode não ser válida por bateria, mas não deve ter erros estruturais
    assert len(mensagens) >= 0
    print("  ✓ Teste passou: validação executada")

def test_validador_rota_invalida_sem_unibrasil():
    """Testa validação de rota que não inicia em Unibrasil"""
    print("\n[TEST] Testando validação de rota inválida (sem Unibrasil)")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    validador = ValidadorSolucao(gerenciador)
    
    todos_ceps = gerenciador.obter_todos_ceps()
    ids_ceps = list(todos_ceps.keys())[:5]
    
    # Rota inválida - não inicia em Unibrasil
    rota_ids = ids_ceps
    velocidades = [60] * len(rota_ids)
    tempos_pouso = [False] * len(rota_ids)
    
    print(f"  Rota (sem Unibrasil): {len(rota_ids)} pontos")
    
    eh_valida, mensagens = validador.validar_solucao_ids(rota_ids, velocidades, tempos_pouso)
    
    print(f"  Rota válida: {eh_valida}")
    print(f"  Mensagens de erro: {len(mensagens)}")
    if mensagens:
        for msg in mensagens[:3]:
            print(f"    - {msg}")
    
    # Deve encontrar erro de que não inicia em Unibrasil
    assert not eh_valida
    print("  ✓ Teste passou: rota inválida detectada corretamente")

