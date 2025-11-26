import csv
from typing import Dict, Tuple, List
from ..config import CSV_FILE, WEATHER_DATA
from .id_mapper import MapeadorID

class GerenciadorDados:
    def __init__(self, csv_file: str = CSV_FILE):
        self.csv_file = csv_file
        self.mapeador_id = MapeadorID()
        self.ceps = self._carregar_ceps()
        self.unibrasil_cep = "82821020"
        self.unibrasil_id = self.mapeador_id.definir_unibrasil(self.unibrasil_cep)
        self.unibrasil_coords = self._obter_coords_unibrasil()
        self.weather_data = WEATHER_DATA
    
    def _carregar_ceps(self) -> Dict[str, Tuple[float, float]]:
        ceps = {}
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cep = row['cep']
                    lat = float(row['latitude'])
                    lon = float(row['longitude'])
                    ceps[cep] = (lat, lon)
                    self.mapeador_id.adicionar_cep(cep)
        except FileNotFoundError:
            print(f"ERRO: Arquivo {self.csv_file} não encontrado!")
            return {}
        except Exception as e:
            print(f"ERRO ao carregar dados: {e}")
            return {}
        
        return ceps
    
    def _obter_coords_unibrasil(self) -> Tuple[float, float]:
        return self.ceps.get(self.unibrasil_cep, (0, 0))
    
    def obter_clima_por_horario(self, dia: int, hora: int) -> Tuple[int, str]:
        if dia not in self.weather_data:
            return (0, "N")
        
        available_hours = sorted(self.weather_data[dia].keys())
        closest_hour = min(available_hours, key=lambda x: abs(x - hora))
        
        wind_speed, wind_direction = self.weather_data[dia][closest_hour]
        return wind_speed, wind_direction
    
    def obter_coords_por_id(self, id_cep: int) -> Tuple[float, float]:
        cep = self.mapeador_id.obter_cep_id(id_cep)
        return self.ceps.get(cep, (0, 0))
    
    def obter_coords_cep(self, cep: str) -> Tuple[float, float]:
        return self.ceps.get(cep, (0, 0))
    
    def obter_cep_por_id(self, id_cep: int) -> str:
        return self.mapeador_id.obter_cep_id(id_cep)
    
    def obter_ids_excluindo_unibrasil(self) -> List[int]:
        return self.mapeador_id.obter_ids_excluindo_unibrasil()
    
    def obter_id_unibrasil(self) -> int:
        return self.mapeador_id.obter_id_unibrasil()
    
    def converter_rota_para_ceps(self, rota_ids: List[int]) -> List[str]:
        return self.mapeador_id.converter_rota_para_ceps(rota_ids)
    
    def obter_todos_ceps(self) -> Dict[str, Tuple[float, float]]:
        return self.ceps.copy()