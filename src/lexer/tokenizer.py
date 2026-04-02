"""
Lexical Analyzer (Tokenizer) for MinLang Compiler
Converts source code into a stream of tokens
"""

from typing import List, Optional
import re
from .token_types import (
    Token, TokenType, KEYWORDS, OPERATORS, DELIMITERS,
    is_keyword, get_keyword_token_type, is_operator, is_delimiter
)


class LexerError(Exception):
    """Custom exception for lexical analysis errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at {line}:{column} - {message}")


class Tokenizer:
    """
    Lexical Analyzer for MinLang
    
    Performs lexical analysis by scanning source code character by character
    and producing a stream of tokens.
    """
    
    def __init__(self, source_code: str, filename: str = "<stdin>"):
        """
        Initialize the tokenizer
        
        Args:
            source_code: The source code to tokenize
            filename: Name of the source file (for error reporting)
        """
        self.source = source_code
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.current_char = self.source[0] if source_code else None
    
    def error(self, message: str) -> None:
        """Raise a lexer error with current position"""
        raise LexerError(message, self.line, self.column)
    
    def advance(self) -> None:
        """Move to the next character in the source code"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """
        Look ahead at the character at position + offset
        
        Args:
            offset: Number of positions to look ahead
            
        Returns:
            The character at position + offset, or None if out of bounds
        """
        peek_pos = self.position + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters except newlines"""
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip single-line comments (// ... \n)"""
        if self.current_char == '/' and self.peek() == '/':
            # Skip until end of line
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
    
    def skip_multiline_comment(self) -> None:
        """Skip multi-line comments (/* ... */)"""
        if self.current_char == '/' and self.peek() == '*':
            self.advance()  # Skip /
            self.advance()  # Skip *
            
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # Skip *
                    self.advance()  # Skip /
                    return
                self.advance()
            
            self.error("Unterminated multi-line comment")
    
    def read_number(self) -> Token:
        """
        Read a numeric literal (integer or float)
        
        Returns:
            Token with type INTEGER_LITERAL or FLOAT_LITERAL
        """
        start_line = self.line
        start_column = self.column
        num_str = ''
        is_float = False
        
        # Read digits
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    self.error("Invalid number: multiple decimal points")
                is_float = True
                
                # Check if next char is a digit
                if self.peek() is None or not self.peek().isdigit():
                    self.error("Invalid number: decimal point must be followed by digits")
            
            num_str += self.current_char
            self.advance()
        
        # Determine token type and convert value
        if is_float:
            return Token(
                TokenType.FLOAT_LITERAL,
                float(num_str),
                start_line,
                start_column,
                self.filename
            )
        else:
            return Token(
                TokenType.INTEGER_LITERAL,
                int(num_str),
                start_line,
                start_column,
                self.filename
            )
    
    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword
        
        Returns:
            Token with type IDENTIFIER or keyword type
        """
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        # Read alphanumeric characters and underscores
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        if is_keyword(identifier):
            token_type = get_keyword_token_type(identifier)
            return Token(
                token_type,
                identifier,
                start_line,
                start_column,
                self.filename
            )
        
        # It's an identifier
        return Token(
            TokenType.IDENTIFIER,
            identifier,
            start_line,
            start_column,
            self.filename
        )
    
    def read_char_literal(self) -> Token:
        """
        Read a character literal ('c')
        
        Returns:
            Token with type CHAR_LITERAL
        """
        start_line = self.line
        start_column = self.column
        
        self.advance()  # Skip opening '
        
        if self.current_char is None:
            self.error("Unterminated character literal")
        
        # Handle escape sequences
        if self.current_char == '\\':
            self.advance()
            if self.current_char is None:
                self.error("Unterminated character literal")
            
            escape_chars = {
                'n': '\n',
                't': '\t',
                'r': '\r',
                '\\': '\\',
                '\'': '\'',
                '0': '\0'
            }
            
            if self.current_char in escape_chars:
                char_value = escape_chars[self.current_char]
            else:
                self.error(f"Invalid escape sequence: \\{self.current_char}")
        else:
            char_value = self.current_char
        
        self.advance()
        
        if self.current_char != '\'':
            self.error("Unterminated character literal (expected closing ')")
        
        self.advance()  # Skip closing '
        
        return Token(
            TokenType.CHAR_LITERAL,
            char_value,
            start_line,
            start_column,
            self.filename
        )
    
    def read_string_literal(self) -> Token:
        """
        Read a string literal ("string")
        
        Returns:
            Token with type STRING_LITERAL
        """
        start_line = self.line
        start_column = self.column
        
        self.advance()  # Skip opening "
        string_value = ''
        
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    self.error("Unterminated string literal")
                
                escape_chars = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    '0': '\0'
                }
                
                if self.current_char in escape_chars:
                    string_value += escape_chars[self.current_char]
                else:
                    self.error(f"Invalid escape sequence: \\{self.current_char}")
            else:
                string_value += self.current_char
            
            self.advance()
        
        if self.current_char is None:
            self.error("Unterminated string literal (missing closing \")")
        
        self.advance()  # Skip closing "
        
        return Token(
            TokenType.STRING_LITERAL,
            string_value,
            start_line,
            start_column,
            self.filename
        )
    
    def read_operator(self) -> Token:
        """
        Read an operator (can be 1 or 2 characters)
        
        Returns:
            Token with appropriate operator type
        """
        start_line = self.line
        start_column = self.column
        
        # Try to match two-character operators first
        if self.current_char is not None and self.peek() is not None:
            two_char = self.current_char + self.peek()
            if two_char in OPERATORS:
                self.advance()
                self.advance()
                return Token(
                    OPERATORS[two_char],
                    two_char,
                    start_line,
                    start_column,
                    self.filename
                )
        
        # Single character operator
        char = self.current_char
        self.advance()
        
        if char in OPERATORS:
            return Token(
                OPERATORS[char],
                char,
                start_line,
                start_column,
                self.filename
            )
        
        self.error(f"Invalid operator: {char}")
    
    def get_next_token(self) -> Optional[Token]:
        """
        Get the next token from the source code
        
        Returns:
            The next Token, or None if end of file
        """
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Skip newlines (but track line numbers)
            if self.current_char == '\n':
                self.advance()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            if self.current_char == '/' and self.peek() == '*':
                self.skip_multiline_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.read_number()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Character literals
            if self.current_char == '\'':
                return self.read_char_literal()
            
            # String literals
            if self.current_char == '"':
                return self.read_string_literal()
            
            # Delimiters
            if is_delimiter(self.current_char):
                char = self.current_char
                line = self.line
                column = self.column
                self.advance()
                return Token(
                    DELIMITERS[char],
                    char,
                    line,
                    column,
                    self.filename
                )
            
            # Operators
            if is_operator(self.current_char):
                return self.read_operator()
            
            # Unknown character
            self.error(f"Unexpected character: '{self.current_char}'")
        
        return None
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code
        
        Returns:
            List of all tokens in the source code
        """
        self.tokens = []
        
        while True:
            token = self.get_next_token()
            if token is None:
                break
            self.tokens.append(token)
        
        # Add EOF token
        self.tokens.append(Token(
            TokenType.EOF,
            None,
            self.line,
            self.column,
            self.filename
        ))
        
        return self.tokens
    
    def print_tokens(self) -> None:
        """Print all tokens (for debugging)"""
        for i, token in enumerate(self.tokens):
            print(f"{i:4d}: {token}")


def tokenize(source_code: str, filename: str = "<stdin>") -> List[Token]:
    """
    Convenience function to tokenize source code
    
    Args:
        source_code: The source code to tokenize
        filename: Name of the source file
        
    Returns:
        List of tokens
    """
    tokenizer = Tokenizer(source_code, filename)
    return tokenizer.tokenize()
