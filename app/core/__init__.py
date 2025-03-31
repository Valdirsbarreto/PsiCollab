"""
Módulo principal da IA - Core
"""

from .config import settings
from .knowledge_manager import KnowledgeManager
from .embedding_generator import EmbeddingGenerator

__all__ = [
    'settings',
    'KnowledgeManager',
    'EmbeddingGenerator'
] 