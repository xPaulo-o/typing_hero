"""
Módulo de otimizações de performance para Typing Hero
Inclui cache de renderização, detecção de hardware e FPS adaptativo
"""

import pygame
import time
from typing import Dict, Tuple, Optional

class TextCache:
    """Cache para surfaces de texto renderizadas"""
    def __init__(self, max_size: int = 500):
        self.cache: Dict[Tuple[str, int, Tuple[int, int, int]], pygame.Surface] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int]) -> pygame.Surface:
        """Obtém ou cria uma surface de texto renderizada"""
        key = (text, id(font), color)
        
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        # Se o cache está cheio, remove o item mais antigo
        if len(self.cache) >= self.max_size:
            # Remove o primeiro item (FIFO simples)
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        
        surface = font.render(text, True, color)
        self.cache[key] = surface
        self.misses += 1
        return surface
    
    def clear(self):
        """Limpa o cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, float]:
        """Retorna estatísticas do cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "size": len(self.cache)
        }


class PerformanceMonitor:
    """Monitora performance e ajusta qualidade automaticamente"""
    def __init__(self, target_fps: int = 60):
        self.target_fps = target_fps
        self.current_fps = target_fps
        self.frame_times = []
        self.max_samples = 60  # Amostras dos últimos 60 frames
        self.quality_level = 1.0  # 1.0 = máxima qualidade, 0.5 = reduzida
        
    def update(self, frame_time: float):
        """Atualiza monitoramento de performance"""
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
        
        # Calcula FPS médio
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1000.0 / avg_frame_time if avg_frame_time > 0 else self.target_fps
        
        # Ajusta qualidade baseado no FPS
        if self.current_fps < self.target_fps * 0.8:  # Se FPS está abaixo de 80% do alvo
            self.quality_level = max(0.5, self.quality_level - 0.05)
        elif self.current_fps >= self.target_fps * 0.95:  # Se FPS está bom
            self.quality_level = min(1.0, self.quality_level + 0.01)
    
    def get_quality_multiplier(self) -> float:
        """Retorna multiplicador de qualidade (0.5 a 1.0)"""
        return self.quality_level
    
    def should_skip_frame(self) -> bool:
        """Determina se deve pular frame de animação para economizar recursos"""
        return self.quality_level < 0.7


def detect_hardware_capabilities() -> Dict[str, any]:
    """Detecta capacidades do hardware"""
    info = pygame.display.Info()
    
    # Estima capacidade baseado na resolução e outras métricas
    total_pixels = info.current_w * info.current_h
    
    # Classifica hardware (básico, médio, alto)
    if total_pixels <= 1920 * 1080:
        tier = "low"
        suggested_fps = 30
    elif total_pixels <= 2560 * 1440:
        tier = "medium"
        suggested_fps = 60
    else:
        tier = "high"
        suggested_fps = 60
    
    return {
        "tier": tier,
        "suggested_fps": suggested_fps,
        "width": info.current_w,
        "height": info.current_h,
        "total_pixels": total_pixels
    }


# Instância global do cache de texto
text_cache = TextCache()

# Instância global do monitor de performance
performance_monitor = PerformanceMonitor()



