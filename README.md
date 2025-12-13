# 🎮 Typing Hero

Um jogo de digitação em português desenvolvido com Python e Pygame, onde você precisa digitar palavras que caem na tela antes que elas atinjam o final. Teste sua velocidade de digitação e expanda seu vocabulário enquanto se diverte!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Índice

- [Sobre o Jogo](#-sobre-o-jogo)
- [Características](#-características)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Como Jogar](#-como-jogar)
- [Mecânicas do Jogo](#-mecânicas-do-jogo)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Otimizações de Performance](#-otimizações-de-performance)
- [Desenvolvimento](#-desenvolvimento)
- [Troubleshooting](#-troubleshooting)
- [Licença](#-licença)

---

## 🎯 Sobre o Jogo

**Typing Hero** é um jogo de digitação educacional que combina diversão com aprendizado. O objetivo é digitar palavras em português que aparecem na tela antes que elas caiam e desapareçam. O jogo possui 13 fases progressivas, cada uma com palavras de diferentes tamanhos e dificuldades, desde palavras simples de 3 letras até palavras complexas de 13+ letras.

### Objetivo
- Digite as palavras corretamente antes que elas atinjam o final da tela
- Mantenha sua energia acima de zero
- Alcance a maior pontuação possível
- Desbloqueie novas fases conforme progride

---

## ✨ Características

### 🎮 Gameplay
- **13 Fases Progressivas**: Cada fase aumenta em dificuldade
- **Sistema de Energia**: Gerencie sua energia - acertos aumentam, erros diminuem
- **Sistema de Combo**: Acertos consecutivos multiplicam sua pontuação
- **Palavras Especiais**: Palavras especiais (10% de chance) dão bônus extras
- **Modo Bônus**: Quando a energia está no máximo, você entra no modo bônus
- **Aceleração Progressiva**: A velocidade das palavras aumenta durante a música

### 🎨 Interface
- **Animações GIF**: Backgrounds animados em menus e gameplay
- **Design Responsivo**: Adapta-se automaticamente à resolução da tela
- **Menus Intuitivos**: Interface fácil de navegar
- **Feedback Visual**: Indicadores claros de combo, energia e pontuação

### 💾 Sistema de Progresso
- **Salvamento Automático**: Pontuações máximas são salvas automaticamente
- **Fases Desbloqueadas**: Progresso é mantido entre sessões
- **Estatísticas**: Acompanhe suas melhores pontuações por fase

### ⚡ Performance
- **Otimização Automática**: Detecta hardware e ajusta performance
- **FPS Adaptativo**: 30 FPS para PCs fracos, 60 FPS para PCs mais potentes
- **Cache Inteligente**: Sistema de cache reduz renderizações desnecessárias
- **Monitoramento em Tempo Real**: Ajusta qualidade automaticamente

---

## 💻 Requisitos do Sistema

### Mínimos
- **Sistema Operacional**: Windows 7+, macOS 10.9+, ou Linux
- **Python**: 3.8 ou superior
- **RAM**: 512 MB
- **Espaço em Disco**: 50 MB
- **Resolução**: 1280x720 (mínimo recomendado)

### Recomendados
- **Sistema Operacional**: Windows 10+, macOS 11+, ou Linux moderno
- **Python**: 3.11 ou superior
- **RAM**: 2 GB ou mais
- **Resolução**: 1920x1080 ou superior

### Dependências
- `pygame-ce` >= 2.5.0 (ou `pygame` >= 2.6.0)
- `Pillow` >= 10.0.0

---

## 🚀 Instalação

### 1. Clone ou Baixe o Repositório

```bash
git clone https://github.com/seu-usuario/TypingHero.git
cd TypingHero
```

Ou baixe o arquivo ZIP e extraia.

### 2. Instale o Python

Certifique-se de ter Python 3.8 ou superior instalado. Você pode verificar com:

```bash
python --version
```

### 3. Instale as Dependências

#### Windows
```bash
python -m pip install -r requirements.txt
```

#### macOS/Linux
```bash
python3 -m pip install -r requirements.txt
```

**Nota**: Se você estiver usando Python 3.14 ou superior, o jogo usará automaticamente `pygame-ce` que tem melhor suporte para versões mais recentes do Python.

### 4. Execute o Jogo

```bash
python typing_hero.py
```

Ou:

```bash
python3 typing_hero.py
```

---

## 🎮 Como Jogar

### Controles

| Ação | Tecla |
|------|-------|
| Digitar palavra | Teclado |
| Confirmar palavra | `Enter` |
| Apagar caractere | `Backspace` |
| Pausar jogo | `ESC` |
| Sair do jogo | `X` (janela) ou botão SAIR |

### Objetivo do Jogo

1. **Digite as palavras** que aparecem na tela antes que elas caiam
2. **Pressione Enter** para confirmar a palavra digitada
3. **Mantenha sua energia** acima de zero
4. **Acumule combos** para multiplicar sua pontuação
5. **Complete a fase** ou tente alcançar a maior pontuação possível

### Dicas

- ✨ **Palavras Especiais** (em ciano) dão mais pontos - priorize-as!
- 🔥 **Combos** aumentam significativamente sua pontuação
- ⚡ **Modo Bônus** ativa quando a energia está no máximo
- 🎯 **Foque na precisão** - erros custam mais energia
- 📈 **A velocidade aumenta** durante a música - prepare-se!

---

## 🎲 Mecânicas do Jogo

### Sistema de Energia
- **Energia Inicial**: 50/100
- **Energia Máxima**: 100
- **Ganho por Acerto**: +10 pontos
- **Perda por Erro**: -15 pontos
- **Perda por Palavra Perdida**: -5 pontos
- **Game Over**: Quando energia chega a 0

### Sistema de Pontuação
- **Pontuação Base**: 1 ponto por palavra normal
- **Palavra Especial**: 10 pontos base
- **Multiplicador de Combo**: 
  - Combo x1: 1x
  - Combo x2: 2x (após 10 acertos)
  - Combo x3: 3x (após 20 acertos)
  - Combo x4: 4x (após 30 acertos) - máximo
- **Bônus de Palavra Especial**: +10x multiplicador extra no modo bônus

### Sistema de Fases
- **Fase 1**: Palavras de 3 letras, velocidade 1
- **Fase 2**: Palavras de 4 letras, velocidade 1-2
- **Fase 3**: Palavras de 5 letras, velocidade 1-2
- **Fase 4**: Palavras de 6 letras, velocidade 1-2
- **Fase 5**: Palavras de 7 letras, velocidade 2
- **Fase 6**: Palavras de 8 letras, velocidade 2
- **Fase 7**: Palavras de 9 letras, velocidade 2
- **Fase 8**: Palavras de 10 letras, velocidade 2
- **Fase 9**: Palavras de 11 letras, velocidade 2-3
- **Fase 10**: Palavras de 12 letras, velocidade 2-3
- **Fase 11**: Palavras de 13 letras, velocidade 2-3
- **Fase 12**: Palavras de 14+ letras, velocidade 3
- **Fase 13**: Palavras com "C", velocidade 3-4

### Desbloqueio de Fases
- A **Fase 1** começa desbloqueada
- Para desbloquear a próxima fase, você precisa:
  - Completar a fase atual OU
  - Alcançar uma pontuação > 0 na fase atual

---

## 📁 Estrutura do Projeto

```
TypingHero/
│
├── typing_hero.py          # Arquivo principal do jogo
├── settings.py            # Configurações e constantes
├── fases.py               # Dicionário com todas as fases e palavras
├── gamedata.py            # Sistema de save/load
├── performance.py         # Módulo de otimizações de performance
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
├── OTIMIZACOES.md         # Documentação das otimizações
│
├── img/                   # Imagens e GIFs
│   ├── menu_typing.gif    # Background animado do menu
│   ├── pause_menu2.png    # Menu de pausa
│   ├── game_over.jpeg     # Tela de game over
│   ├── win_screen.gif     # Tela de vitória
│   ├── fase_menu.png      # Menu de seleção de fases
│   └── ...
│
├── sounds/                # Arquivos de áudio
│   ├── audio_menu.mp3     # Música do menu
│   ├── gameplay_music.mp3 # Música do gameplay
│   └── click.ogg          # Som de clique dos botões
│
├── videos/                 # Vídeos e GIFs de background
│   ├── fundo_gameplay3.gif # Background animado do gameplay
│   └── ...
│
└── save_data.json         # Arquivo de salvamento (criado automaticamente)
```

### Descrição dos Arquivos

#### `typing_hero.py`
Arquivo principal contendo toda a lógica do jogo:
- Loop principal do jogo
- Gerenciamento de estados (menu, jogo, pause, etc.)
- Sistema de input e renderização
- Lógica de gameplay

#### `settings.py`
Configurações globais do jogo:
- Cores
- Constantes de gameplay (energia, pontuação, etc.)
- Carregamento de recursos (imagens, sons)
- Funções auxiliares (botões, texto com outline)

#### `fases.py`
Contém todas as fases do jogo:
- Dicionário com 13 fases
- Palavras de cada fase
- Velocidades mínima e máxima por fase

#### `gamedata.py`
Sistema de persistência:
- Salva pontuações máximas
- Salva fases desbloqueadas
- Usa JSON para armazenamento

#### `performance.py`
Módulo de otimizações:
- Cache de renderização de texto
- Monitoramento de performance
- Detecção de hardware
- Ajuste automático de qualidade

---

## ⚡ Otimizações de Performance

O jogo inclui várias otimizações para garantir bom desempenho em diferentes tipos de hardware:

### 1. Sistema de Cache de Texto
- Armazena até 500 surfaces de texto renderizadas
- Reduz chamadas a `font.render()` em até 90%
- Melhora significativa em PCs mais fracos

### 2. FPS Adaptativo
- Detecta hardware automaticamente
- Ajusta FPS alvo: 30 FPS (PCs fracos) ou 60 FPS (PCs médios/fortes)
- Melhora compatibilidade universal

### 3. Monitoramento de Performance
- Monitora FPS em tempo real
- Ajusta qualidade automaticamente quando FPS cai
- Reduz animações em hardware limitado

### 4. Otimização de Listas
- Remoção eficiente de palavras (evita O(n²))
- Uso de `pop(i)` em vez de `remove()` em loops

### 5. Renderização Otimizada
- Remove renderizações duplicadas
- Reutiliza surfaces quando possível
- Pula frames de animação quando necessário

Para mais detalhes, consulte [OTIMIZACOES.md](OTIMIZACOES.md).

---

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Pygame/Pygame-CE**: Biblioteca de jogos
- **Pillow (PIL)**: Processamento de imagens (GIFs)
- **JSON**: Armazenamento de dados

### Arquitetura

O jogo segue uma arquitetura modular:
- **Separação de responsabilidades**: Cada módulo tem uma função específica
- **Configuração centralizada**: Todas as constantes em `settings.py`
- **Sistema de estados**: Menu, jogo, pause, game over, etc.
- **Otimizações isoladas**: Módulo `performance.py` separado

### Adicionando Novas Fases

Para adicionar uma nova fase, edite `fases.py`:

```python
14: {
    "palavras": ["palavra1", "palavra2", ...],
    "min_speed": 2,
    "max_speed": 3
}
```

### Personalizando Configurações

Edite `settings.py` para ajustar:
- Cores
- Pontuações
- Energia
- Velocidades
- Intervalos de spawn

---

## 🐛 Troubleshooting

### Problema: "Import pygame could not be resolved"

**Solução**: Instale pygame ou pygame-ce:
```bash
pip install pygame-ce
```

### Problema: Jogo está lento

**Soluções**:
1. O jogo detecta automaticamente seu hardware e ajusta FPS
2. Verifique se há outros programas pesados rodando
3. Reduza a resolução da tela se necessário

### Problema: Erro ao carregar imagens/sons

**Solução**: Certifique-se de que todos os arquivos estão nas pastas corretas:
- `img/` para imagens
- `sounds/` para áudios
- `videos/` para GIFs de background

### Problema: Save não funciona

**Solução**: Verifique permissões de escrita na pasta do jogo. O arquivo `save_data.json` será criado automaticamente.

### Problema: Python 3.14 não instala pygame

**Solução**: O jogo usa automaticamente `pygame-ce` que tem suporte para Python 3.14. Instale com:
```bash
pip install pygame-ce
```

---

## 📝 Changelog

### Versão Atual
- ✅ Sistema de cache de texto
- ✅ FPS adaptativo baseado em hardware
- ✅ Monitoramento de performance em tempo real
- ✅ Otimizações de renderização
- ✅ 13 fases progressivas
- ✅ Sistema de save/load
- ✅ Interface responsiva
- ✅ Animações GIF
- ✅ Sistema de combo e palavras especiais

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Adicionar novas fases
- Melhorar a documentação
- Otimizar o código

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.

---

## 👤 Autor

Desenvolvido com ❤️ usando Python e Pygame.

---

## 🙏 Agradecimentos

- Comunidade Pygame
- Desenvolvedores do pygame-ce
- Todos os testadores e contribuidores

---

## 📧 Contato

Para dúvidas, sugestões ou problemas, abra uma issue no repositório.

---

**Divirta-se jogando Typing Hero! 🎮✨**

