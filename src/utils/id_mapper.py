from typing import Dict, List, Tuple

class MapeadorID:
    def __init__(self):
        self.cep_to_id: Dict[str, int] = {}
        self.id_to_cep: Dict[int, str] = {}
        self.next_id = 0
        self.unibrasil_id = None
    
    def adicionar_cep(self, cep: str) -> int:
        if cep not in self.cep_to_id:
            self.cep_to_id[cep] = self.next_id
            self.id_to_cep[self.next_id] = cep
            self.next_id += 1
        return self.cep_to_id[cep]
    
    def obter_id_cep(self, cep: str) -> int:
        return self.cep_to_id.get(cep, -1)
    
    def obter_cep_id(self, id_cep: int) -> str:
        return self.id_to_cep.get(id_cep, "")
    
    def obter_todos_ids(self) -> List[int]:
        return list(self.id_to_cep.keys())
    
    def obter_quantidade_ids(self) -> int:
        return len(self.cep_to_id)
    
    def definir_unibrasil(self, cep_unibrasil: str):
        self.unibrasil_id = self.adicionar_cep(cep_unibrasil)
    
    def eh_id_unibrasil(self, id_cep: int) -> bool:
        return id_cep == self.unibrasil_id
    
    def obter_id_unibrasil(self) -> int:
        return self.unibrasil_id
    
    def converter_rota_para_ids(self, rota_ceps: List[str]) -> List[int]:
        return [self.obter_id_cep(cep) for cep in rota_ceps]
    
    def converter_rota_para_ceps(self, rota_ids: List[int]) -> List[str]:
        return [self.obter_cep_id(id_cep) for id_cep in rota_ids]
    
    def obter_ceps_excluindo_unibrasil(self) -> List[str]:
        ceps = []
        for cep, id_cep in self.cep_to_id.items():
            if id_cep != self.unibrasil_id:
                ceps.append(cep)
        return ceps
    
    def obter_ids_excluindo_unibrasil(self) -> List[int]:
        ids = []
        for id_cep in self.id_to_cep.keys():
            if id_cep != self.unibrasil_id:
                ids.append(id_cep)
        return ids
