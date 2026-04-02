"""
Unit tests for Semantic Analyzer
Tests type checking, symbol table, and semantic validation
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer, DataType, SymbolKind


def compile_source(source: str):
    """Helper to compile source code and return analyzer"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    return analyzer, success


class TestBasicSemantics:
    """Test basic semantic analysis"""
    
    def test_simple_program(self):
        """Test a simple valid program"""
        source = """
        int main() {
            int x;
            x = 5;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
        assert len(analyzer.errors) == 0
    
    def test_missing_main(self):
        """Test error when main function is missing"""
        source = """
        int foo() {
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("main" in str(e) for e in analyzer.errors)
    
    def test_main_wrong_return_type(self):
        """Test error when main has wrong return type"""
        source = """
        void main() {
            return;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("main" in str(e) and "int" in str(e) for e in analyzer.errors)


class TestVariableDeclarations:
    """Test variable declaration semantics"""
    
    def test_valid_variable_declaration(self):
        """Test valid variable declarations"""
        source = """
        int main() {
            int x;
            float y;
            bool flag;
            char c;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_duplicate_variable(self):
        """Test error on duplicate variable declaration"""
        source = """
        int main() {
            int x;
            int x;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("already defined" in str(e) for e in analyzer.errors)
    
    def test_variable_initialization(self):
        """Test variable initialization"""
        source = """
        int main() {
            int x = 10;
            float y = 3.14;
            bool flag = true;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_type_mismatch_initialization(self):
        """Test error on type mismatch in initialization"""
        source = """
        int main() {
            int x = true;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("assign" in str(e).lower() for e in analyzer.errors)
    
    def test_constant_declaration(self):
        """Test constant declaration"""
        source = """
        const int MAX = 100;
        
        int main() {
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_uninitialized_constant(self):
        """Test error on uninitialized constant"""
        source = """
        int main() {
            const int MAX;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("must be initialized" in str(e) for e in analyzer.errors)


class TestTypeChecking:
    """Test type checking"""
    
    def test_arithmetic_operations(self):
        """Test arithmetic type checking"""
        source = """
        int main() {
            int a = 5;
            int b = 3;
            int c = a + b;
            int d = a - b;
            int e = a * b;
            int f = a / b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_float_arithmetic(self):
        """Test float arithmetic"""
        source = """
        int main() {
            float a = 5.5;
            float b = 2.2;
            float c = a + b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_mixed_numeric_types(self):
        """Test mixed int/float operations"""
        source = """
        int main() {
            int a = 5;
            float b = 2.5;
            float c = a + b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_invalid_arithmetic(self):
        """Test error on invalid arithmetic"""
        source = """
        int main() {
            bool a = true;
            int b = 5;
            int c = a + b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
    
    def test_comparison_operations(self):
        """Test comparison operations"""
        source = """
        int main() {
            int a = 5;
            int b = 3;
            bool c = a < b;
            bool d = a > b;
            bool e = a <= b;
            bool f = a >= b;
            bool g = a == b;
            bool h = a != b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_logical_operations(self):
        """Test logical operations"""
        source = """
        int main() {
            bool a = true;
            bool b = false;
            bool c = a && b;
            bool d = a || b;
            bool e = !a;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_invalid_logical_operation(self):
        """Test error on invalid logical operation"""
        source = """
        int main() {
            int a = 5;
            int b = 3;
            bool c = a && b;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False


class TestControlFlow:
    """Test control flow statements"""
    
    def test_if_statement(self):
        """Test if statement"""
        source = """
        int main() {
            int x = 5;
            if (x > 0) {
                x = x + 1;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_if_non_boolean_condition(self):
        """Test error on non-boolean if condition"""
        source = """
        int main() {
            int x = 5;
            if (x) {
                x = x + 1;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("boolean" in str(e).lower() for e in analyzer.errors)
    
    def test_while_loop(self):
        """Test while loop"""
        source = """
        int main() {
            int i = 0;
            while (i < 10) {
                i = i + 1;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_for_loop(self):
        """Test for loop"""
        source = """
        int main() {
            int i;
            for (i = 0; i < 10; i = i + 1) {
                int x = i;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True


class TestFunctions:
    """Test function semantics"""
    
    def test_function_declaration(self):
        """Test function declaration"""
        source = """
        int add(int a, int b) {
            return a + b;
        }
        
        int main() {
            int result = add(5, 3);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_function_duplicate_declaration(self):
        """Test error on duplicate function"""
        source = """
        int foo() {
            return 0;
        }
        
        int foo() {
            return 1;
        }
        
        int main() {
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("already defined" in str(e) for e in analyzer.errors)
    
    def test_function_call(self):
        """Test function call"""
        source = """
        int square(int x) {
            return x * x;
        }
        
        int main() {
            int result = square(5);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_undefined_function(self):
        """Test error on undefined function call"""
        source = """
        int main() {
            int result = foo(5);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("Undefined function" in str(e) for e in analyzer.errors)
    
    def test_return_type_mismatch(self):
        """Test error on return type mismatch"""
        source = """
        int foo() {
            return true;
        }
        
        int main() {
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("Return type" in str(e) for e in analyzer.errors)
    
    def test_void_function(self):
        """Test void function"""
        source = """
        void printNum(int x) {
            print(x);
        }
        
        int main() {
            printNum(5);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True


class TestScoping:
    """Test scope management"""
    
    def test_nested_scopes(self):
        """Test nested scopes"""
        source = """
        int main() {
            int x = 5;
            {
                int y = 10;
                x = y;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_variable_shadowing(self):
        """Test variable shadowing in nested scope"""
        source = """
        int main() {
            int x = 5;
            {
                int x = 10;
            }
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_function_parameter_scope(self):
        """Test function parameters are in function scope"""
        source = """
        int add(int a, int b) {
            int sum = a + b;
            return sum;
        }
        
        int main() {
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True


class TestUnusedVariables:
    """Test uninitialized variable detection"""
    
    def test_use_before_initialization(self):
        """Test error on using variable before initialization"""
        source = """
        int main() {
            int x;
            int y = x + 5;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == False
        assert any("before initialization" in str(e) for e in analyzer.errors)
    
    def test_assignment_marks_initialized(self):
        """Test that assignment marks variable as initialized"""
        source = """
        int main() {
            int x;
            x = 5;
            int y = x + 3;
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True


class TestBuiltInFunctions:
    """Test built-in functions"""
    
    def test_print_function(self):
        """Test print function"""
        source = """
        int main() {
            int x = 5;
            print(x);
            print("Hello");
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
    
    def test_read_function(self):
        """Test read function"""
        source = """
        int main() {
            int x;
            read(x);
            print(x);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True


class TestComplexPrograms:
    """Test complex programs"""
    
    def test_factorial_program(self):
        """Test factorial program"""
        source = """
        int factorial(int n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        
        int main() {
            int num;
            read(num);
            int result = factorial(num);
            print(result);
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
        assert len(analyzer.errors) == 0
    
    def test_fibonacci_program(self):
        """Test Fibonacci program"""
        source = """
        int main() {
            int n;
            int a;
            int b;
            int temp;
            int i;
            
            a = 0;
            b = 1;
            
            read(n);
            
            for (i = 0; i < n; i = i + 1) {
                print(a);
                temp = a + b;
                a = b;
                b = temp;
            }
            
            return 0;
        }
        """
        analyzer, success = compile_source(source)
        assert success == True
        assert len(analyzer.errors) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
