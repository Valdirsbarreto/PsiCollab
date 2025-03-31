"""
Processadores de Testes Psicológicos
"""

from .base_processor import BaseTestProcessor
from .wechsler_processor import WechslerProcessor
from .personality_processor import PersonalityProcessor
from .projective_processor import ProjectiveProcessor
from .test_processor_factory import TestProcessorFactory

__all__ = [
    'BaseTestProcessor',
    'WechslerProcessor',
    'PersonalityProcessor',
    'ProjectiveProcessor',
    'TestProcessorFactory'
] 