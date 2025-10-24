import random
from typing import List, Tuple
from ..utils.data_manager import GerenciadorDados
from ..core.validator import ValidadorSolucao
from ..core.cost_calculator import CalculadorCusto
from ..config import GENETIC_CONFIG

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
        """Cria um indivíduo usando a estratégia do vizinho mais próximo"""
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
        
        # Gerar velocidades e tempos de pouso otimizados
        velocidades = self._gerar_velocidades_otimizadas(rota_ids)
        tempos_pouso = self._gerar_tempos_pouso_inteligentes(rota_ids, velocidades)
        
        return rota_ids, velocidades, tempos_pouso
    
    def _encontrar_vizinho_mais_proximo(self, id_atual: int, ids_nao_visitados: List[int]) -> int:
        """Encontra o CEP mais próximo do atual"""
        menor_distancia = float('inf')
        id_mais_proximo = None
        
        for id_cep in ids_nao_visitados:
            distancia = self._calcular_distancia_entre_ids(id_atual, id_cep)
            if distancia < menor_distancia:
                menor_distancia = distancia
                id_mais_proximo = id_cep
        
        return id_mais_proximo
    
    def _calcular_distancia_entre_ids(self, id1: int, id2: int) -> float:
        """Calcula distância entre dois IDs"""
        from ..utils.calculations import haversine_distance
        coords1 = self.gerenciador_dados.obter_coords_por_id(id1)
        coords2 = self.gerenciador_dados.obter_coords_por_id(id2)
        return haversine_distance(coords1, coords2)
    
    def _gerar_velocidades_otimizadas(self, rota_ids: List[int]) -> List[int]:
        """Gera velocidades otimizadas baseadas na distância"""
        velocidades = []
        for i in range(len(rota_ids) - 1):
            id_atual = rota_ids[i]
            id_proximo = rota_ids[i + 1]
            
            distancia = self._calcular_distancia_entre_ids(id_atual, id_proximo)
            
            if distancia < 1.0:  # Distância muito pequena
                velocidade = 36  # Velocidade mínima
            elif distancia < 5.0:  # Distância pequena
                velocidade = random.choice([40, 44, 48])
            elif distancia < 15.0:  # Distância média
                velocidade = random.choice([52, 56, 60, 64])
            else:  # Distância grande
                velocidade = random.choice([68, 72, 76, 80, 84, 88, 92, 96])
            
            velocidades.append(velocidade)
        
        return velocidades
    
    def _gerar_tempos_pouso_inteligentes(self, rota_ids: List[int], velocidades: List[int]) -> List[bool]:
        """Gera tempos de pouso inteligentes baseados na bateria"""
        from ..utils.calculations import calculate_autonomy
        from ..config import DRONE_CONFIG
        
        tempos_pouso = []
        bateria_atual = 5000 * 0.93  # Autonomia inicial
        
        for i in range(len(rota_ids) - 1):
            id_atual = rota_ids[i]
            id_proximo = rota_ids[i + 1]
            velocidade = velocidades[i]
            
            distancia = self._calcular_distancia_entre_ids(id_atual, id_proximo)
            tempo_voo = (distancia / velocidade) * 3600  # em segundos
            
            autonomia = calculate_autonomy(velocidade, 5000, 0.93)
            consumo_bateria = tempo_voo * (5000 / autonomia)
            
            # Decidir se precisa pousar para recarga
            if bateria_atual < consumo_bateria + 72:  # 72s de consumo por parada
                tempos_pouso.append(True)
                bateria_atual = 5000 * 0.93  # Recarregar bateria
            else:
                tempos_pouso.append(False)
                bateria_atual -= consumo_bateria
            
            # Consumir bateria da parada
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
        
        filho1_velocidades = velocidades1[:crossover_point] + velocidades2[crossover_point:]
        filho1_pousos = pousos1[:crossover_point] + pousos2[crossover_point:]
        
        filho2_velocidades = velocidades2[:crossover_point] + velocidades1[crossover_point:]
        filho2_pousos = pousos2[:crossover_point] + pousos1[crossover_point:]
        
        return (filho1_rota, filho1_velocidades, filho1_pousos), (filho2_rota, filho2_velocidades, filho2_pousos)
    
    def _corrigir_rota(self, rota_ids: List[int]) -> List[int]:
        if not rota_ids or len(rota_ids) < 3:
            return self.criar_individuo()[0]
        
        if rota_ids[0] != self.unibrasil_id:
            rota_ids[0] = self.unibrasil_id
        if rota_ids[-1] != self.unibrasil_id:
            rota_ids[-1] = self.unibrasil_id
        
        unibrasil_count = rota_ids.count(self.unibrasil_id)
        if unibrasil_count > 2:
            indices_unibrasil = [i for i, x in enumerate(rota_ids) if x == self.unibrasil_id]
            for idx in indices_unibrasil[1:-1]:
                rota_ids[idx] = random.choice(self.ids_ceps)
        
        return rota_ids
    
    def mutar(self, individuo: Tuple) -> Tuple:
        rota_ids, velocidades, tempos_pouso = individuo
        
        # Mutação híbrida: 30% chance de usar vizinho mais próximo
        if random.random() < 0.3:
            return self._mutacao_vizinho_mais_proximo(individuo)
        
        # Mutação tradicional
        if random.random() < self.mutation_rate:
            indices = random.sample(range(1, len(rota_ids) - 1), 2)
            rota_ids[indices[0]], rota_ids[indices[1]] = rota_ids[indices[1]], rota_ids[indices[0]]
        
        for i in range(len(velocidades)):
            if random.random() < self.mutation_rate:
                velocidades[i] = random.choice(range(36, 97, 4))
        
        for i in range(len(tempos_pouso)):
            if random.random() < self.mutation_rate:
                tempos_pouso[i] = not tempos_pouso[i]
        
        return rota_ids, velocidades, tempos_pouso
    
    def _mutacao_vizinho_mais_proximo(self, individuo: Tuple) -> Tuple:
        """Mutação usando estratégia do vizinho mais próximo em uma seção da rota"""
        rota_ids, velocidades, tempos_pouso = individuo
        
        # Escolher uma seção da rota para otimizar (excluindo início e fim)
        if len(rota_ids) < 6:  # Muito pequeno para otimizar
            return individuo
        
        # Escolher ponto de início e fim da seção
        inicio = random.randint(1, len(rota_ids) - 4)
        fim = random.randint(inicio + 2, len(rota_ids) - 2)
        
        # Extrair seção para otimizar
        secao_ids = rota_ids[inicio:fim]
        ids_para_otimizar = [id_cep for id_cep in secao_ids if id_cep != self.unibrasil_id]
        
        if len(ids_para_otimizar) < 2:
            return individuo
        
        # Aplicar vizinho mais próximo na seção
        nova_secao = [self.unibrasil_id] if inicio == 1 else [rota_ids[inicio-1]]
        ids_nao_visitados = ids_para_otimizar.copy()
        id_atual = nova_secao[-1]
        
        while ids_nao_visitados:
            id_mais_proximo = self._encontrar_vizinho_mais_proximo(id_atual, ids_nao_visitados)
            if id_mais_proximo is None:
                break
            
            nova_secao.append(id_mais_proximo)
            ids_nao_visitados.remove(id_mais_proximo)
            id_atual = id_mais_proximo
        
        # Reconstruir rota
        nova_rota = rota_ids[:inicio] + nova_secao[1:] + rota_ids[fim:]
        
        # Gerar novas velocidades e tempos de pouso para a seção otimizada
        novas_velocidades = velocidades.copy()
        novos_tempos_pouso = tempos_pouso.copy()
        
        for i in range(inicio, min(fim, len(nova_rota) - 1)):
            if i < len(novas_velocidades):
                distancia = self._calcular_distancia_entre_ids(nova_rota[i], nova_rota[i + 1])
                if distancia < 1.0:
                    novas_velocidades[i] = 36
                elif distancia < 5.0:
                    novas_velocidades[i] = random.choice([40, 44, 48])
                elif distancia < 15.0:
                    novas_velocidades[i] = random.choice([52, 56, 60, 64])
                else:
                    novas_velocidades[i] = random.choice([68, 72, 76, 80, 84, 88, 92, 96])
        
        return nova_rota, novas_velocidades, novos_tempos_pouso
    
    def selecao_torneio(self, populacao: List, fitness_scores: List[float]) -> Tuple:
        tournament_indices = random.sample(range(len(populacao)), self.tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(min(tournament_fitness))]
        return populacao[winner_idx]
    
    def executar(self) -> Tuple[List[int], List[int], List[bool], float]:
        # Inicialização híbrida: 20% vizinho mais próximo, 80% aleatório
        populacao = []
        
        # 20% da população com vizinho mais próximo
        num_vizinho = int(self.population_size * 0.2)
        for _ in range(num_vizinho):
            populacao.append(self.criar_individuo_vizinho_mais_proximo())
        
        # 80% da população aleatória
        for _ in range(self.population_size - num_vizinho):
            populacao.append(self.criar_individuo())
        
        melhor_individuo = None
        melhor_fitness = float('inf')
        
        for geracao in range(self.generations):
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
            
            populacao = nova_populacao[:self.population_size]
            
            if geracao % 20 == 0:
                print(f"Geração {geracao}: Melhor fitness = {melhor_fitness:.2f}")
        
        if melhor_individuo is None:
            melhor_individuo = populacao[0]
        
        return melhor_individuo[0], melhor_individuo[1], melhor_individuo[2], melhor_fitness