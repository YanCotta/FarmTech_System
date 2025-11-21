"""
FarmGeneticOptimizer - Algoritmo Genético para Otimização de Recursos Agrícolas

Este módulo implementa um Algoritmo Genético para resolver o Problema da Mochila Binária
aplicado ao contexto agrícola, otimizando a alocação de recursos da fazenda.

Baseado no desafio "Ir Além 2" - Otimização com Algoritmos Genéticos
"""

import numpy as np
import pandas as pd
import random as rd
from random import randint
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt


class FarmGeneticOptimizer:
    """
    Otimizador Genético para Alocação de Recursos na Fazenda
    
    Esta classe implementa um algoritmo genético que resolve o problema de
    otimização de recursos agrícolas, determinando quais culturas/itens devem
    ser selecionados para maximizar o valor dentro de um orçamento limitado.
    
    Attributes:
        items_df (pd.DataFrame): DataFrame com as informações dos itens (Nome, Custo, Valor)
        budget (float): Orçamento/Capacidade máxima disponível
        population_size (int): Tamanho da população
        num_generations (int): Número de gerações para evoluir
        crossover_rate (float): Taxa de crossover (0.0 a 1.0)
        mutation_rate (float): Taxa de mutação (0.0 a 1.0)
    """
    
    def __init__(
        self, 
        items_df: pd.DataFrame = None,
        budget: float = 100.0,
        population_size: int = 16,
        num_generations: int = 1000,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.15
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
        """
        self.items_df = items_df
        self.budget = budget
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
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
    
    def _fitness(self, population: np.ndarray) -> np.ndarray:
        """
        Calcula o fitness de cada indivíduo na população.
        
        Um indivíduo é um array binário onde 1 indica que o item foi selecionado
        e 0 indica que não foi. O fitness é a soma dos valores dos itens selecionados,
        mas é zero se o custo total exceder o orçamento.
        
        Args:
            population: Array 2D onde cada linha é um indivíduo (solução binária)
            
        Returns:
            Array com o fitness de cada indivíduo
        """
        fitness = np.empty(len(population))
        
        for i in range(len(fitness)):
            total_value = np.sum(population[i] * self.values)
            total_cost = np.sum(population[i] * self.costs)
            
            # Se o custo exceder o orçamento, fitness = 0 (solução inválida)
            if total_cost <= self.budget:
                fitness[i] = total_value
            else:
                fitness[i] = 0
                
        return fitness.astype(int)
    
    def _selection(self, fitness: np.ndarray, num_parents: int, population: np.ndarray) -> np.ndarray:
        """
        Seleciona os melhores indivíduos para reprodução (elitismo).
        
        Args:
            fitness: Array com fitness de cada indivíduo
            num_parents: Número de pais a selecionar
            population: População atual
            
        Returns:
            Array com os melhores indivíduos selecionados
        """
        fitness_list = list(fitness)
        parents = np.empty((num_parents, population.shape[1]))
        
        for i in range(num_parents):
            max_fitness_idx = np.where(fitness_list == np.max(fitness_list))
            parents[i, :] = population[max_fitness_idx[0][0], :]
            fitness_list[max_fitness_idx[0][0]] = -9999  # Marca como já selecionado
            
        return parents
    
    def _crossover(self, parents: np.ndarray, num_offsprings: int) -> np.ndarray:
        """
        Realiza crossover de um ponto para gerar descendentes.
        
        Args:
            parents: Array com os pais selecionados
            num_offsprings: Número de filhos a gerar
            
        Returns:
            Array com os descendentes gerados
        """
        offsprings = np.empty((num_offsprings, parents.shape[1]))
        crossover_point = int(parents.shape[1] / 2)
        cnt_offsprings = 0
        i = 0
        
        while cnt_offsprings < num_offsprings:
            parent1_index = i % parents.shape[0]
            parent2_index = (i + 1) % parents.shape[0]
            x = rd.random()
            
            if x <= self.crossover_rate:
                # Realiza crossover
                offsprings[cnt_offsprings, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
                offsprings[cnt_offsprings, crossover_point:] = parents[parent2_index, crossover_point:]
                cnt_offsprings += 1
            
            i += 1
            
        return offsprings
    
    def _mutation(self, offsprings: np.ndarray) -> np.ndarray:
        """
        Aplica mutação aos descendentes invertendo bits aleatoriamente.
        
        Args:
            offsprings: Array com descendentes
            
        Returns:
            Array com descendentes mutados
        """
        mutants = np.empty(offsprings.shape)
        
        for i in range(mutants.shape[0]):
            random_value = rd.random()
            mutants[i, :] = offsprings[i, :]
            
            if random_value <= self.mutation_rate:
                # Seleciona gene aleatório para mutar
                int_random_value = randint(0, offsprings.shape[1] - 1)
                # Inverte o bit
                mutants[i, int_random_value] = 1 - mutants[i, int_random_value]
                
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
            
            # Seleciona os melhores para reprodução
            parents = self._selection(fitness, num_parents, population)
            
            # Gera descendentes via crossover
            offsprings = self._crossover(parents, num_offsprings)
            
            # Aplica mutação
            mutants = self._mutation(offsprings)
            
            # Forma nova população (pais + mutantes)
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
        
        return selected_items, total_value, total_cost, history_df
    
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
            'melhor_fitness': float(self.best_fitness)
        }


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
    print("=" * 60)
    print("FarmGeneticOptimizer - Otimização de Recursos Agrícolas")
    print("=" * 60)
    
    items_df = generate_sample_farm_items(num_items=20)
    budget = 150
    
    print(f"\nOrçamento disponível: R$ {budget}")
    print(f"\nCulturas disponíveis:\n{items_df}")
    
    # Cria e executa o otimizador
    optimizer = FarmGeneticOptimizer(
        items_df=items_df,
        budget=budget,
        population_size=16,
        num_generations=500,
        crossover_rate=0.8,
        mutation_rate=0.15
    )
    
    print("\nExecutando otimização genética...")
    selected_items, total_value, total_cost, history = optimizer.optimize()
    
    print("\n" + "=" * 60)
    print("RESULTADOS DA OTIMIZAÇÃO")
    print("=" * 60)
    print(f"\nItens selecionados: {', '.join(selected_items)}")
    print(f"Valor total: R$ {total_value}")
    print(f"Custo total: R$ {total_cost} (de R$ {budget})")
    print(f"Orçamento utilizado: {total_cost/budget*100:.1f}%")
    
    # Plota evolução
    fig = optimizer.plot_fitness_evolution()
    plt.savefig('genetic_optimization_evolution.png', dpi=150, bbox_inches='tight')
    print("\nGráfico de evolução salvo em 'genetic_optimization_evolution.png'")
    
    # Mostra resumo
    summary = optimizer.get_summary()
    print(f"\nResumo completo:\n{summary}")
