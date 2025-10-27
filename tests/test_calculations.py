import pytest
from src.utils.calculations import haversine_distance, calculate_autonomy

def test_haversine_distance_pontos_proximos():
    """Testa cálculo de distância entre pontos próximos"""
    # Coordenadas em Curitiba (Unibrasil)
    ponto1 = (-25.422264, -49.264543)
    ponto2 = (-25.422000, -49.264000)
    
    distancia = haversine_distance(ponto1, ponto2)
    
    assert distancia > 0
    assert distancia < 1  # Menos de 1 km

def test_haversine_distance_mesmo_ponto():
    """Testa cálculo de distância com mesmo ponto"""
    ponto = (-25.422264, -49.264543)
    distancia = haversine_distance(ponto, ponto)
    
    assert distancia == 0

def test_calculate_autonomy_velocidade_media():
    """Testa cálculo de autonomia com velocidade média"""
    autonomia = calculate_autonomy(
        speed=60,  # 60 km/h
        base_autonomy=5000,
        correction_factor=0.93
    )
    
    # Autonomia deve ser um valor positivo
    assert autonomia > 0
    # Com 5000mAh e 60km/h, autonomia deve ser razoável
    assert autonomia < 7200  # Menos de 2 horas

def test_calculate_autonomy_velocidade_alta():
    """Testa que velocidades mais altas reduzem a autonomia"""
    autonomia_40 = calculate_autonomy(40, 5000, 0.93)
    autonomia_80 = calculate_autonomy(80, 5000, 0.93)
    
    # Velocidade maior deve resultar em menor autonomia
    assert autonomia_40 > autonomia_80

