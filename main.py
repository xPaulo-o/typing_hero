#!/usr/bin/env python3
"""
Launcher do Typing Hero
Execute este arquivo para rodar o jogo
"""

import sys
import os

# Adiciona a pasta Components ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Components'))

# Importa e executa o jogo
from typing_hero import run_game

if __name__ == "__main__":
    run_game()
