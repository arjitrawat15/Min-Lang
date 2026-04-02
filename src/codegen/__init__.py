"""
Code Generation package for MinLang Compiler
"""

from .intermediate import (
    TACOpcode, TACInstruction, TACProgram, format_tac_output
)
from .generator import IRGenerator, IRGeneratorError, generate_tac

__all__ = [
    'TACOpcode',
    'TACInstruction',
    'TACProgram',
    'format_tac_output',
    'IRGenerator',
    'IRGeneratorError',
    'generate_tac',
]
