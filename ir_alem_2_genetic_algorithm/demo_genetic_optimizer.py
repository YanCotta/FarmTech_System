#!/usr/bin/env python3
"""
Demo: FarmGeneticOptimizer - Otimização de Recursos Agrícolas
===============================================================

Este script demonstra o uso completo da classe FarmGeneticOptimizer
com diferentes cenários de otimização.

Execute: python demo_genetic_optimizer.py
"""

import sys
import os

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fase_4_dashboard_ml', 'scripts'))

import pandas as pd
import matplotlib.pyplot as plt
from genetic_optimizer import FarmGeneticOptimizer, generate_sample_farm_items


def print_separator(title="", char="=", length=70):
    """Imprime um separador formatado"""
    if title:
        padding = (length - len(title) - 2) // 2
        print(f"\n{char * padding} {title} {char * padding}")
    else:
        print(f"\n{char * length}")


def demo_basico():
    """Demonstração básica de uso"""
    print_separator("DEMO 1: Uso Básico", "=")
    
    # Dados simples
    culturas = pd.DataFrame({
        'Nome': ['Soja', 'Milho', 'Trigo', 'Arroz'],
        'Custo': [5000, 3000, 2000, 4000],
        'Valor': [8000, 5000, 3500, 7000]
    })
    
    print("\n📊 DADOS DE ENTRADA")
    print("─" * 70)
    print(culturas.to_string(index=False))
    print(f"\nOrçamento disponível: R$ 10,000.00")
    
    # Otimização
    print("\n🧬 EXECUTANDO ALGORITMO GENÉTICO...")
    print("Configuração: 20 indivíduos, 50 gerações")
    
    otimizador = FarmGeneticOptimizer(
        items_df=culturas,
        budget=10000,
        population_size=20,
        num_generations=50
    )
    
    itens, valor, custo, hist = otimizador.optimize()
    
    # Resultados
    print_separator("RESULTADOS", "─")
    print(f"\n✅ Culturas selecionadas: {', '.join(itens)}")
    print(f"💰 Valor total esperado: R$ {valor:,.2f}")
    print(f"💸 Custo total: R$ {custo:,.2f}")
    print(f"📊 Orçamento utilizado: {(custo/10000)*100:.1f}%")
    print(f"📈 Lucro líquido: R$ {valor - custo:,.2f}")
    print(f"🎯 Convergência na geração: {otimizador.convergence_generation}")


def demo_comparacao_estrategias():
    """Compara diferentes configurações do AG"""
    print_separator("DEMO 2: Comparação de Estratégias", "=")
    
    culturas = generate_sample_farm_items(num_items=15, seed=42)
    budget = 100
    
    print(f"\n📊 Dataset: 15 culturas aleatórias")
    print(f"💰 Orçamento: R$ {budget}")
    
    estrategias = [
        {
            'nome': 'Conservadora',
            'config': {
                'mutation_rate': 0.05,
                'crossover_type': 'single_point',
                'num_generations': 100
            }
        },
        {
            'nome': 'Balanceada',
            'config': {
                'mutation_rate': 0.15,
                'crossover_type': 'single_point',
                'num_generations': 100
            }
        },
        {
            'nome': 'Exploratória',
            'config': {
                'mutation_rate': 0.30,
                'crossover_type': 'random_point',
                'num_generations': 100
            }
        }
    ]
    
    print("\n🔬 TESTANDO 3 ESTRATÉGIAS:")
    print("─" * 70)
    
    resultados = []
    
    for estrategia in estrategias:
        print(f"\n⚙️  Estratégia: {estrategia['nome']}")
        print(f"   Mutação: {estrategia['config']['mutation_rate']}")
        print(f"   Crossover: {estrategia['config']['crossover_type']}")
        
        opt = FarmGeneticOptimizer(
            items_df=culturas,
            budget=budget,
            population_size=20,
            **estrategia['config']
        )
        
        itens, valor, custo, hist = opt.optimize()
        
        resultados.append({
            'Estratégia': estrategia['nome'],
            'Valor': valor,
            'Custo': custo,
            'Itens': len(itens),
            'Convergência': opt.convergence_generation
        })
        
        print(f"   ✅ Valor: R$ {valor:.2f} | Itens: {len(itens)} | Conv: Gen {opt.convergence_generation}")
    
    # Resumo comparativo
    print_separator("COMPARAÇÃO FINAL", "─")
    df_resultados = pd.DataFrame(resultados)
    print("\n" + df_resultados.to_string(index=False))
    
    melhor_idx = df_resultados['Valor'].idxmax()
    melhor = df_resultados.iloc[melhor_idx]
    print(f"\n🏆 MELHOR ESTRATÉGIA: {melhor['Estratégia']} (R$ {melhor['Valor']:.2f})")


def demo_analise_sensibilidade():
    """Demonstra análise de sensibilidade de orçamento"""
    print_separator("DEMO 3: Análise de Sensibilidade de Orçamento", "=")
    
    culturas = pd.DataFrame({
        'Nome': ['Soja', 'Milho', 'Trigo', 'Arroz', 'Feijão', 'Café'],
        'Custo': [50, 30, 20, 40, 25, 60],
        'Valor': [80, 50, 35, 70, 45, 100]
    })
    
    print("\n📊 Culturas disponíveis:")
    print(culturas.to_string(index=False))
    
    otimizador = FarmGeneticOptimizer(
        items_df=culturas,
        budget=150,  # Orçamento base
        population_size=16,
        num_generations=50
    )
    
    print("\n🔬 ANALISANDO IMPACTO DO ORÇAMENTO...")
    
    # Análise
    budget_range = [50, 100, 150, 200, 250]
    sensibilidade = otimizador.analyze_budget_sensitivity(budget_range)
    
    print_separator("RESULTADOS DA ANÁLISE", "─")
    print("\n" + sensibilidade.to_string(index=False))
    
    # Análise de ROI incremental
    print("\n💡 INSIGHTS:")
    for i in range(1, len(sensibilidade)):
        diff_orcamento = sensibilidade.iloc[i]['Orcamento'] - sensibilidade.iloc[i-1]['Orcamento']
        diff_valor = sensibilidade.iloc[i]['Valor_Total'] - sensibilidade.iloc[i-1]['Valor_Total']
        roi_incremental = (diff_valor / diff_orcamento) * 100 if diff_orcamento > 0 else 0
        
        print(f"   Aumentar de R$ {sensibilidade.iloc[i-1]['Orcamento']:.0f} → "
              f"R$ {sensibilidade.iloc[i]['Orcamento']:.0f}: "
              f"ROI incremental de {roi_incremental:.1f}%")


def demo_visualizacao():
    """Demonstra geração de gráficos"""
    print_separator("DEMO 4: Visualização de Evolução", "=")
    
    culturas = generate_sample_farm_items(num_items=20, seed=123)
    
    print("\n📊 Executando otimização com 20 culturas...")
    
    otimizador = FarmGeneticOptimizer(
        items_df=culturas,
        budget=150,
        population_size=30,
        num_generations=200
    )
    
    itens, valor, custo, hist = otimizador.optimize()
    
    print(f"✅ Otimização concluída!")
    print(f"   Valor: R$ {valor:.2f} | Custo: R$ {custo:.2f}")
    
    # Gerar gráfico
    print("\n📈 Gerando visualização...")
    fig = otimizador.plot_fitness_evolution(figsize=(14, 6))
    
    output_file = 'demo_genetic_evolution.png'
    fig.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"✅ Gráfico salvo: {output_file}")
    
    # Análise detalhada
    print("\n📋 TOP 5 ITENS SELECIONADOS (por ROI):")
    print("─" * 70)
    detalhes = otimizador.get_detailed_results()
    top5 = detalhes[detalhes['Selecionado'] == 1].head(5)
    print(top5[['Nome', 'Custo', 'Valor', 'ROI']].to_string(index=False))


def main():
    """Função principal que executa todas as demos"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🧬 FarmGeneticOptimizer - Demonstração")
    print(" " * 20 + "Algoritmos Genéticos na Agritech")
    print("=" * 70)
    
    try:
        # Executa todas as demos
        demo_basico()
        demo_comparacao_estrategias()
        demo_analise_sensibilidade()
        demo_visualizacao()
        
        # Mensagem final
        print_separator("DEMONSTRAÇÃO CONCLUÍDA", "=")
        print("\n✨ Todas as funcionalidades foram demonstradas com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("   - README: fase_4_dashboard_ml/scripts/README_GENETIC_OPTIMIZER.md")
        print("   - Código: fase_4_dashboard_ml/scripts/genetic_optimizer.py")
        print("   - Testes: fase_4_dashboard_ml/tests/test_genetic_optimizer.py")
        print("\n" + "=" * 70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstração interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRO durante demonstração: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
