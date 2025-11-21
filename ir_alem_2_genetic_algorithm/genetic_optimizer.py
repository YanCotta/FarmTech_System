"""
FarmGeneticOptimizer - Algoritmo Genético para Otimização de Recursos Agrícolas
=================================================================================

Este módulo implementa um Algoritmo Genético (AG) para resolver o Problema da
Mochila Binária aplicado ao contexto agrícola, otimizando a alocação de recursos
da fazenda com orçamento limitado.

Baseado no desafio "Ir Além 2" - Otimização com Algoritmos Genéticos (FIAP)

Problema de Negócio:
--------------------
Dado um conjunto de culturas/insumos agrícolas, cada um com:
    - Custo de investimento inicial
    - Valor/Lucro esperado
    
E um orçamento máximo disponível, determinar QUAIS itens investir para
MAXIMIZAR o retorno total, respeitando a restrição orçamentária.

Formulação Matemática:
----------------------
    Maximizar:   Z = Σ(x_i * v_i)    para i=1 até n
    Sujeito a:   Σ(x_i * c_i) ≤ B
    Onde:        x_i ∈ {0, 1}  (decisão binária: investir ou não)
                 v_i = valor/lucro esperado do item i
                 c_i = custo do item i
                 B   = orçamento máximo disponível

Algoritmo Genético - Componentes:
----------------------------------
1. **Representação (Cromossomo)**: Array binário de tamanho n
   - Gene = 1: item selecionado
   - Gene = 0: item não selecionado

2. **Fitness**: Soma dos valores dos itens selecionados
   - Penalização: fitness = 0 se custo > orçamento (Death Penalty)

3. **Seleção**: Elitismo (melhores indivíduos sobrevivem)

4. **Crossover**: 
   - Single-point: ponto fixo no meio
   - Random-point: ponto aleatório para cada par

5. **Mutação**: Bit-flip aleatório (mantém diversidade genética)

6. **Convergência**: Preservação do melhor indivíduo (elitismo)

Uso Básico:
-----------
>>> import pandas as pd
>>> from genetic_optimizer import FarmGeneticOptimizer
>>> 
>>> # Dados das culturas
>>> culturas = pd.DataFrame({
>>>     'Nome': ['Soja', 'Milho', 'Trigo'],
>>>     'Custo': [5000, 3000, 2000],
>>>     'Valor': [8000, 5000, 3500]
>>> })
>>> 
>>> # Otimização
>>> otimizador = FarmGeneticOptimizer(
>>>     items_df=culturas,
>>>     budget=10000,
>>>     population_size=20,
>>>     num_generations=100
>>> )
>>> 
>>> itens, valor, custo, historico = otimizador.optimize()
>>> print(f"Investir em: {', '.join(itens)}")
>>> print(f"Lucro esperado: R$ {valor:,.2f}")

Autor: FIAP IA Engineering Team - Fase 7 Integration
Data: 2025-11-21
Versão: 2.0.0 (Refatorado com validações e novos recursos)
"""

import numpy as np
import pandas as pd
import random as rd
from random import randint
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt


class FarmGeneticOptimizer:
    """
    Otimizador Genético para Alocação de Recursos na Fazenda.
    
    Esta classe implementa um algoritmo genético completo que resolve o problema de
    otimização de recursos agrícolas, determinando quais culturas/itens devem
    ser selecionados para maximizar o valor dentro de um orçamento limitado.
    
    O algoritmo utiliza:
        - Elitismo para preservar melhores soluções
        - Crossover configurável (ponto fixo ou aleatório)
        - Mutação bit-flip para manter diversidade
        - Death Penalty para soluções inválidas (custo > orçamento)
    
    Attributes:
        items_df (pd.DataFrame): DataFrame com as informações dos itens (Nome, Custo, Valor)
        budget (float): Orçamento/Capacidade máxima disponível
        population_size (int): Tamanho da população (deve ser par)
        num_generations (int): Número de gerações para evoluir
        crossover_rate (float): Taxa de crossover (0.0 a 1.0)
        mutation_rate (float): Taxa de mutação (0.0 a 1.0)
        crossover_type (str): Tipo de crossover - 'single_point' ou 'random_point'
        best_solution (np.ndarray): Melhor solução encontrada (array binário)
        best_fitness (float): Melhor fitness alcançado
        convergence_generation (int): Geração em que a melhor solução foi encontrada
        
    Example:
        >>> culturas = pd.DataFrame({
        ...     'Nome': ['Soja', 'Milho'],
        ...     'Custo': [5000, 3000],
        ...     'Valor': [8000, 5000]
        ... })
        >>> opt = FarmGeneticOptimizer(culturas, budget=10000)
        >>> itens, valor, custo, hist = opt.optimize()
        >>> print(opt.get_summary())
    """
    
    def __init__(
        self, 
        items_df: pd.DataFrame = None,
        budget: float = 100.0,
        population_size: int = 16,
        num_generations: int = 1000,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.15,
        crossover_type: str = 'single_point'
    ):
        """
        Inicializa o otimizador genético.
        
        Args:
            items_df: DataFrame com colunas ['Nome', 'Custo', 'Valor']
            budget: Orçamento máximo disponível
            population_size: Tamanho da população (deve ser par)
            num_generations: Número de gerações para evoluir
            crossover_rate: Probabilidade de crossover entre 0 e 1
            mutation_rate: Probabilidade de mutação entre 0 e 1
            crossover_type: Tipo de crossover - 'single_point' (fixo no meio) ou 'random_point' (aleatório)
            
        Raises:
            ValueError: Se population_size for ímpar ou menor que 4
            ValueError: Se items_df não tiver as colunas necessárias
            ValueError: Se crossover_rate ou mutation_rate estiverem fora de [0, 1]
        """
        # Validações
        if population_size < 4 or population_size % 2 != 0:
            raise ValueError("Population size deve ser um número par >= 4")
        
        if not 0 <= crossover_rate <= 1:
            raise ValueError("crossover_rate deve estar entre 0 e 1")
        
        if not 0 <= mutation_rate <= 1:
            raise ValueError("mutation_rate deve estar entre 0 e 1")
        
        if crossover_type not in ['single_point', 'random_point']:
            raise ValueError("crossover_type deve ser 'single_point' ou 'random_point'")
        
        if items_df is not None:
            required_cols = {'Nome', 'Custo', 'Valor'}
            if not required_cols.issubset(items_df.columns):
                raise ValueError(f"DataFrame deve conter as colunas: {required_cols}")
            
            if len(items_df) == 0:
                raise ValueError("DataFrame não pode estar vazio")
        
        self.items_df = items_df
        self.budget = budget
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.crossover_type = crossover_type
        
        # Extrair arrays de custo e valor
        if items_df is not None:
            self.costs = items_df['Custo'].values
            self.values = items_df['Valor'].values
            self.item_names = items_df['Nome'].values
            self.num_items = len(items_df)
        else:
            self.costs = None
            self.values = None
            self.item_names = None
            self.num_items = 0
            
        # Armazenar histórico de fitness
        self.fitness_history = []
        self.best_solution = None
        self.best_fitness = 0
        self.convergence_generation = 0
    
    def _fitness(self, population: np.ndarray) -> np.ndarray:
        """
        Calcula o fitness de cada indivíduo na população usando Death Penalty.
        
        Um indivíduo é um array binário onde 1 indica que o item foi selecionado
        e 0 indica que não foi. O fitness é a soma dos valores dos itens selecionados,
        mas é zero se o custo total exceder o orçamento (Death Penalty).
        
        Formulação Matemática:
            fitness(i) = Σ(chromosome[i] * values)  se Σ(chromosome[i] * costs) ≤ budget
                       = 0                          caso contrário (penalização mortal)
        
        Args:
            population: Array 2D onde cada linha é um indivíduo (solução binária)
                       Shape: (population_size, num_items)
            
        Returns:
            Array com o fitness de cada indivíduo (valores não-negativos)
        """
        fitness = np.empty(len(population))
        
        for i in range(len(fitness)):
            total_value = np.sum(population[i] * self.values)
            total_cost = np.sum(population[i] * self.costs)
            
            # Death Penalty: soluções inválidas recebem fitness 0
            if total_cost <= self.budget:
                fitness[i] = total_value
            else:
                fitness[i] = 0
                
        return fitness.astype(float)
    
    def _selection(self, fitness: np.ndarray, num_parents: int, population: np.ndarray) -> np.ndarray:
        """
        Seleciona os melhores indivíduos para reprodução usando Elitismo.
        
        Estratégia: Ordena a população por fitness e seleciona os top N indivíduos.
        Isso garante que as melhores soluções sejam preservadas para a próxima geração.
        
        Args:
            fitness: Array com fitness de cada indivíduo
            num_parents: Número de pais a selecionar
            population: População atual (shape: population_size x num_items)
            
        Returns:
            Array com os melhores indivíduos selecionados (shape: num_parents x num_items)
        """
        fitness_copy = fitness.copy().tolist()
        parents = np.empty((num_parents, population.shape[1]))
        
        for i in range(num_parents):
            # Encontra o índice do maior fitness
            max_fitness_idx = np.argmax(fitness_copy)
            parents[i, :] = population[max_fitness_idx, :]
            # Marca como já selecionado atribuindo valor muito baixo
            fitness_copy[max_fitness_idx] = -999999
            
        return parents
    
    def _crossover(self, parents: np.ndarray, num_offsprings: int) -> np.ndarray:
        """
        Realiza crossover de um ponto para gerar descendentes.
        
        Tipos de Crossover:
            - 'single_point': Ponto de corte fixo no meio do cromossomo
            - 'random_point': Ponto de corte aleatório para cada par de pais
        
        Lógica: Combina genes de dois pais diferentes. Se o crossover não ocorrer
        (baseado na taxa de crossover), copia o parent1 diretamente.
        
        Args:
            parents: Array com os pais selecionados (shape: num_parents x num_items)
            num_offsprings: Número de filhos a gerar
            
        Returns:
            Array com os descendentes gerados (shape: num_offsprings x num_items)
        """
        offsprings = np.empty((num_offsprings, parents.shape[1]))
        
        # Define o ponto de crossover baseado no tipo
        if self.crossover_type == 'single_point':
            crossover_point = int(parents.shape[1] / 2)
        
        cnt_offsprings = 0
        i = 0
        max_attempts = num_offsprings * 10  # Evita loop infinito
        
        while cnt_offsprings < num_offsprings and i < max_attempts:
            parent1_index = i % parents.shape[0]
            parent2_index = (i + 1) % parents.shape[0]
            
            # Decide se aplica crossover baseado na taxa
            if rd.random() <= self.crossover_rate:
                # Ponto de crossover aleatório se configurado
                if self.crossover_type == 'random_point':
                    crossover_point = randint(1, parents.shape[1] - 1)
                
                # Realiza crossover
                offsprings[cnt_offsprings, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
                offsprings[cnt_offsprings, crossover_point:] = parents[parent2_index, crossover_point:]
                cnt_offsprings += 1
            else:
                # Sem crossover: copia parent1 diretamente (clonagem)
                offsprings[cnt_offsprings, :] = parents[parent1_index, :]
                cnt_offsprings += 1
            
            i += 1
        
        # Se não conseguiu gerar todos os filhos, completa com clones dos pais
        while cnt_offsprings < num_offsprings:
            parent_idx = cnt_offsprings % parents.shape[0]
            offsprings[cnt_offsprings, :] = parents[parent_idx, :]
            cnt_offsprings += 1
            
        return offsprings
    
    def _mutation(self, offsprings: np.ndarray) -> np.ndarray:
        """
        Aplica mutação de inversão de bit (Bit-Flip Mutation) aos descendentes.
        
        Para cada descendente, há uma chance (mutation_rate) de mutar.
        Se mutação ocorrer, um gene aleatório é invertido (0→1 ou 1→0).
        
        Objetivo: Manter diversidade genética e evitar convergência prematura
        para ótimos locais.
        
        Args:
            offsprings: Array com descendentes (shape: num_offsprings x num_items)
            
        Returns:
            Array com descendentes mutados (mesma shape)
        """
        mutants = np.empty(offsprings.shape)
        
        for i in range(mutants.shape[0]):
            mutants[i, :] = offsprings[i, :]
            
            # Aplica mutação baseado na taxa
            if rd.random() <= self.mutation_rate:
                # Seleciona gene aleatório para inverter
                gene_idx = randint(0, offsprings.shape[1] - 1)
                # Inverte o bit (0→1 ou 1→0)
                mutants[i, gene_idx] = 1 - mutants[i, gene_idx]
                
        return mutants
    
    def optimize(self) -> Tuple[List[str], float, float, pd.DataFrame]:
        """
        Executa o algoritmo genético para encontrar a melhor solução.
        
        Returns:
            Tupla contendo:
                - Lista com nomes dos itens selecionados
                - Valor total alcançado
                - Custo total usado
                - DataFrame com histórico de fitness
        """
        if self.items_df is None or len(self.items_df) == 0:
            raise ValueError("Items DataFrame não foi fornecido ou está vazio")
        
        # Inicializa população aleatória
        population = np.random.randint(2, size=(self.population_size, self.num_items))
        population = population.astype(int)
        
        # Calcula número de pais e filhos
        num_parents = int(self.population_size / 2)
        num_offsprings = self.population_size - num_parents
        
        # Histórico para visualização
        fitness_history_mean = []
        fitness_history_max = []
        
        # Loop principal do algoritmo genético
        for generation in range(self.num_generations):
            # Avalia fitness da população atual
            fitness = self._fitness(population)
            
            # Armazena estatísticas
            fitness_history_mean.append(np.mean(fitness))
            fitness_history_max.append(np.max(fitness))
            
            # Rastreia a melhor solução encontrada até agora
            gen_best_fitness = np.max(fitness)
            if gen_best_fitness > self.best_fitness:
                self.best_fitness = gen_best_fitness
                self.convergence_generation = generation
            
            # Seleciona os melhores para reprodução
            parents = self._selection(fitness, num_parents, population)
            
            # Gera descendentes via crossover
            offsprings = self._crossover(parents, num_offsprings)
            
            # Aplica mutação
            mutants = self._mutation(offsprings)
            
            # Forma nova população (elitismo: mantém melhores pais + novos mutantes)
            population[0:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutants
        
        # Avalia fitness da última geração
        fitness_last_gen = self._fitness(population)
        
        # Encontra melhor solução
        max_fitness_idx = np.where(fitness_last_gen == np.max(fitness_last_gen))[0][0]
        best_solution = population[max_fitness_idx, :]
        
        # Armazena resultados
        self.best_solution = best_solution
        self.best_fitness = fitness_last_gen[max_fitness_idx]
        
        # Calcula itens selecionados e custos
        selected_items = []
        total_cost = 0
        total_value = 0
        
        for i in range(len(best_solution)):
            if best_solution[i] == 1:
                selected_items.append(self.item_names[i])
                total_cost += self.costs[i]
                total_value += self.values[i]
        
        # Cria DataFrame com histórico
        history_df = pd.DataFrame({
            'Geração': list(range(self.num_generations)),
            'Fitness Médio': fitness_history_mean,
            'Fitness Máximo': fitness_history_max
        })
        
        self.fitness_history = history_df
        
        # Converte para tipos Python nativos para compatibilidade
        return (
            selected_items, 
            float(total_value), 
            float(total_cost), 
            history_df
        )
    
    def plot_fitness_evolution(self, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Plota a evolução do fitness ao longo das gerações.
        
        Args:
            figsize: Tamanho da figura (largura, altura)
            
        Returns:
            Figura matplotlib
        """
        if len(self.fitness_history) == 0:
            raise ValueError("Execute optimize() primeiro para gerar dados")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(
            self.fitness_history['Geração'], 
            self.fitness_history['Fitness Médio'],
            label='Fitness Médio',
            linewidth=2,
            alpha=0.7
        )
        ax.plot(
            self.fitness_history['Geração'],
            self.fitness_history['Fitness Máximo'],
            label='Fitness Máximo',
            linewidth=2,
            alpha=0.7
        )
        
        ax.set_xlabel('Gerações', fontsize=12)
        ax.set_ylabel('Fitness', fontsize=12)
        ax.set_title('Evolução do Fitness - Algoritmo Genético', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def get_summary(self) -> Dict[str, any]:
        """
        Retorna um resumo dos resultados da otimização.
        
        Returns:
            Dicionário com informações sobre a melhor solução
        """
        if self.best_solution is None:
            return {"error": "Execute optimize() primeiro"}
        
        selected_items = []
        total_cost = 0
        total_value = 0
        
        for i in range(len(self.best_solution)):
            if self.best_solution[i] == 1:
                selected_items.append({
                    'Nome': self.item_names[i],
                    'Custo': float(self.costs[i]),
                    'Valor': float(self.values[i])
                })
                total_cost += self.costs[i]
                total_value += self.values[i]
        
        return {
            'itens_selecionados': selected_items,
            'total_itens': len(selected_items),
            'valor_total': float(total_value),
            'custo_total': float(total_cost),
            'orcamento': float(self.budget),
            'orcamento_utilizado_percentual': float(total_cost / self.budget * 100),
            'melhor_fitness': float(self.best_fitness),
            'geracao_convergencia': int(self.convergence_generation)
        }
    
    def get_detailed_results(self) -> pd.DataFrame:
        """
        Retorna um DataFrame detalhado com todos os itens e indicação de seleção.
        
        Returns:
            DataFrame com colunas: Nome, Custo, Valor, Selecionado, ROI
        """
        if self.best_solution is None:
            raise ValueError("Execute optimize() primeiro")
        
        results = self.items_df.copy()
        results['Selecionado'] = self.best_solution.astype(int)
        results['ROI'] = ((results['Valor'] - results['Custo']) / results['Custo'] * 100).round(2)
        results['Eficiencia'] = (results['Valor'] / results['Custo']).round(2)
        
        # Ordena por selecionados primeiro, depois por ROI
        results = results.sort_values(['Selecionado', 'ROI'], ascending=[False, False])
        
        return results
    
    def analyze_budget_sensitivity(self, budget_range: List[float] = None) -> pd.DataFrame:
        """
        Analisa como diferentes orçamentos afetam o valor total otimizado.
        
        Útil para planejamento: "Se eu tiver mais R$ 10.000, quanto mais lucro consigo?"
        
        Args:
            budget_range: Lista de orçamentos a testar. Se None, usa variações de ±50%
            
        Returns:
            DataFrame com: Budget, Total_Value, Num_Items, Budget_Usage_%
        """
        if budget_range is None:
            # Cria range automático: 50% a 150% do orçamento atual
            budget_range = np.linspace(
                self.budget * 0.5, 
                self.budget * 1.5, 
                num=10
            )
        
        results = []
        original_budget = self.budget
        
        for test_budget in budget_range:
            self.budget = test_budget
            selected, value, cost, _ = self.optimize()
            
            results.append({
                'Orcamento': test_budget,
                'Valor_Total': value,
                'Num_Itens': len(selected),
                'Custo_Total': cost,
                'Uso_Orcamento_%': (cost / test_budget * 100) if test_budget > 0 else 0
            })
        
        # Restaura orçamento original
        self.budget = original_budget
        
        return pd.DataFrame(results)


def generate_sample_farm_items(num_items: int = 20, seed: int = 42) -> pd.DataFrame:
    """
    Gera dados de exemplo de culturas agrícolas para teste.
    
    Args:
        num_items: Número de itens a gerar
        seed: Seed para reprodutibilidade
        
    Returns:
        DataFrame com culturas de exemplo
    """
    np.random.seed(seed)
    
    culturas = [
        'Milho', 'Soja', 'Trigo', 'Arroz', 'Feijão', 'Café', 'Cana-de-açúcar',
        'Algodão', 'Mandioca', 'Batata', 'Tomate', 'Cebola', 'Alho', 'Cenoura',
        'Abóbora', 'Melancia', 'Melão', 'Banana', 'Laranja', 'Manga', 'Uva',
        'Maçã', 'Pera', 'Pêssego', 'Morango', 'Alface', 'Couve', 'Brócolis',
        'Couve-flor', 'Espinafre'
    ]
    
    # Seleciona culturas aleatórias
    selected_cultures = np.random.choice(culturas, size=min(num_items, len(culturas)), replace=False)
    
    # Gera custos e valores
    costs = np.random.randint(5, 50, size=num_items)
    values = np.random.randint(10, 150, size=num_items)
    
    df = pd.DataFrame({
        'Nome': selected_cultures[:num_items],
        'Custo': costs,
        'Valor': values
    })
    
    return df


# Exemplo de uso
if __name__ == "__main__":
    # Gera dados de exemplo
    print("=" * 70)
    print(" FarmGeneticOptimizer - Otimização de Recursos Agrícolas")
    print(" Algoritmo Genético para o Problema da Mochila Binária")
    print("=" * 70)
    
    items_df = generate_sample_farm_items(num_items=20)
    budget = 150
    
    print(f"\n📊 CONFIGURAÇÃO DO PROBLEMA")
    print(f"{'─' * 70}")
    print(f"   Orçamento disponível: R$ {budget:,.2f}")
    print(f"   Número de culturas: {len(items_df)}")
    print(f"\n📋 Culturas disponíveis:")
    print(items_df.to_string(index=False))
    
    # Cria e executa o otimizador
    print(f"\n{'─' * 70}")
    print("🧬 EXECUTANDO ALGORITMO GENÉTICO...")
    print(f"{'─' * 70}")
    
    optimizer = FarmGeneticOptimizer(
        items_df=items_df,
        budget=budget,
        population_size=20,
        num_generations=500,
        crossover_rate=0.8,
        mutation_rate=0.15,
        crossover_type='single_point'  # Ou 'random_point'
    )
    
    selected_items, total_value, total_cost, history = optimizer.optimize()
    
    print("\n" + "=" * 70)
    print(" ✅ RESULTADOS DA OTIMIZAÇÃO")
    print("=" * 70)
    print(f"\n🌱 Itens selecionados ({len(selected_items)}):")
    print(f"   {', '.join(selected_items)}")
    print(f"\n💰 Valor total esperado: R$ {total_value:,.2f}")
    print(f"💸 Custo total: R$ {total_cost:,.2f} (de R$ {budget:,.2f})")
    print(f"📊 Orçamento utilizado: {total_cost/budget*100:.1f}%")
    print(f"🎯 Convergência na geração: {optimizer.convergence_generation}")
    
    # Mostra resumo detalhado
    summary = optimizer.get_summary()
    print(f"\n📈 Resumo Completo:")
    for key, value in summary.items():
        if key != 'itens_selecionados':
            print(f"   {key}: {value}")
    
    # Mostra análise detalhada
    print(f"\n{'─' * 70}")
    print("📊 ANÁLISE DETALHADA DE ITENS")
    print(f"{'─' * 70}")
    detailed = optimizer.get_detailed_results()
    print(detailed.to_string(index=False))
    
    # Plota evolução
    print(f"\n{'─' * 70}")
    print("📈 Gerando gráfico de evolução do fitness...")
    fig = optimizer.plot_fitness_evolution(figsize=(14, 7))
    plt.savefig('genetic_optimization_evolution.png', dpi=150, bbox_inches='tight')
    print("   ✅ Gráfico salvo: 'genetic_optimization_evolution.png'")
    
    # Análise de sensibilidade (opcional - comentado pois demora)
    # print(f"\n{'─' * 70}")
    # print("🔬 ANÁLISE DE SENSIBILIDADE DE ORÇAMENTO")
    # print(f"{'─' * 70}")
    # sensitivity = optimizer.analyze_budget_sensitivity()
    # print(sensitivity.to_string(index=False))
    
    print(f"\n{'=' * 70}")
    print(" ✨ Otimização concluída com sucesso!")
    print("=" * 70)
