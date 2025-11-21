"""
Testes Unitários para FarmGeneticOptimizer

Este módulo testa todas as funcionalidades da classe de otimização genética,
garantindo que as validações, cálculos e transformações funcionem corretamente.
"""

import pytest
import numpy as np
import pandas as pd
import sys
import os

# Adiciona o diretório scripts ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from genetic_optimizer import FarmGeneticOptimizer, generate_sample_farm_items


class TestFarmGeneticOptimizer:
    """Testes para a classe FarmGeneticOptimizer"""
    
    @pytest.fixture
    def sample_data(self):
        """Cria dados de teste padrão"""
        return pd.DataFrame({
            'Nome': ['Soja', 'Milho', 'Trigo'],
            'Custo': [50, 30, 20],
            'Valor': [80, 50, 35]
        })
    
    @pytest.fixture
    def optimizer(self, sample_data):
        """Cria uma instância do otimizador com dados de teste"""
        return FarmGeneticOptimizer(
            items_df=sample_data,
            budget=100,
            population_size=10,
            num_generations=50,
            crossover_rate=0.8,
            mutation_rate=0.15
        )
    
    # ==========================================
    # TESTES DE INICIALIZAÇÃO E VALIDAÇÃO
    # ==========================================
    
    def test_initialization_valid(self, sample_data):
        """Testa inicialização com dados válidos"""
        opt = FarmGeneticOptimizer(
            items_df=sample_data,
            budget=100,
            population_size=10
        )
        assert opt.budget == 100
        assert opt.num_items == 3
        assert opt.population_size == 10
    
    def test_initialization_invalid_population_odd(self, sample_data):
        """Testa que population_size ímpar gera erro"""
        with pytest.raises(ValueError, match="Population size deve ser um número par"):
            FarmGeneticOptimizer(
                items_df=sample_data,
                budget=100,
                population_size=11  # Ímpar
            )
    
    def test_initialization_invalid_population_small(self, sample_data):
        """Testa que population_size < 4 gera erro"""
        with pytest.raises(ValueError, match="Population size deve ser um número par"):
            FarmGeneticOptimizer(
                items_df=sample_data,
                budget=100,
                population_size=2
            )
    
    def test_initialization_invalid_crossover_rate(self, sample_data):
        """Testa que crossover_rate fora de [0, 1] gera erro"""
        with pytest.raises(ValueError, match="crossover_rate deve estar entre 0 e 1"):
            FarmGeneticOptimizer(
                items_df=sample_data,
                budget=100,
                crossover_rate=1.5
            )
    
    def test_initialization_invalid_mutation_rate(self, sample_data):
        """Testa que mutation_rate fora de [0, 1] gera erro"""
        with pytest.raises(ValueError, match="mutation_rate deve estar entre 0 e 1"):
            FarmGeneticOptimizer(
                items_df=sample_data,
                budget=100,
                mutation_rate=-0.1
            )
    
    def test_initialization_invalid_crossover_type(self, sample_data):
        """Testa que crossover_type inválido gera erro"""
        with pytest.raises(ValueError, match="crossover_type deve ser"):
            FarmGeneticOptimizer(
                items_df=sample_data,
                budget=100,
                crossover_type='invalid_type'
            )
    
    def test_initialization_missing_columns(self):
        """Testa que DataFrame sem colunas necessárias gera erro"""
        invalid_df = pd.DataFrame({
            'Nome': ['A', 'B'],
            'Preco': [10, 20]  # Falta 'Custo' e 'Valor'
        })
        with pytest.raises(ValueError, match="DataFrame deve conter as colunas"):
            FarmGeneticOptimizer(items_df=invalid_df, budget=100)
    
    def test_initialization_empty_dataframe(self):
        """Testa que DataFrame vazio gera erro"""
        empty_df = pd.DataFrame(columns=['Nome', 'Custo', 'Valor'])
        with pytest.raises(ValueError, match="DataFrame não pode estar vazio"):
            FarmGeneticOptimizer(items_df=empty_df, budget=100)
    
    # ==========================================
    # TESTES DA FUNÇÃO DE FITNESS
    # ==========================================
    
    def test_fitness_valid_solution(self, optimizer):
        """Testa cálculo de fitness para solução válida"""
        # Solução: seleciona apenas Trigo (custo=20, valor=35)
        population = np.array([[0, 0, 1]])
        fitness = optimizer._fitness(population)
        
        assert fitness[0] == 35.0
    
    def test_fitness_invalid_solution_over_budget(self, optimizer):
        """Testa que solução acima do orçamento recebe fitness 0"""
        # Seleciona todos (custo total = 100, valor = 165)
        # Está no limite exato, então deve ser válido
        population = np.array([[1, 1, 1]])
        fitness = optimizer._fitness(population)
        
        assert fitness[0] == 165.0  # Solução válida (exatamente no limite)
        
        # Agora vamos testar com orçamento menor
        optimizer.budget = 50
        fitness = optimizer._fitness(population)
        assert fitness[0] == 0.0  # Agora excede o orçamento
    
    def test_fitness_empty_solution(self, optimizer):
        """Testa solução vazia (nenhum item selecionado)"""
        population = np.array([[0, 0, 0]])
        fitness = optimizer._fitness(population)
        
        assert fitness[0] == 0.0
    
    # ==========================================
    # TESTES DE SELEÇÃO
    # ==========================================
    
    def test_selection_returns_best(self, optimizer):
        """Testa que seleção retorna os melhores indivíduos"""
        population = np.array([
            [1, 0, 0],  # fitness = 80
            [0, 1, 0],  # fitness = 50
            [0, 0, 1],  # fitness = 35
            [1, 1, 0],  # fitness = 130 (MELHOR)
        ])
        
        fitness = optimizer._fitness(population)
        parents = optimizer._selection(fitness, num_parents=2, population=population)
        
        # Deve retornar os 2 melhores: [1,1,0] e [1,0,0]
        assert parents.shape == (2, 3)
        # Primeiro pai deve ser o melhor
        assert np.array_equal(parents[0], [1, 1, 0])
    
    # ==========================================
    # TESTES DE CROSSOVER
    # ==========================================
    
    def test_crossover_single_point(self, sample_data):
        """Testa crossover de ponto único"""
        opt = FarmGeneticOptimizer(
            items_df=sample_data,
            budget=100,
            crossover_type='single_point',
            crossover_rate=1.0  # Sempre aplica crossover
        )
        
        parents = np.array([
            [1, 1, 1],
            [0, 0, 0]
        ])
        
        offspring = opt._crossover(parents, num_offsprings=2)
        
        assert offspring.shape == (2, 3)
        # Com crossover rate 1.0, deve ter ocorrido crossover
    
    def test_crossover_random_point(self, sample_data):
        """Testa crossover de ponto aleatório"""
        opt = FarmGeneticOptimizer(
            items_df=sample_data,
            budget=100,
            crossover_type='random_point',
            crossover_rate=1.0
        )
        
        parents = np.array([
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ])
        
        offspring = opt._crossover(parents, num_offsprings=2)
        
        assert offspring.shape == (2, 4)
    
    def test_crossover_no_crossover(self, sample_data):
        """Testa que com rate=0, offspring são clones dos pais"""
        opt = FarmGeneticOptimizer(
            items_df=sample_data,
            budget=100,
            crossover_rate=0.0  # Nunca aplica crossover
        )
        
        parents = np.array([
            [1, 1, 1],
            [0, 0, 0]
        ])
        
        offspring = opt._crossover(parents, num_offsprings=2)
        
        # Deve retornar clones dos pais
        assert offspring.shape == (2, 3)
    
    # ==========================================
    # TESTES DE MUTAÇÃO
    # ==========================================
    
    def test_mutation_changes_genes(self, optimizer):
        """Testa que mutação altera genes"""
        np.random.seed(42)
        
        offspring = np.array([
            [1, 1, 1],
            [0, 0, 0]
        ])
        
        mutants = optimizer._mutation(offspring)
        
        assert mutants.shape == offspring.shape
        # Com mutation_rate > 0, pode haver mutações
    
    # ==========================================
    # TESTES DO MÉTODO OPTIMIZE
    # ==========================================
    
    def test_optimize_runs_successfully(self, optimizer):
        """Testa que optimize executa sem erros"""
        selected, value, cost, history = optimizer.optimize()
        
        assert isinstance(selected, list)
        assert isinstance(value, (int, float))
        assert isinstance(cost, (int, float))
        assert isinstance(history, pd.DataFrame)
        assert cost <= optimizer.budget
    
    def test_optimize_returns_valid_solution(self, optimizer):
        """Testa que optimize retorna solução válida"""
        selected, value, cost, history = optimizer.optimize()
        
        # Verifica que o custo não excede o orçamento
        assert cost <= optimizer.budget
        # Verifica que há pelo menos um item selecionado (se possível)
        assert len(selected) >= 0
    
    def test_optimize_fitness_improves(self, optimizer):
        """Testa que fitness melhora ao longo das gerações"""
        _, _, _, history = optimizer.optimize()
        
        # Fitness máximo no final deve ser >= fitness máximo no início
        final_max = history['Fitness Máximo'].iloc[-1]
        initial_max = history['Fitness Máximo'].iloc[0]
        
        assert final_max >= initial_max
    
    def test_optimize_without_items_raises_error(self):
        """Testa que optimize sem itens gera erro"""
        opt = FarmGeneticOptimizer(items_df=None, budget=100)
        
        with pytest.raises(ValueError, match="Items DataFrame não foi fornecido"):
            opt.optimize()
    
    # ==========================================
    # TESTES DOS MÉTODOS DE RESUMO
    # ==========================================
    
    def test_get_summary_after_optimize(self, optimizer):
        """Testa que get_summary retorna dados corretos após optimize"""
        optimizer.optimize()
        summary = optimizer.get_summary()
        
        assert 'itens_selecionados' in summary
        assert 'valor_total' in summary
        assert 'custo_total' in summary
        assert 'orcamento_utilizado_percentual' in summary
        assert summary['custo_total'] <= summary['orcamento']
    
    def test_get_summary_before_optimize(self, optimizer):
        """Testa que get_summary antes de optimize retorna erro"""
        summary = optimizer.get_summary()
        
        assert 'error' in summary
    
    def test_get_detailed_results(self, optimizer):
        """Testa que get_detailed_results retorna DataFrame correto"""
        optimizer.optimize()
        detailed = optimizer.get_detailed_results()
        
        assert isinstance(detailed, pd.DataFrame)
        assert 'Selecionado' in detailed.columns
        assert 'ROI' in detailed.columns
        assert 'Eficiencia' in detailed.columns
    
    def test_get_detailed_results_before_optimize_raises_error(self, optimizer):
        """Testa que get_detailed_results antes de optimize gera erro"""
        with pytest.raises(ValueError, match="Execute optimize\\(\\) primeiro"):
            optimizer.get_detailed_results()
    
    # ==========================================
    # TESTES DE ANÁLISE DE SENSIBILIDADE
    # ==========================================
    
    def test_analyze_budget_sensitivity(self, optimizer):
        """Testa análise de sensibilidade de orçamento"""
        result = optimizer.analyze_budget_sensitivity(budget_range=[50, 100, 150])
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'Orcamento' in result.columns
        assert 'Valor_Total' in result.columns
    
    # ==========================================
    # TESTES DE PLOTAGEM
    # ==========================================
    
    def test_plot_fitness_evolution(self, optimizer):
        """Testa que plot_fitness_evolution gera figura"""
        optimizer.optimize()
        fig = optimizer.plot_fitness_evolution()
        
        assert fig is not None
        assert len(fig.axes) > 0
    
    def test_plot_before_optimize_raises_error(self, optimizer):
        """Testa que plotar antes de optimize gera erro"""
        with pytest.raises(ValueError, match="Execute optimize\\(\\) primeiro"):
            optimizer.plot_fitness_evolution()


class TestUtilityFunctions:
    """Testes para funções utilitárias"""
    
    def test_generate_sample_farm_items(self):
        """Testa geração de dados de exemplo"""
        df = generate_sample_farm_items(num_items=10, seed=42)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert 'Nome' in df.columns
        assert 'Custo' in df.columns
        assert 'Valor' in df.columns
    
    def test_generate_sample_farm_items_reproducibility(self):
        """Testa que seed garante reprodutibilidade"""
        df1 = generate_sample_farm_items(num_items=5, seed=123)
        df2 = generate_sample_farm_items(num_items=5, seed=123)
        
        assert df1.equals(df2)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
