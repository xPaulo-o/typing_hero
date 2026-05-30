
import json
import os
import sys

# Encontra o diretório de dados relativo à localização deste arquivo
if getattr(sys, "frozen", False):
    DATA_DIR = os.path.join(os.path.dirname(sys.executable), "data")
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
SAVE_FILE = os.path.join(DATA_DIR, "save_data.json")

def load_game_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError: # Caso o arquivo esteja corrompido
                data = {"max_scores": {}, "unlocked_fases": [1]} # Resetar dados
            return data
    return {"max_scores": {}, "unlocked_fases": [1]} # Inicia com fase 1 desbloqueada e sem scores

def save_game_data(data):
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
