import csv
from typing import List, Dict
from datetime import datetime

class GeradorRelatorio:
    def gerar_csv_rota(self, rota: List[str], velocidades: List[int], 
                      tempos_pouso: List[bool], info_rota: List[Dict], 
                      arquivo_saida: str):
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'CEP inicial', 'Latitude inicial', 'Longitude inicial',
                'Dia do voo', 'Hora inicial', 'Velocidade',
                'CEP final', 'Latitude final', 'Longitude final',
                'Pouso', 'Hora final'
            ])
            
            for i, info in enumerate(info_rota):
                coords_inicial = info['start_coords']
                coords_final = info['end_coords']
                
                hora_inicio = f"{info['start_hour']:02d}:{info['start_minute']:02d}:{info['start_second']:02d}"
                hora_fim = f"{info['end_hour']:02d}:{info['end_minute']:02d}:{info['end_second']:02d}"
                
                writer.writerow([
                    info['start_cep'],
                    f"{coords_inicial[0]:.15f}",
                    f"{coords_inicial[1]:.15f}",
                    info['day'],
                    hora_inicio,
                    info['speed'],
                    info['end_cep'],
                    f"{coords_final[0]:.15f}",
                    f"{coords_final[1]:.15f}",
                    "SIM" if info['landing'] else "NÃO",
                    hora_fim
                ])