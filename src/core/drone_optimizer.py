from typing import List, Tuple
from datetime import datetime
from ..utils.data_manager import GerenciadorDados
from ..core.validator import ValidadorSolucao
from ..core.cost_calculator import CalculadorCusto
from ..algorithms.genetic_algorithm import AlgoritmoGenetico
from ..utils.report_generator import GeradorRelatorio
from ..visualization.route_plotter import PlotadorRota
from ..config import DRONE_CONFIG, OPERATION_CONFIG

class OtimizadorDrone:
    def __init__(self, csv_file: str = "data/coordenadas.csv"):
        self.gerenciador_dados = GerenciadorDados(csv_file)
        self.validador = ValidadorSolucao(self.gerenciador_dados)
        self.calculador_custo = CalculadorCusto(self.gerenciador_dados)
        self.algoritmo_genetico = AlgoritmoGenetico(
            self.gerenciador_dados, self.validador, self.calculador_custo
        )
        self.gerador_relatorio = GeradorRelatorio()
        self.plotador_rota = PlotadorRota(self.gerenciador_dados)
        
        self.drone_config = DRONE_CONFIG
        self.operation_config = OPERATION_CONFIG
    
    def executar_otimizacao(self) -> Tuple[List[str], List[int], List[bool], float]:
        rota_ids, velocidades, tempos_pouso, fitness = self.algoritmo_genetico.executar()
        rota_ceps = self.gerenciador_dados.converter_rota_para_ceps(rota_ids)
        return rota_ceps, velocidades, tempos_pouso, fitness
    
    def gerar_relatorios(self, rota: List[str], velocidades: List[int], 
                        tempos_pouso: List[bool], fitness: float):
        timestamp = datetime.now().strftime("%d%m%H%M%S")
        
        _, info = self.calculador_custo.calcular_custo_rota(rota, velocidades, tempos_pouso)
        info_rota = info["route_info"]
        
        arquivo_csv = f"output/roteiro_otimizado_{timestamp}.csv"
        arquivo_png = f"output/roteiro_visualizacao_{timestamp}.png"
        
        self.gerador_relatorio.gerar_csv_rota(rota, velocidades, tempos_pouso, info_rota, arquivo_csv)
        self.plotador_rota.plotar_rota(rota, arquivo_png)
        
        return arquivo_csv, arquivo_png