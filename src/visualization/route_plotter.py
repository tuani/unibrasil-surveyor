import matplotlib.pyplot as plt
from typing import List
from ..utils.data_manager import GerenciadorDados

class PlotadorRota:
    def __init__(self, gerenciador_dados: GerenciadorDados):
        self.gerenciador_dados = gerenciador_dados
        self.unibrasil_cep = gerenciador_dados.unibrasil_cep
        self.unibrasil_coords = gerenciador_dados.unibrasil_coords
    
    def plotar_rota(self, rota: List[str], arquivo_saida: str):
        plt.figure(figsize=(12, 10))
        
        todos_ceps = self.gerenciador_dados.obter_todos_ceps()
        todas_lats = [coords[0] for coords in todos_ceps.values()]
        todas_lons = [coords[1] for coords in todos_ceps.values()]
        plt.scatter(todas_lons, todas_lats, c='blue', s=20, alpha=0.6, label='CEPs')
        
        unibrasil_lat, unibrasil_lon = self.unibrasil_coords
        plt.scatter(unibrasil_lon, unibrasil_lat, c='red', s=100, marker='o', label='Unibrasil')
        plt.annotate('N', (unibrasil_lon, unibrasil_lat), ha='center', va='center', 
                    color='white', fontsize=12, fontweight='bold')
        
        lats_rota = [self.gerenciador_dados.obter_coords_cep(cep)[0] for cep in rota]
        lons_rota = [self.gerenciador_dados.obter_coords_cep(cep)[1] for cep in rota]
        plt.plot(lons_rota, lats_rota, 'b-', linewidth=2, alpha=0.8)
        
        plt.scatter(lons_rota, lats_rota, c='green', s=30, alpha=0.8)
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Rota Otimizada do Drone UNIBRASIL Surveyor')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plotar_evolucao_fitness(self, historico_fitness: List[float], arquivo_saida: str):
        plt.figure(figsize=(10, 6))
        plt.plot(historico_fitness)
        plt.xlabel('Geração')
        plt.ylabel('Fitness (Custo)')
        plt.title('Evolução do Fitness - Algoritmo Genético')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plotar_distribuicao_velocidades(self, velocidades: List[int], arquivo_saida: str):
        plt.figure(figsize=(10, 6))
        plt.hist(velocidades, bins=20, alpha=0.7, edgecolor='black')
        plt.xlabel('Velocidade (km/h)')
        plt.ylabel('Frequência')
        plt.title('Distribuição de Velocidades na Rota Otimizada')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()