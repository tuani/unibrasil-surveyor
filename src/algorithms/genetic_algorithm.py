import random
from typing import List, Tuple
from tqdm import tqdm
from ..utils.data_manager import GerenciadorDados
from ..core.validator import ValidadorSolucao
from ..core.cost_calculator import CalculadorCusto
from ..config import GENETIC_CONFIG
from ..utils.calculations import remove_crossings_2opt, has_crossings

class AlgoritmoGenetico:
    def __init__(self, gerenciador_dados: GerenciadorDados, validador: ValidadorSolucao, 
                 calculador_custo: CalculadorCusto):
        self.gerenciador_dados = gerenciador_dados
        self.validador = validador
        self.calculador_custo = calculador_custo
        self.config = GENETIC_CONFIG
        
        self.population_size = self.config['population_size']
        self.generations = self.config['generations']
        self.mutation_rate = self.config['mutation_rate']
        self.crossover_rate = self.config['crossover_rate']
        self.elite_size = self.config['elite_size']
        self.tournament_size = self.config['tournament_size']
        
        self.unibrasil_id = gerenciador_dados.obter_id_unibrasil()
        self.ids_ceps = gerenciador_dados.obter_ids_excluindo_unibrasil()
    
    def criar_individuo(self) -> Tuple[List[int], List[int], List[bool]]:
        ids_aleatorios = self.ids_ceps.copy()
        random.shuffle(ids_aleatorios)
        
        rota_ids = [self.unibrasil_id] + ids_aleatorios + [self.unibrasil_id]
        
        velocidades = [random.choice(range(36, 97, 4)) for _ in range(len(rota_ids) - 1)]
        
        tempos_pouso = [random.choice([True, False]) for _ in range(len(rota_ids) - 1)]
        
        return rota_ids, velocidades, tempos_pouso
    
    def criar_individuo_vizinho_mais_proximo(self) -> Tuple[List[int], List[int], List[bool]]:
        rota_ids = [self.unibrasil_id]
        ids_nao_visitados = self.ids_ceps.copy()
        id_atual = self.unibrasil_id
        
        while ids_nao_visitados:
            id_mais_proximo = self._encontrar_vizinho_mais_proximo(id_atual, ids_nao_visitados)
            if id_mais_proximo is None:
                break
            
            rota_ids.append(id_mais_proximo)
            ids_nao_visitados.remove(id_mais_proximo)
            id_atual = id_mais_proximo
        
        rota_ids.append(self.unibrasil_id)
        rota_ids = self._aplicar_2opt(rota_ids, max_iterations=3)
        velocidades = self._gerar_velocidades(rota_ids)
        tempos_pouso = self._gerar_tempos_pouso_inteligentes(rota_ids, velocidades)
        
        return rota_ids, velocidades, tempos_pouso
    
    def _encontrar_vizinho_mais_proximo(self, id_atual: int, ids_nao_visitados: List[int]) -> int:
        menor_distancia = float('inf')
        id_mais_proximo = None
        
        for id_cep in ids_nao_visitados:
            distancia = self._calcular_distancia_entre_ids(id_atual, id_cep)
            if distancia < menor_distancia:
                menor_distancia = distancia
                id_mais_proximo = id_cep
        
        return id_mais_proximo
    
    def _calcular_distancia_entre_ids(self, id1: int, id2: int) -> float:
        from ..utils.calculations import haversine_distance
        coords1 = self.gerenciador_dados.obter_coords_por_id(id1)
        coords2 = self.gerenciador_dados.obter_coords_por_id(id2)
        return haversine_distance(coords1, coords2)
    
    def _aplicar_2opt(self, rota_ids: List[int], max_iterations: int = 10, force_complete: bool = False) -> List[int]:
        if len(rota_ids) < 4:
            return rota_ids
        def get_coords(route_id: int):
            return self.gerenciador_dados.obter_coords_por_id(route_id)
        return remove_crossings_2opt(rota_ids, get_coords, max_iterations, force_complete)
    
    def _tem_cruzamentos(self, rota_ids: List[int]) -> bool:
        if len(rota_ids) < 4:
            return False
        def get_coords(route_id: int):
            return self.gerenciador_dados.obter_coords_por_id(route_id)
        coords_list = [get_coords(route_id) for route_id in rota_ids]
        return has_crossings(coords_list)
    
    def _gerar_velocidades(self, rota_ids: List[int]) -> List[int]:
        velocidades = []
        for i in range(len(rota_ids) - 1):
            distancia = self._calcular_distancia_entre_ids(rota_ids[i], rota_ids[i + 1])
            if distancia < 1.0:
                velocidade = 36
            elif distancia < 5.0:
                velocidade = random.choice([40, 44, 48])
            elif distancia < 15.0:
                velocidade = random.choice([52, 56, 60, 64])
            else:
                velocidade = random.choice([68, 72, 76, 80, 84, 88, 92, 96])
            velocidades.append(velocidade)
        return velocidades
    
    def _gerar_tempos_pouso_inteligentes(self, rota_ids: List[int], velocidades: List[int]) -> List[bool]:
        from ..utils.calculations import calculate_autonomy
        tempos_pouso = []
        bateria_atual = 5000 * 0.93
        for i in range(len(rota_ids) - 1):
            distancia = self._calcular_distancia_entre_ids(rota_ids[i], rota_ids[i + 1])
            tempo_voo = (distancia / velocidades[i]) * 3600
            autonomia = calculate_autonomy(velocidades[i], 5000, 0.93)
            consumo_bateria = tempo_voo * (5000 / autonomia)
            if bateria_atual < consumo_bateria + 72:
                tempos_pouso.append(True)
                bateria_atual = 5000 * 0.93
            else:
                tempos_pouso.append(False)
                bateria_atual -= consumo_bateria
            bateria_atual -= 72
        return tempos_pouso
    
    def crossover(self, pai1: Tuple, pai2: Tuple) -> Tuple[Tuple, Tuple]:
        rota1_ids, velocidades1, pousos1 = pai1
        rota2_ids, velocidades2, pousos2 = pai2
        
        size = len(rota1_ids)
        crossover_point = random.randint(1, size - 2)
        
        filho1_rota = rota1_ids[:crossover_point] + rota2_ids[crossover_point:]
        filho2_rota = rota2_ids[:crossover_point] + rota1_ids[crossover_point:]
        
        filho1_rota = self._corrigir_rota(filho1_rota)
        filho2_rota = self._corrigir_rota(filho2_rota)
        
        if random.random() < 0.02:
            filho1_rota = self._aplicar_2opt(filho1_rota, max_iterations=2)
        if random.random() < 0.02:
            filho2_rota = self._aplicar_2opt(filho2_rota, max_iterations=2)
        
        filho1_velocidades = velocidades1[:crossover_point] + velocidades2[crossover_point:]
        filho1_pousos = pousos1[:crossover_point] + pousos2[crossover_point:]
        filho2_velocidades = velocidades2[:crossover_point] + velocidades1[crossover_point:]
        filho2_pousos = pousos2[:crossover_point] + pousos1[crossover_point:]
        
        if len(filho1_velocidades) != len(filho1_rota) - 1:
            filho1_velocidades = self._gerar_velocidades(filho1_rota)
            filho1_pousos = self._gerar_tempos_pouso_inteligentes(filho1_rota, filho1_velocidades)
        
        if len(filho2_velocidades) != len(filho2_rota) - 1:
            filho2_velocidades = self._gerar_velocidades(filho2_rota)
            filho2_pousos = self._gerar_tempos_pouso_inteligentes(filho2_rota, filho2_velocidades)
        
        return (filho1_rota, filho1_velocidades, filho1_pousos), (filho2_rota, filho2_velocidades, filho2_pousos)
    
    def _corrigir_rota(self, rota_ids: List[int]) -> List[int]:
        if not rota_ids or len(rota_ids) < 3:
            return self.criar_individuo()[0]
        
        ceps_meio = rota_ids[1:-1]
        ceps_unicos = []
        ceps_vistos = set()
        for cep_id in ceps_meio:
            if cep_id != self.unibrasil_id and cep_id not in ceps_vistos:
                ceps_unicos.append(cep_id)
                ceps_vistos.add(cep_id)
        
        ceps_faltantes = [cep for cep in self.ids_ceps if cep not in ceps_vistos]
        random.shuffle(ceps_faltantes)
        ceps_unicos.extend(ceps_faltantes)
        ceps_unicos = list(dict.fromkeys(ceps_unicos))
        
        if len(ceps_unicos) < len(self.ids_ceps):
            ceps_restantes = [cep for cep in self.ids_ceps if cep not in ceps_unicos]
            ceps_unicos.extend(ceps_restantes)
        
        if len(ceps_unicos) > len(self.ids_ceps):
            ceps_unicos = ceps_unicos[:len(self.ids_ceps)]
        
        return [self.unibrasil_id] + ceps_unicos + [self.unibrasil_id]
    
    def mutar(self, individuo: Tuple) -> Tuple:
        rota_ids, velocidades, tempos_pouso = individuo
        
        if random.random() < 0.3:
            return self._mutacao_vizinho_mais_proximo(individuo)
        
        if random.random() < self.mutation_rate:
            indices = random.sample(range(1, len(rota_ids) - 1), 2)
            rota_ids[indices[0]], rota_ids[indices[1]] = rota_ids[indices[1]], rota_ids[indices[0]]
        
        for i in range(len(velocidades)):
            if random.random() < self.mutation_rate:
                velocidades[i] = random.choice(range(36, 97, 4))
        
        for i in range(len(tempos_pouso)):
            if random.random() < self.mutation_rate:
                tempos_pouso[i] = not tempos_pouso[i]
        
        if random.random() < 0.01:
            rota_ids = self._aplicar_2opt(rota_ids, max_iterations=2)
            if len(velocidades) != len(rota_ids) - 1:
                velocidades = self._gerar_velocidades(rota_ids)
                tempos_pouso = self._gerar_tempos_pouso_inteligentes(rota_ids, velocidades)
        
        return rota_ids, velocidades, tempos_pouso
    
    def _mutacao_vizinho_mais_proximo(self, individuo: Tuple) -> Tuple:
        rota_ids, velocidades, tempos_pouso = individuo
        
        if len(rota_ids) < 6:
            return individuo
        
        inicio = random.randint(1, len(rota_ids) - 4)
        fim = random.randint(inicio + 2, len(rota_ids) - 2)
        secao_ids = rota_ids[inicio:fim]
        ids_para_reordenar = [id_cep for id_cep in secao_ids if id_cep != self.unibrasil_id]
        
        if len(ids_para_reordenar) < 2:
            return individuo
        
        nova_secao = [self.unibrasil_id] if inicio == 1 else [rota_ids[inicio-1]]
        ids_nao_visitados = ids_para_reordenar.copy()
        id_atual = nova_secao[-1]
        
        while ids_nao_visitados:
            id_mais_proximo = self._encontrar_vizinho_mais_proximo(id_atual, ids_nao_visitados)
            if id_mais_proximo is None:
                break
            nova_secao.append(id_mais_proximo)
            ids_nao_visitados.remove(id_mais_proximo)
            id_atual = id_mais_proximo
        
        nova_rota = rota_ids[:inicio] + nova_secao[1:] + rota_ids[fim:]
        
        if random.random() < 0.05:
            nova_rota = self._aplicar_2opt(nova_rota, max_iterations=2)
        
        novas_velocidades = self._gerar_velocidades(nova_rota)
        novos_tempos_pouso = self._gerar_tempos_pouso_inteligentes(nova_rota, novas_velocidades)
        
        return nova_rota, novas_velocidades, novos_tempos_pouso
    
    def selecao_torneio(self, populacao: List, fitness_scores: List[float]) -> Tuple:
        tournament_indices = random.sample(range(len(populacao)), self.tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(min(tournament_fitness))]
        return populacao[winner_idx]
    
    def executar(self) -> Tuple[List[int], List[int], List[bool], float]:
        populacao = []
        num_vizinho = int(self.population_size * 0.2)
        for _ in range(num_vizinho):
            populacao.append(self.criar_individuo_vizinho_mais_proximo())
        for _ in range(self.population_size - num_vizinho):
            populacao.append(self.criar_individuo())
        
        melhor_individuo = None
        melhor_fitness = float('inf')
        
        for geracao in tqdm(range(self.generations), desc="Gerando rota", unit="geração"):
            fitness_scores = []
            for individuo in populacao:
                eh_valida, _ = self.validador.validar_solucao_ids(*individuo)
                if eh_valida:
                    custo, _ = self.calculador_custo.calcular_custo_rota_ids(*individuo)
                    fitness_scores.append(custo)
                else:
                    fitness_scores.append(float('inf'))
            
            min_fitness = min(fitness_scores)
            if min_fitness < melhor_fitness:
                melhor_fitness = min_fitness
                melhor_individuo = populacao[fitness_scores.index(min_fitness)]
            
            nova_populacao = []
            
            elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:self.elite_size]
            for idx in elite_indices:
                nova_populacao.append(populacao[idx])
            
            while len(nova_populacao) < self.population_size:
                pai1 = self.selecao_torneio(populacao, fitness_scores)
                pai2 = self.selecao_torneio(populacao, fitness_scores)
                
                if random.random() < self.crossover_rate:
                    filho1, filho2 = self.crossover(pai1, pai2)
                else:
                    filho1, filho2 = pai1, pai2
                
                filho1 = self.mutar(filho1)
                filho2 = self.mutar(filho2)
                
                nova_populacao.extend([filho1, filho2])
            
            if geracao % 30 == 0 and len(nova_populacao) > 0:
                rota_ids, velocidades, tempos_pouso = nova_populacao[0]
                rota_melhorada = self._aplicar_2opt(rota_ids, max_iterations=5)
                if len(velocidades) != len(rota_melhorada) - 1:
                    velocidades = self._gerar_velocidades(rota_melhorada)
                    tempos_pouso = self._gerar_tempos_pouso_inteligentes(rota_melhorada, velocidades)
                nova_populacao[0] = (rota_melhorada, velocidades, tempos_pouso)
            
            populacao = nova_populacao[:self.population_size]
        
        if melhor_individuo is None:
            melhor_individuo = populacao[0]
        
        rota_final, velocidades_final, tempos_pouso_final = melhor_individuo
        rota_final = self._corrigir_rota(rota_final)
        
        rota_final = self._aplicar_2opt(rota_final, max_iterations=100, force_complete=True)
        rota_final = self._corrigir_rota(rota_final)
        if len(velocidades_final) != len(rota_final) - 1:
            velocidades_final = self._gerar_velocidades(rota_final)
            tempos_pouso_final = self._gerar_tempos_pouso_inteligentes(rota_final, velocidades_final)
        
        return rota_final, velocidades_final, tempos_pouso_final, melhor_fitness