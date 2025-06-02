
import json
import os

SAVE_FILE = "save_data.json"

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

# Exemplo de uso:
# game_data = load_game_data()
# print(game_data["max_scores"])
# print(game_data["unlocked_fases"])