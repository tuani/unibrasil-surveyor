import csv
from typing import List, Dict
from datetime import datetime

class GeradorRelatorio:
    def __init__(self):
        pass
    
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
    
    def gerar_relatorio_resumo(self, rota: List[str], velocidades: List[int], 
                             tempos_pouso: List[bool], custo_total: float, 
                             tempo_total: float, custo_pousos: float, 
                             arquivo_saida: str):
        with open(arquivo_saida, 'w', encoding='utf-8') as file:
            file.write("RELATÓRIO DE OTIMIZAÇÃO - UNIBRASIL SURVEYOR\n")
            file.write("=" * 50 + "\n\n")
            
            file.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            file.write(f"Total de CEPs: {len(rota) - 2}\n")
            file.write(f"Pontos na rota: {len(rota)}\n")
            file.write(f"Fitness (custo total): {custo_total:.2f}\n")
            file.write(f"Tempo total: {tempo_total:.2f} segundos\n")
            file.write(f"Custo de pousos: R$ {custo_pousos:.2f}\n")
            
            velocidade_media = sum(velocidades) / len(velocidades)
            file.write(f"Velocidade média: {velocidade_media:.1f} km/h\n")
            
            pousos = sum(tempos_pouso)
            percentual_pousos = (pousos / len(tempos_pouso)) * 100
            file.write(f"Pousos para recarga: {pousos} ({percentual_pousos:.1f}%)\n")
            
            file.write("\nPRIMEIROS 10 CEPs DA ROTA:\n")
            file.write("-" * 30 + "\n")
            for i, cep in enumerate(rota[:11]):
                file.write(f"{i+1:2d}. {cep}\n")
            
            file.write("\nÚLTIMOS 10 CEPs DA ROTA:\n")
            file.write("-" * 30 + "\n")
            for i, cep in enumerate(rota[-11:], len(rota)-10):
                file.write(f"{i:2d}. {cep}\n")