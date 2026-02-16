"""
Token definitions for MinLang Compiler
Defines all token types and the Token class
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """Enumeration of all token types in MinLang"""
    
    # Keywords
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    CHAR = auto()
    VOID = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    CONST = auto()
    TRUE = auto()
    FALSE = auto()
    READ = auto()
    PRINT = auto()
    
    # Identifiers and Literals
    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    CHAR_LITERAL = auto()
    STRING_LITERAL = auto()
    
    # Operators
    # Arithmetic
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    
    # Relational
    LESS_THAN = auto()      # <
    GREATER_THAN = auto()   # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    
    # Logical
    AND = auto()            # &&
    OR = auto()             # ||
    NOT = auto()            # !
    
    # Assignment
    ASSIGN = auto()         # =
    
    # Delimiters
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """
    Represents a single token in the source code
    
    Attributes:
        type: The type of the token (from TokenType enum)
        value: The actual value/lexeme of the token
        line: Line number where token appears
        column: Column number where token starts
    """
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self) -> str:
        """String representation of the token"""
        if self.value is not None and self.type not in [
            TokenType.SEMICOLON, TokenType.COMMA, TokenType.LPAREN,
            TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE
        ]:
            return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"
        return f"Token({self.type.name}, {self.line}:{self.column})"
    
    def __str__(self) -> str:
        """User-friendly string representation"""
        return self.__repr__()


# Keyword mapping
KEYWORDS = {
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'bool': TokenType.BOOL,
    'char': TokenType.CHAR,
    'void': TokenType.VOID,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'return': TokenType.RETURN,
    'const': TokenType.CONST,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'read': TokenType.READ,
    'print': TokenType.PRINT,
}


# Operator mapping for single and double character operators
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '<': TokenType.LESS_THAN,
    '>': TokenType.GREATER_THAN,
    '=': TokenType.ASSIGN,
    '!': TokenType.NOT,
    '<=': TokenType.LESS_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
    '==': TokenType.EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '&&': TokenType.AND,
    '||': TokenType.OR,
}


# Delimiter mapping
DELIMITERS = {
    ';': TokenType.SEMICOLON,
    ',': TokenType.COMMA,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
}


def is_keyword(text: str) -> bool:
    """Check if the given text is a keyword"""
    return text in KEYWORDS


def get_keyword_type(text: str) -> Optional[TokenType]:
    """Get the token type for a keyword"""
    return KEYWORDS.get(text)


def is_operator_char(char: str) -> bool:
    """Check if character can be part of an operator"""
    return char in '+-*/%<>=!&|'


def is_delimiter(char: str) -> bool:
    """Check if character is a delimiter"""
    return char in DELIMITERS
