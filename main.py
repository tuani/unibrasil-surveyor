#!/usr/bin/env python3
import sys
import os
from src.core.drone_optimizer import GerenciadorRota

def main():
    csv_file = "data/coordenadas.csv"
    if not os.path.exists(csv_file):
        print(f"ERRO: Arquivo {csv_file} não encontrado!")
        return 1
    
    try:
        gerenciador = GerenciadorRota(csv_file)
        rota, velocidades, tempos_pouso, fitness = gerenciador.executar()
        gerenciador.gerar_relatorios(rota, velocidades, tempos_pouso, fitness)
        print(f"Rota gerada! Fitness: {fitness:.0f}")
        return 0
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())