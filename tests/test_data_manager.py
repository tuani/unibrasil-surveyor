import pytest
from src.utils.data_manager import GerenciadorDados

def test_gerenciador_carrega_dados():
    """Testa se o gerenciador carrega os dados corretamente"""
    print("\n[TEST] Testando carregamento de dados")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    
    assert gerenciador is not None
    assert gerenciador.unibrasil_cep == "82821020"
    
    todos_ceps = gerenciador.obter_todos_ceps()
    print(f"  CEP Unibrasil: {gerenciador.unibrasil_cep}")
    print(f"  Total de CEPs carregados: {len(todos_ceps)}")
    print(f"  Coordenadas Unibrasil: {gerenciador.unibrasil_coords}")
    print("  ✓ Teste passou: dados carregados corretamente")

def test_gerenciador_converte_rota():
    """Testa conversão de rota de IDs para CEPs"""
    print("\n[TEST] Testando conversão de rota IDs para CEPs")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    
    unibrasil_id = gerenciador.obter_id_unibrasil()
    todos_ceps = gerenciador.obter_todos_ceps()
    
    rota_ids = [unibrasil_id, list(todos_ceps.keys())[0], unibrasil_id]
    print(f"  Rota em IDs: {rota_ids}")
    
    rota_ceps = gerenciador.converter_rota_para_ceps(rota_ids)
    print(f"  Rota em CEPs: {rota_ceps}")
    
    # Verificar que primeiro e último são Unibrasil
    assert rota_ceps[0] == "82821020"
    assert rota_ceps[-1] == "82821020"
    assert len(rota_ceps) == 3
    print("  ✓ Teste passou: conversão realizada corretamente")

def test_gerenciador_obtem_coordenadas():
    """Testa obtenção de coordenadas por CEP"""
    print("\n[TEST] Testando obtenção de coordenadas por CEP")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    
    coords = gerenciador.obter_coords_cep("82821020")
    print(f"  CEP: 82821020")
    print(f"  Coordenadas: {coords}")
    
    assert coords is not None
    assert len(coords) == 2
    assert coords[0] < 0  # Latitude de Curitiba (negativa)
    assert coords[1] < 0  # Longitude de Curitiba (negativa)
    print("  ✓ Teste passou: coordenadas obtidas corretamente (latitude e longitude negativas)")

def test_gerenciador_exclui_unibrasil():
    """Testa que lista de CEPs exclui Unibrasil"""
    print("\n[TEST] Testando exclusão de Unibrasil da lista de CEPs")
    gerenciador = GerenciadorDados("data/coordenadas.csv")
    
    todos_ceps = gerenciador.obter_todos_ceps()
    ids_sem_unibrasil = gerenciador.obter_ids_excluindo_unibrasil()
    
    print(f"  Total de CEPs: {len(todos_ceps)}")
    print(f"  IDs sem Unibrasil: {len(ids_sem_unibrasil)}")
    
    # IDs excluindo Unibrasil devem ser menos que total
    assert len(ids_sem_unibrasil) == len(todos_ceps) - 1
    # Unibrasil não deve estar na lista
    assert "82821020" not in [gerenciador.obter_cep_por_id(id) for id in ids_sem_unibrasil]
    print("  ✓ Teste passou: Unibrasil excluído corretamente da lista")

