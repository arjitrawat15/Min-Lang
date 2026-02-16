"""
Lexical Analyzer (Lexer) for MinLang Compiler
Converts source code into a stream of tokens
"""

from typing import List, Optional
from .token import (
    Token, TokenType, KEYWORDS, OPERATORS, DELIMITERS,
    is_keyword, get_keyword_type, is_operator_char, is_delimiter
)


class LexerError(Exception):
    """Exception raised for lexical analysis errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at {line}:{column} - {message}")


class Lexer:
    """
    Lexical Analyzer that tokenizes MinLang source code
    
    Attributes:
        source: The source code string to analyze
        position: Current position in source code
        line: Current line number (1-indexed)
        column: Current column number (1-indexed)
        current_char: Character at current position
    """
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code
        
        Args:
            source: MinLang source code as string
        """
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None
    
    def error(self, message: str) -> None:
        """
        Raise a lexer error with current position
        
        Args:
            message: Error message
        """
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
        Look ahead at the next character without consuming it
        
        Args:
            offset: Number of characters to look ahead (default: 1)
            
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
        """Skip single-line comments starting with //"""
        if self.current_char == '/' and self.peek() == '/':
            # Skip until end of line
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            # Skip the newline
            if self.current_char == '\n':
                self.advance()
    
    def skip_multiline_comment(self) -> None:
        """Skip multi-line comments /* ... */"""
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
            Token representing the number
        """
        start_line = self.line
        start_column = self.column
        num_str = ''
        is_float = False
        
        # Read digits and possibly a decimal point
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    self.error("Multiple decimal points in number")
                is_float = True
                num_str += self.current_char
                self.advance()
                
                # Must have digit after decimal point
                if self.current_char is None or not self.current_char.isdigit():
                    self.error("Expected digit after decimal point")
            else:
                num_str += self.current_char
                self.advance()
        
        # Create appropriate token
        if is_float:
            return Token(TokenType.FLOAT_LITERAL, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INTEGER_LITERAL, int(num_str), start_line, start_column)
    
    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword
        
        Returns:
            Token representing identifier or keyword
        """
        start_line = self.line
        start_column = self.column
        id_str = ''
        
        # Read alphanumeric characters and underscores
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            id_str += self.current_char
            self.advance()
        
        # Check if it's a keyword
        if is_keyword(id_str):
            token_type = get_keyword_type(id_str)
            # For boolean literals, store the actual boolean value
            if token_type == TokenType.TRUE:
                return Token(token_type, True, start_line, start_column)
            elif token_type == TokenType.FALSE:
                return Token(token_type, False, start_line, start_column)
            return Token(token_type, id_str, start_line, start_column)
        
        # It's an identifier
        return Token(TokenType.IDENTIFIER, id_str, start_line, start_column)
    
    def read_string(self) -> Token:
        """
        Read a string literal enclosed in double quotes
        
        Returns:
            Token representing the string
        """
        start_line = self.line
        start_column = self.column
        
        # Skip opening quote
        self.advance()
        
        string_value = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                # Handle escape sequences
                self.advance()
                if self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                elif self.current_char == '\\':
                    string_value += '\\'
                elif self.current_char == '"':
                    string_value += '"'
                else:
                    self.error(f"Invalid escape sequence: \\{self.current_char}")
                self.advance()
            elif self.current_char == '\n':
                self.error("Unterminated string literal")
            else:
                string_value += self.current_char
                self.advance()
        
        if self.current_char is None:
            self.error("Unterminated string literal")
        
        # Skip closing quote
        self.advance()
        
        return Token(TokenType.STRING_LITERAL, string_value, start_line, start_column)
    
    def read_char(self) -> Token:
        """
        Read a character literal enclosed in single quotes
        
        Returns:
            Token representing the character
        """
        start_line = self.line
        start_column = self.column
        
        # Skip opening quote
        self.advance()
        
        if self.current_char is None or self.current_char == '\'':
            self.error("Empty character literal")
        
        char_value = None
        if self.current_char == '\\':
            # Handle escape sequences
            self.advance()
            if self.current_char == 'n':
                char_value = '\n'
            elif self.current_char == 't':
                char_value = '\t'
            elif self.current_char == '\\':
                char_value = '\\'
            elif self.current_char == '\'':
                char_value = '\''
            else:
                self.error(f"Invalid escape sequence: \\{self.current_char}")
            self.advance()
        else:
            char_value = self.current_char
            self.advance()
        
        if self.current_char != '\'':
            self.error("Character literal must contain exactly one character")
        
        # Skip closing quote
        self.advance()
        
        return Token(TokenType.CHAR_LITERAL, char_value, start_line, start_column)
    
    def read_operator(self) -> Token:
        """
        Read an operator (single or double character)
        
        Returns:
            Token representing the operator
        """
        start_line = self.line
        start_column = self.column
        
        # Check for two-character operators
        if self.peek() is not None:
            two_char = self.current_char + self.peek()
            if two_char in OPERATORS:
                self.advance()
                self.advance()
                return Token(OPERATORS[two_char], two_char, start_line, start_column)
        
        # Single character operator
        op = self.current_char
        if op in OPERATORS:
            self.advance()
            return Token(OPERATORS[op], op, start_line, start_column)
        
        self.error(f"Unknown operator: {op}")
    
    def get_next_token(self) -> Token:
        """
        Get the next token from the source code
        
        Returns:
            The next Token in the source
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
            
            # String literals
            if self.current_char == '"':
                return self.read_string()
            
            # Character literals
            if self.current_char == '\'':
                return self.read_char()
            
            # Operators
            if is_operator_char(self.current_char):
                return self.read_operator()
            
            # Delimiters
            if is_delimiter(self.current_char):
                char = self.current_char
                line = self.line
                col = self.column
                self.advance()
                return Token(DELIMITERS[char], char, line, col)
            
            # Unknown character
            self.error(f"Unexpected character: '{self.current_char}'")
        
        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code
        
        Returns:
            List of all tokens in the source code
        """
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


def tokenize_file(filename: str) -> List[Token]:
    """
    Tokenize a MinLang source file
    
    Args:
        filename: Path to the source file
        
    Returns:
        List of tokens
    """
    with open(filename, 'r') as f:
        source = f.read()
    
    lexer = Lexer(source)
    return lexer.tokenize()


def tokenize_string(source: str) -> List[Token]:
    """
    Tokenize a MinLang source string
    
    Args:
        source: Source code string
        
    Returns:
        List of tokens
    """
    lexer = Lexer(source)
    return lexer.tokenize()
