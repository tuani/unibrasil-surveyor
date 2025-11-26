import matplotlib.pyplot as plt
from typing import List
from ..utils.data_manager import GerenciadorDados

class PlotadorRota:
    def __init__(self, gerenciador_dados: GerenciadorDados):
        self.gerenciador_dados = gerenciador_dados
        self.unibrasil_cep = gerenciador_dados.unibrasil_cep
        self.unibrasil_coords = gerenciador_dados.unibrasil_coords
    
    def plotar_rota(self, rota: List[str], arquivo_saida: str):
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            try:
                plt.style.use('seaborn-darkgrid')
            except:
                plt.style.use('default')
        
        fig, ax = plt.subplots(figsize=(14, 11))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f8f9fa')
        
        lats_rota = [self.gerenciador_dados.obter_coords_cep(cep)[0] for cep in rota]
        lons_rota = [self.gerenciador_dados.obter_coords_cep(cep)[1] for cep in rota]
        
        ax.plot(lons_rota, lats_rota, color='#0d6efd', linewidth=2.5, 
               alpha=0.7, zorder=2, label='Rota do Drone')
        
        ax.scatter(lons_rota[1:-1], lats_rota[1:-1], c='#198754', s=40, 
                  alpha=0.8, edgecolors='white', linewidths=1, zorder=3, label='Pontos Visitados')
        
        unibrasil_lat, unibrasil_lon = self.unibrasil_coords
        ax.scatter(unibrasil_lon, unibrasil_lat, c='#dc3545', s=400, 
                  marker='*', label='Unibrasil', zorder=10, 
                  edgecolors='white', linewidths=2)
        
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.set_title('Rota do Drone UNIBRASIL Surveyor', 
                    fontsize=16, fontweight='bold', pad=20)
        
        ax.legend(loc='upper right', frameon=True, fancybox=True, 
                 shadow=True, fontsize=10, framealpha=0.95)
        
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dee2e6')
        ax.spines['bottom'].set_color('#dee2e6')
        
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()