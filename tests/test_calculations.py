import pytest
from src.utils.calculations import haversine_distance, calculate_autonomy

def test_haversine_distance_pontos_proximos():
    """Testa cálculo de distância entre pontos próximos"""
    print("\n[TEST] Testando distância Haversine entre pontos próximos")
    # Coordenadas em Curitiba (Unibrasil)
    ponto1 = (-25.422264, -49.264543)
    ponto2 = (-25.422000, -49.264000)
    
    distancia = haversine_distance(ponto1, ponto2)
    print(f"  Ponto 1: {ponto1}")
    print(f"  Ponto 2: {ponto2}")
    print(f"  Distância calculada: {distancia:.4f} km")
    
    assert distancia > 0
    assert distancia < 1  # Menos de 1 km
    print("  ✓ Teste passou: distância está entre 0 e 1 km")

def test_haversine_distance_mesmo_ponto():
    """Testa cálculo de distância com mesmo ponto"""
    print("\n[TEST] Testando distância Haversine com mesmo ponto")
    ponto = (-25.422264, -49.264543)
    distancia = haversine_distance(ponto, ponto)
    print(f"  Ponto: {ponto}")
    print(f"  Distância calculada: {distancia:.4f} km")
    
    assert distancia == 0
    print("  ✓ Teste passou: distância é zero para mesmo ponto")

def test_calculate_autonomy_velocidade_media():
    """Testa cálculo de autonomia com velocidade média"""
    print("\n[TEST] Testando cálculo de autonomia com velocidade média")
    autonomia = calculate_autonomy(
        speed=60,  # 60 km/h
        base_autonomy=5000,
        correction_factor=0.93
    )
    print(f"  Velocidade: 60 km/h")
    print(f"  Autonomia calculada: {autonomia:.2f} segundos ({autonomia/3600:.2f} horas)")
    
    # Autonomia deve ser um valor positivo
    assert autonomia > 0
    # Com 5000mAh e 60km/h, autonomia deve ser razoável
    assert autonomia < 7200  # Menos de 2 horas
    print("  ✓ Teste passou: autonomia está entre 0 e 2 horas")

def test_calculate_autonomy_velocidade_alta():
    """Testa que velocidades mais altas reduzem a autonomia"""
    print("\n[TEST] Testando que velocidade maior reduz autonomia")
    autonomia_40 = calculate_autonomy(40, 5000, 0.93)
    autonomia_80 = calculate_autonomy(80, 5000, 0.93)
    print(f"  Autonomia a 40 km/h: {autonomia_40:.2f} segundos ({autonomia_40/3600:.2f} horas)")
    print(f"  Autonomia a 80 km/h: {autonomia_80:.2f} segundos ({autonomia_80/3600:.2f} horas)")
    
    # Velocidade maior deve resultar em menor autonomia
    assert autonomia_40 > autonomia_80
    print(f"  ✓ Teste passou: autonomia a 40 km/h ({autonomia_40:.2f}) > autonomia a 80 km/h ({autonomia_80:.2f})")

