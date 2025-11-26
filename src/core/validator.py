from typing import List, Tuple
from ..utils.data_manager import GerenciadorDados

class ValidadorSolucao:
    def __init__(self, gerenciador_dados: GerenciadorDados):
        self.gerenciador_dados = gerenciador_dados
        self.unibrasil_id = gerenciador_dados.obter_id_unibrasil()
    
    def validar_solucao(self, rota: List[str], velocidades: List[int], 
                       tempos_pouso: List[bool]) -> Tuple[bool, str]:
        if not rota or rota[0] != "82821020" or rota[-1] != "82821020":
            return False, "Rota deve começar e terminar no Unibrasil"
        
        if len(rota) != len(velocidades) + 1 or len(rota) != len(tempos_pouso) + 1:
            return False, "Tamanhos inconsistentes"
        
        unibrasil_count = rota.count("82821020")
        if unibrasil_count != 2:
            return False, "Unibrasil deve aparecer apenas no início e fim"
        
        ceps_visitados = set(rota[1:-1])
        if len(ceps_visitados) < 1:
            return False, "Pelo menos um CEP deve ser visitado"
        
        if len(ceps_visitados) != len(rota) - 2:
            return False, "CEPs duplicados na rota"
        
        return True, "Solução válida"
    
    def validar_solucao_ids(self, rota_ids: List[int], velocidades: List[int], 
                           tempos_pouso: List[bool]) -> Tuple[bool, str]:
        if not rota_ids or len(rota_ids) < 3:
            return False, "Rota deve ter pelo menos 3 pontos"
        
        if rota_ids[0] != self.unibrasil_id or rota_ids[-1] != self.unibrasil_id:
            return False, "Rota deve começar e terminar no Unibrasil"
        
        if len(rota_ids) != len(velocidades) + 1 or len(rota_ids) != len(tempos_pouso) + 1:
            return False, "Tamanhos inconsistentes"
        
        unibrasil_count = rota_ids.count(self.unibrasil_id)
        if unibrasil_count != 2:
            return False, "Unibrasil deve aparecer apenas no início e fim"
        
        ids_visitados = set(rota_ids[1:-1])
        if len(ids_visitados) < 1:
            return False, "Pelo menos um CEP deve ser visitado"
        
        if len(ids_visitados) != len(rota_ids) - 2:
            return False, "CEPs duplicados na rota"
        
        return True, "Solução válida"