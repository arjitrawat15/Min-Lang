"""Unit tests for the Lexer"""

import pytest
from src.lexer import Lexer, TokenType, LexerError


def test_keywords():
    """Test keyword recognition"""
    source = "int float bool char void if else while for return"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected_types = [
        TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR,
        TokenType.VOID, TokenType.IF, TokenType.ELSE, TokenType.WHILE,
        TokenType.FOR, TokenType.RETURN, TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types)
    for token, expected in zip(tokens, expected_types):
        assert token.type == expected


def test_identifiers():
    """Test identifier recognition"""
    source = "x y_var count123 _private"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'x'
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == 'y_var'


def test_numbers():
    """Test number literal recognition"""
    source = "42 3.14 0 99.99"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.INTEGER_LITERAL
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.FLOAT_LITERAL
    assert tokens[1].value == 3.14


def test_operators():
    """Test operator recognition"""
    source = "+ - * / == != < > <= >= && ||"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected_types = [
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
        TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN,
        TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
        TokenType.AND, TokenType.OR, TokenType.EOF
    ]
    
    for token, expected in zip(tokens, expected_types):
        assert token.type == expected


def test_strings():
    """Test string literal recognition"""
    source = '"Hello, World!" "Test\\nString"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.STRING_LITERAL
    assert tokens[0].value == "Hello, World!"
    assert tokens[1].type == TokenType.STRING_LITERAL
    assert tokens[1].value == "Test\nString"


def test_comments():
    """Test comment handling"""
    source = """
    int x; // This is a comment
    /* Multi-line
       comment */
    int y;
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Should only have tokens for "int x;" and "int y;"
    token_types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert TokenType.INT in token_types
    assert TokenType.IDENTIFIER in token_types


def test_error_invalid_character():
    """Test lexer error on invalid character"""
    source = "int x @ y;"
    lexer = Lexer(source)
    
    with pytest.raises(LexerError):
        lexer.tokenize()


def test_simple_program():
    """Test lexing a simple program"""
    source = """
    int main() {
        int x;
        x = 5;
        return x;
    }
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Check for key tokens
    token_types = [t.type for t in tokens]
    assert TokenType.INT in token_types
    assert TokenType.IDENTIFIER in token_types
    assert TokenType.ASSIGN in token_types
    assert TokenType.RETURN in token_types


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
