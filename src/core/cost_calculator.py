import math
from typing import List, Tuple, Dict
from ..utils.calculations import (
    haversine_distance, calculate_flight_angle, 
    calculate_effective_speed, calculate_autonomy
)
from ..utils.data_manager import GerenciadorDados
from ..config import DRONE_CONFIG, OPERATION_CONFIG

class CalculadorCusto:
    def __init__(self, gerenciador_dados: GerenciadorDados):
        self.gerenciador_dados = gerenciador_dados
        self.drone_config = DRONE_CONFIG
        self.operation_config = OPERATION_CONFIG
    
    def calcular_custo_rota(self, rota: List[str], velocidades: List[int], 
                          tempos_pouso: List[bool]) -> Tuple[float, Dict]:
        tempo_total = 0
        custo_total = 0
        bateria_atual = calculate_autonomy(velocidades[0], 
                                         self.drone_config['base_autonomy'],
                                         self.drone_config['autonomy_correction'])
        dia_atual = 1
        hora_atual = self.operation_config['start_hour']
        minuto_atual = 0
        segundo_atual = 0
        
        info_rota = []
        
        for i in range(len(rota) - 1):
            cep_inicial = rota[i]
            cep_final = rota[i + 1]
            velocidade = velocidades[i]
            pouso = tempos_pouso[i]
            
            coords_inicial = self.gerenciador_dados.obter_coords_cep(cep_inicial)
            coords_final = self.gerenciador_dados.obter_coords_cep(cep_final)
            
            distancia = haversine_distance(coords_inicial, coords_final)
            
            angulo_voo = calculate_flight_angle(coords_inicial, coords_final)
            
            velocidade_vento, direcao_vento = self.gerenciador_dados.obter_clima_por_horario(dia_atual, hora_atual)
            
            velocidade_efetiva = calculate_effective_speed(velocidade, velocidade_vento, direcao_vento, angulo_voo)
            
            tempo_voo = math.ceil(distancia / velocidade_efetiva * 3600)
            
            autonomia = calculate_autonomy(velocidade, 
                                       self.drone_config['base_autonomy'],
                                       self.drone_config['autonomy_correction'])
            consumo_bateria = tempo_voo * (self.drone_config['base_autonomy'] / autonomia)
            
            if bateria_atual < consumo_bateria + self.drone_config['stop_consumption']:
                pouso = True
                bateria_atual = calculate_autonomy(velocidade,
                                                 self.drone_config['base_autonomy'],
                                                 self.drone_config['autonomy_correction'])
                custo_total += self.drone_config['landing_cost'] if hora_atual >= 17 else 0
            else:
                bateria_atual -= consumo_bateria
            
            if pouso:
                bateria_atual -= self.drone_config['stop_consumption']
                custo_total += self.drone_config['landing_cost'] if hora_atual >= 17 else 0
            else:
                bateria_atual -= self.drone_config['stop_consumption']
            
            dia_inicio = dia_atual
            hora_inicio = hora_atual
            minuto_inicio = minuto_atual
            segundo_inicio = segundo_atual
            
            tempo_total += tempo_voo + self.drone_config['stop_consumption']
            
            total_segundos = tempo_voo + self.drone_config['stop_consumption']
            segundo_fim = segundo_atual + total_segundos
            minuto_fim = minuto_atual + segundo_fim // 60
            hora_fim = hora_atual + minuto_fim // 60
            dia_fim = dia_atual
            
            segundo_fim = segundo_fim % 60
            minuto_fim = minuto_fim % 60
            
            if hora_fim >= self.operation_config['end_hour']:
                dia_fim += 1
                hora_fim = self.operation_config['start_hour']
                if dia_fim > self.operation_config['max_days']:
                    return float('inf'), {"error": "Excedeu prazo de 7 dias"}
            
            dia_atual = dia_fim
            hora_atual = hora_fim
            minuto_atual = minuto_fim
            segundo_atual = segundo_fim
            
            info_rota.append({
                'start_cep': cep_inicial,
                'start_coords': coords_inicial,
                'day': dia_inicio,
                'start_hour': hora_inicio,
                'start_minute': minuto_inicio,
                'start_second': segundo_inicio,
                'speed': velocidade,
                'end_cep': cep_final,
                'end_coords': coords_final,
                'landing': pouso,
                'end_day': dia_fim,
                'end_hour': hora_fim,
                'end_minute': minuto_fim,
                'end_second': segundo_fim
            })
        
        return tempo_total + custo_total * 10, {
            "route_info": info_rota, 
            "total_time": tempo_total, 
            "total_cost": custo_total
        }
    
    def calcular_custo_rota_ids(self, rota_ids: List[int], velocidades: List[int], 
                               tempos_pouso: List[bool]) -> Tuple[float, Dict]:
        tempo_total = 0
        custo_total = 0
        bateria_atual = calculate_autonomy(velocidades[0], 
                                         self.drone_config['base_autonomy'],
                                         self.drone_config['autonomy_correction'])
        dia_atual = 1
        hora_atual = self.operation_config['start_hour']
        minuto_atual = 0
        segundo_atual = 0
        
        info_rota = []
        
        for i in range(len(rota_ids) - 1):
            id_inicial = rota_ids[i]
            id_final = rota_ids[i + 1]
            velocidade = velocidades[i]
            pouso = tempos_pouso[i]
            
            coords_inicial = self.gerenciador_dados.obter_coords_por_id(id_inicial)
            coords_final = self.gerenciador_dados.obter_coords_por_id(id_final)
            
            distancia = haversine_distance(coords_inicial, coords_final)
            
            angulo_voo = calculate_flight_angle(coords_inicial, coords_final)
            
            velocidade_vento, direcao_vento = self.gerenciador_dados.obter_clima_por_horario(dia_atual, hora_atual)
            
            velocidade_efetiva = calculate_effective_speed(velocidade, velocidade_vento, direcao_vento, angulo_voo)
            
            tempo_voo = math.ceil(distancia / velocidade_efetiva * 3600)
            
            autonomia = calculate_autonomy(velocidade, 
                                       self.drone_config['base_autonomy'],
                                       self.drone_config['autonomy_correction'])
            consumo_bateria = tempo_voo * (self.drone_config['base_autonomy'] / autonomia)
            
            if bateria_atual < consumo_bateria + self.drone_config['stop_consumption']:
                pouso = True
                bateria_atual = calculate_autonomy(velocidade,
                                                 self.drone_config['base_autonomy'],
                                                 self.drone_config['autonomy_correction'])
                custo_total += self.drone_config['landing_cost'] if hora_atual >= 17 else 0
            else:
                bateria_atual -= consumo_bateria
            
            if pouso:
                bateria_atual -= self.drone_config['stop_consumption']
                custo_total += self.drone_config['landing_cost'] if hora_atual >= 17 else 0
            else:
                bateria_atual -= self.drone_config['stop_consumption']
            
            dia_inicio = dia_atual
            hora_inicio = hora_atual
            minuto_inicio = minuto_atual
            segundo_inicio = segundo_atual
            
            tempo_total += tempo_voo + self.drone_config['stop_consumption']
            
            total_segundos = tempo_voo + self.drone_config['stop_consumption']
            segundo_fim = segundo_atual + total_segundos
            minuto_fim = minuto_atual + segundo_fim // 60
            hora_fim = hora_atual + minuto_fim // 60
            dia_fim = dia_atual
            
            segundo_fim = segundo_fim % 60
            minuto_fim = minuto_fim % 60
            
            if hora_fim >= self.operation_config['end_hour']:
                dia_fim += 1
                hora_fim = self.operation_config['start_hour']
                if dia_fim > self.operation_config['max_days']:
                    return float('inf'), {"error": "Excedeu prazo de 7 dias"}
            
            dia_atual = dia_fim
            hora_atual = hora_fim
            minuto_atual = minuto_fim
            segundo_atual = segundo_fim
            
            cep_inicial = self.gerenciador_dados.obter_cep_por_id(id_inicial)
            cep_final = self.gerenciador_dados.obter_cep_por_id(id_final)
            
            info_rota.append({
                'start_cep': cep_inicial,
                'start_coords': coords_inicial,
                'day': dia_inicio,
                'start_hour': hora_inicio,
                'start_minute': minuto_inicio,
                'start_second': segundo_inicio,
                'speed': velocidade,
                'end_cep': cep_final,
                'end_coords': coords_final,
                'landing': pouso,
                'end_day': dia_fim,
                'end_hour': hora_fim,
                'end_minute': minuto_fim,
                'end_second': segundo_fim
            })
        
        return tempo_total + custo_total * 10, {
            "route_info": info_rota, 
            "total_time": tempo_total, 
            "total_cost": custo_total
        }