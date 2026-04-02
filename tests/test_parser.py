"""
Unit tests for the Parser
Tests AST generation for MinLang constructs
"""

import pytest
from src.lexer import tokenize
from src.parser import parse, ParserError
from src.parser.ast_nodes import *


class TestBasicParsing:
    """Test basic parsing functionality"""
    
    def test_empty_program(self):
        """Test parsing an empty program"""
        source = ""
        tokens = tokenize(source)
        ast = parse(tokens)
        
        assert isinstance(ast, Program)
        assert len(ast.declarations) == 0
        assert len(ast.functions) == 0
    
    def test_variable_declaration(self):
        """Test parsing variable declarations"""
        source = "int x;"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        assert isinstance(ast, Program)
        assert len(ast.declarations) == 1
        assert isinstance(ast.declarations[0], VariableDeclaration)
        assert ast.declarations[0].type_name == "int"
        assert ast.declarations[0].identifier == "x"
    
    def test_variable_with_initializer(self):
        """Test parsing variable with initializer"""
        source = "int x = 10;"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        decl = ast.declarations[0]
        assert isinstance(decl, VariableDeclaration)
        assert decl.initializer is not None
        assert isinstance(decl.initializer, IntegerLiteral)
        assert decl.initializer.value == 10
    
    def test_const_declaration(self):
        """Test parsing const declarations"""
        source = "const int MAX = 100;"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        decl = ast.declarations[0]
        assert decl.is_const == True
        assert decl.type_name == "int"
        assert decl.identifier == "MAX"


class TestFunctions:
    """Test function parsing"""
    
    def test_empty_function(self):
        """Test parsing function with empty body"""
        source = "void test() { }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        assert len(ast.functions) == 1
        func = ast.functions[0]
        assert isinstance(func, FunctionDeclaration)
        assert func.return_type == "void"
        assert func.name == "test"
        assert len(func.parameters) == 0
        assert isinstance(func.body, Block)
    
    def test_function_with_parameters(self):
        """Test parsing function with parameters"""
        source = "int add(int a, int b) { return a + b; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        assert func.return_type == "int"
        assert func.name == "add"
        assert len(func.parameters) == 2
        assert func.parameters[0].type_name == "int"
        assert func.parameters[0].identifier == "a"
        assert func.parameters[1].type_name == "int"
        assert func.parameters[1].identifier == "b"
    
    def test_main_function(self):
        """Test parsing main function"""
        source = """
        int main() {
            int x;
            x = 5;
            return 0;
        }
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        assert func.name == "main"
        assert func.return_type == "int"
        assert len(func.body.statements) == 3


class TestStatements:
    """Test statement parsing"""
    
    def test_assignment_statement(self):
        """Test parsing assignment statements"""
        source = """
        int main() {
            int x;
            x = 10;
        }
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        stmt = func.body.statements[1]  # Second statement (first is declaration)
        assert isinstance(stmt, AssignmentStatement)
        assert stmt.identifier == "x"
        assert isinstance(stmt.expression, IntegerLiteral)
    
    def test_print_statement(self):
        """Test parsing print statements"""
        source = """
        int main() {
            print(42);
        }
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        stmt = func.body.statements[0]
        assert isinstance(stmt, PrintStatement)
        assert isinstance(stmt.expression, IntegerLiteral)
        assert stmt.expression.value == 42
    
    def test_return_statement(self):
        """Test parsing return statements"""
        source = """
        int test() {
            return 0;
        }
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        stmt = func.body.statements[0]
        assert isinstance(stmt, ReturnStatement)
        assert isinstance(stmt.expression, IntegerLiteral)
    
    def test_read_statement(self):
        """Test parsing read statements"""
        source = """
        int main() {
            int x;
            read(x);
        }
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        stmt = func.body.statements[1]
        assert isinstance(stmt, ReadStatement)
        assert stmt.identifier == "x"


class TestExpressions:
    """Test expression parsing"""
    
    def test_integer_literal(self):
        """Test parsing integer literals"""
        source = "int main() { int x; x = 42; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        assign_stmt = func.body.statements[1]
        assert isinstance(assign_stmt.expression, IntegerLiteral)
        assert assign_stmt.expression.value == 42
    
    def test_binary_expression(self):
        """Test parsing binary expressions"""
        source = "int main() { int x; x = 5 + 3; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        assign_stmt = func.body.statements[1]
        assert isinstance(assign_stmt.expression, BinaryExpression)
        assert assign_stmt.expression.operator == "+"
        assert isinstance(assign_stmt.expression.left, IntegerLiteral)
        assert assign_stmt.expression.left.value == 5
        assert isinstance(assign_stmt.expression.right, IntegerLiteral)
        assert assign_stmt.expression.right.value == 3
    
    def test_complex_expression(self):
        """Test parsing complex expressions"""
        source = "int main() { int x; x = 2 + 3 * 4; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        # Should parse with correct precedence: 2 + (3 * 4)
        func = ast.functions[0]
        assign_stmt = func.body.statements[1]
        expr = assign_stmt.expression
        
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "+"
        assert isinstance(expr.right, BinaryExpression)
        assert expr.right.operator == "*"
    
    def test_parenthesized_expression(self):
        """Test parsing parenthesized expressions"""
        source = "int main() { int x; x = (2 + 3) * 4; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        # Should parse as: (2 + 3) * 4
        func = ast.functions[0]
        assign_stmt = func.body.statements[1]
        expr = assign_stmt.expression
        
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "*"
        assert isinstance(expr.left, BinaryExpression)
        assert expr.left.operator == "+"
    
    def test_unary_expression(self):
        """Test parsing unary expressions"""
        source = "int main() { int x; x = -5; }"
        tokens = tokenize(source)
        ast = parse(tokens)
        
        func = ast.functions[0]
        assign_stmt = func.body.statements[1]
        expr = assign_stmt.expression
        
        assert isinstance(expr, UnaryExpression)
        assert expr.operator == "-"
        assert isinstance(expr.operand, IntegerLiteral)
        assert expr.operand.value == 5


class TestErrors:
    """Test error detection"""
    
    def test_missing_semicolon(self):
        """Test missing semicolon error"""
        source = "int x"
        tokens = tokenize(source)
        
        with pytest.raises(ParserError) as excinfo:
            parse(tokens)
        assert "semicolon" in str(excinfo.value).lower() or "';'" in str(excinfo.value)
    
    def test_unexpected_token(self):
        """Test unexpected token error"""
        source = "int main() { if }"
        tokens = tokenize(source)
        
        with pytest.raises(ParserError):
            parse(tokens)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
