"""
Lexer package for MinLang Compiler
"""

from .token import Token, TokenType, KEYWORDS, OPERATORS, DELIMITERS
from .lexer import Lexer, LexerError, tokenize_file, tokenize_string


def tokenize(source: str):
    """Compatibility helper: tokenize source text into a token list."""
    return tokenize_string(source)

__all__ = [
    'Token',
    'TokenType',
    'KEYWORDS',
    'OPERATORS',
    'DELIMITERS',
    'Lexer',
    'LexerError',
    'tokenize',
    'tokenize_file',
    'tokenize_string',
]
