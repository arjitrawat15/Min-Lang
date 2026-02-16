"""
Token Type Definitions for MinLang Compiler
Defines all token types and their categories
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
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    
    # Relational Operators
    LESS_THAN = auto()      # <
    GREATER_THAN = auto()   # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    
    # Logical Operators
    AND = auto()            # &&
    OR = auto()             # ||
    NOT = auto()            # !
    
    # Assignment
    ASSIGN = auto()         # =
    
    # Delimiters
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class Token:
    """
    Represents a single token in the source code
    
    Attributes:
        type: The token type (from TokenType enum)
        value: The actual value/lexeme
        line: Line number in source code
        column: Column number in source code
        file: Source file name (optional)
    """
    type: TokenType
    value: Any
    line: int
    column: int
    file: Optional[str] = None
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"
    
    def __str__(self) -> str:
        """User-friendly string representation"""
        if self.value is not None:
            return f"<{self.type.name}: '{self.value}'>"
        return f"<{self.type.name}>"


# Keyword mapping for fast lookup
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

# Operator mapping
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '<': TokenType.LESS_THAN,
    '>': TokenType.GREATER_THAN,
    '<=': TokenType.LESS_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
    '==': TokenType.EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '&&': TokenType.AND,
    '||': TokenType.OR,
    '!': TokenType.NOT,
    '=': TokenType.ASSIGN,
}

# Delimiter mapping
DELIMITERS = {
    ';': TokenType.SEMICOLON,
    ',': TokenType.COMMA,
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    '[': TokenType.LEFT_BRACKET,
    ']': TokenType.RIGHT_BRACKET,
}


def is_keyword(text: str) -> bool:
    """Check if a given text is a keyword"""
    return text in KEYWORDS


def get_keyword_token_type(text: str) -> Optional[TokenType]:
    """Get the TokenType for a keyword, or None if not a keyword"""
    return KEYWORDS.get(text)


def is_operator(char: str) -> bool:
    """Check if a character is part of an operator"""
    return char in '+-*/%<>=!&|'


def is_delimiter(char: str) -> bool:
    """Check if a character is a delimiter"""
    return char in DELIMITERS
