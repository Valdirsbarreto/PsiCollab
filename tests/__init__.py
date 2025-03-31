"""
Testes Automatizados
"""

from .test_llm import TestLLM
from .test_processors import TestProcessors
from .test_api import TestAPI

__all__ = [
    'TestLLM',
    'TestProcessors',
    'TestAPI'
] 