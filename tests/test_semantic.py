"""Unit tests for semantic analysis."""

import pytest

from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer, SemanticError


def parse_source(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_semantic_valid_program_passes():
    source = """
    int add(int a, int b) {
        return a + b;
    }

    int main() {
        int x;
        x = add(2, 3);
        print(x);
        return 0;
    }
    """
    ast = parse_source(source)
    analyzer = SemanticAnalyzer()

    analyzer.analyze(ast)


def test_semantic_undeclared_identifier_fails():
    source = """
    int main() {
        x = 1;
        return 0;
    }
    """
    ast = parse_source(source)

    with pytest.raises(SemanticError):
        SemanticAnalyzer().analyze(ast)


def test_semantic_type_mismatch_fails():
    source = """
    int main() {
        int x;
        x = true;
        return 0;
    }
    """
    ast = parse_source(source)

    with pytest.raises(SemanticError):
        SemanticAnalyzer().analyze(ast)


def test_semantic_function_argument_count_fails():
    source = """
    int add(int a, int b) {
        return a + b;
    }

    int main() {
        int x;
        x = add(1);
        return 0;
    }
    """
    ast = parse_source(source)

    with pytest.raises(SemanticError):
        SemanticAnalyzer().analyze(ast)


def test_semantic_const_assignment_fails():
    source = """
    int main() {
        const int x = 1;
        x = 2;
        return 0;
    }
    """
    ast = parse_source(source)

    with pytest.raises(SemanticError):
        SemanticAnalyzer().analyze(ast)
