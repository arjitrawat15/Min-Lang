"""
Semantic Analyzer for MinLang Compiler
Performs type checking, scope resolution, and semantic validation
"""

from typing import List, Optional, Any
from ..parser.ast_nodes import *
from .symbol_table import (
    SymbolTable, Symbol, SymbolKind, DataType, TypeChecker
)


class SemanticError(Exception):
    """Exception raised for semantic errors"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Semantic Error at {line}:{column} - {message}")


class SemanticAnalyzer:
    """
    Semantic analyzer that traverses the AST and performs:
    - Type checking
    - Scope resolution
    - Symbol table management
    - Semantic validation
    """
    
    def __init__(self):
        """Initialize the semantic analyzer"""
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_function_return_type: Optional[DataType] = None
        self.has_main = False
    
    def error(self, message: str, line: int = 0, column: int = 0):
        """
        Report a semantic error
        
        Args:
            message: Error message
            line: Line number
            column: Column number
        """
        error = SemanticError(message, line, column)
        self.errors.append(error)
    
    def analyze(self, ast: Program) -> bool:
        """
        Analyze the entire program
        
        Args:
            ast: Program AST node
            
        Returns:
            True if no errors, False otherwise
        """
        self.errors.clear()
        self.analyze_program(ast)
        
        # Check if main function exists
        if not self.has_main:
            self.error("Program must have a 'main' function", 0, 0)
        
        return len(self.errors) == 0
    
    def get_errors(self) -> List[SemanticError]:
        """Get list of semantic errors"""
        return self.errors
    
    def print_errors(self):
        """Print all semantic errors"""
        if not self.errors:
            print("✓ No semantic errors found")
            return
        
        print(f"\n✗ Found {len(self.errors)} semantic error(s):\n")
        for error in self.errors:
            print(f"  {error}")
        print()
    
    # AST Traversal Methods
    
    def analyze_program(self, node: Program):
        """Analyze program node"""
        for declaration in node.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self.analyze_function_declaration(declaration)
            elif isinstance(declaration, VariableDeclaration):
                self.analyze_variable_declaration(declaration, is_global=True)
    
    def analyze_function_declaration(self, node: FunctionDeclaration):
        """Analyze function declaration"""
        # Check if main function
        if node.identifier == "main":
            self.has_main = True
            # Main must return int
            if node.return_type != "int":
                self.error(
                    f"main function must return int, not {node.return_type}",
                    node.line, node.column
                )
        
        # Convert return type
        return_type = DataType.from_string(node.return_type)
        if return_type == DataType.ERROR:
            self.error(
                f"Invalid return type: {node.return_type}",
                node.line, node.column
            )
            return_type = DataType.VOID
        
        # Check if function already defined
        if self.symbol_table.lookup_local(node.identifier):
            self.error(
                f"Function '{node.identifier}' already defined",
                node.line, node.column
            )
            return
        
        # Process parameters
        param_types = []
        for param in node.parameters:
            param_type = DataType.from_string(param.param_type)
            if param_type == DataType.ERROR:
                self.error(
                    f"Invalid parameter type: {param.param_type}",
                    param.line, param.column
                )
                param_type = DataType.INT
            param_types.append(param_type)
        
        # Define function in symbol table
        self.symbol_table.define_symbol(
            name=node.identifier,
            kind=SymbolKind.FUNCTION,
            data_type=return_type,
            line=node.line,
            column=node.column,
            parameters=param_types,
            return_type=return_type
        )
        
        # Enter function scope
        self.symbol_table.enter_scope()
        self.current_function_return_type = return_type
        
        # Define parameters in function scope
        for param in node.parameters:
            param_type = DataType.from_string(param.param_type)
            if not self.symbol_table.define_symbol(
                name=param.identifier,
                kind=SymbolKind.PARAMETER,
                data_type=param_type,
                line=param.line,
                column=param.column
            ):
                self.error(
                    f"Parameter '{param.identifier}' already defined",
                    param.line, param.column
                )
            else:
                self.symbol_table.mark_initialized(param.identifier)
        
        # Analyze function body
        self.analyze_block(node.body)
        
        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_function_return_type = None
    
    def analyze_variable_declaration(self, node: VariableDeclaration, 
                                    is_global: bool = False):
        """Analyze variable declaration"""
        # Convert type
        var_type = DataType.from_string(node.var_type)
        if var_type == DataType.ERROR:
            self.error(
                f"Invalid variable type: {node.var_type}",
                node.line, node.column
            )
            var_type = DataType.INT
        
        # Check if variable already defined in current scope
        if self.symbol_table.lookup_local(node.identifier):
            self.error(
                f"Variable '{node.identifier}' already defined in this scope",
                node.line, node.column
            )
            return
        
        # Define variable
        kind = SymbolKind.CONSTANT if node.is_const else SymbolKind.VARIABLE
        self.symbol_table.define_symbol(
            name=node.identifier,
            kind=kind,
            data_type=var_type,
            line=node.line,
            column=node.column
        )
        
        # Check initializer if present
        if node.initializer:
            init_type = self.analyze_expression(node.initializer)
            
            # Check type compatibility
            if not TypeChecker.check_assignment(var_type, init_type):
                self.error(
                    f"Cannot assign {init_type.value} to {var_type.value}",
                    node.line, node.column
                )
            
            # Mark as initialized
            self.symbol_table.mark_initialized(node.identifier)
        elif node.is_const:
            self.error(
                f"Constant '{node.identifier}' must be initialized",
                node.line, node.column
            )
    
    def analyze_block(self, node: Block):
        """Analyze block statement"""
        # Enter new scope for block
        self.symbol_table.enter_scope()
        
        for statement in node.statements:
            self.analyze_statement(statement)
        
        # Exit block scope
        self.symbol_table.exit_scope()
    
    def analyze_statement(self, node: ASTNode):
        """Analyze a statement"""
        if isinstance(node, VariableDeclaration):
            self.analyze_variable_declaration(node)
        elif isinstance(node, ExpressionStatement):
            self.analyze_expression(node.expression)
        elif isinstance(node, IfStatement):
            self.analyze_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.analyze_while_statement(node)
        elif isinstance(node, ForStatement):
            self.analyze_for_statement(node)
        elif isinstance(node, ReturnStatement):
            self.analyze_return_statement(node)
        elif isinstance(node, Block):
            self.analyze_block(node)
        elif isinstance(node, ReadStatement):
            self.analyze_read_statement(node)
        elif isinstance(node, PrintStatement):
            self.analyze_print_statement(node)
    
    def analyze_if_statement(self, node: IfStatement):
        """Analyze if statement"""
        # Check condition
        cond_type = self.analyze_expression(node.condition)
        if cond_type != DataType.BOOL:
            self.error(
                f"If condition must be boolean, got {cond_type.value}",
                node.line, node.column
            )
        
        # Analyze branches
        self.analyze_statement(node.then_branch)
        if node.else_branch:
            self.analyze_statement(node.else_branch)
    
    def analyze_while_statement(self, node: WhileStatement):
        """Analyze while statement"""
        # Check condition
        cond_type = self.analyze_expression(node.condition)
        if cond_type != DataType.BOOL:
            self.error(
                f"While condition must be boolean, got {cond_type.value}",
                node.line, node.column
            )
        
        # Analyze body
        self.analyze_statement(node.body)
    
    def analyze_for_statement(self, node: ForStatement):
        """Analyze for statement"""
        # Analyze init
        if node.init:
            self.analyze_expression(node.init)
        
        # Check condition
        cond_type = self.analyze_expression(node.condition)
        if cond_type != DataType.BOOL:
            self.error(
                f"For condition must be boolean, got {cond_type.value}",
                node.line, node.column
            )
        
        # Analyze increment
        if node.increment:
            self.analyze_expression(node.increment)
        
        # Analyze body
        self.analyze_statement(node.body)
    
    def analyze_return_statement(self, node: ReturnStatement):
        """Analyze return statement"""
        if self.current_function_return_type is None:
            self.error(
                "Return statement outside of function",
                node.line, node.column
            )
            return
        
        if node.value:
            value_type = self.analyze_expression(node.value)
            
            # Check return type matches function
            if not TypeChecker.check_assignment(
                self.current_function_return_type, value_type
            ):
                self.error(
                    f"Return type {value_type.value} does not match "
                    f"function return type {self.current_function_return_type.value}",
                    node.line, node.column
                )
        else:
            # Void return
            if self.current_function_return_type != DataType.VOID:
                self.error(
                    f"Function must return {self.current_function_return_type.value}",
                    node.line, node.column
                )
    
    def analyze_read_statement(self, node: ReadStatement):
        """Analyze read statement"""
        symbol = self.symbol_table.lookup_symbol(node.identifier)
        
        if not symbol:
            self.error(
                f"Undefined variable: {node.identifier}",
                node.line, node.column
            )
            return
        
        if symbol.kind not in [SymbolKind.VARIABLE, SymbolKind.PARAMETER]:
            self.error(
                f"Cannot read into {symbol.kind.value}",
                node.line, node.column
            )
        
        # Mark as initialized after read
        self.symbol_table.mark_initialized(node.identifier)
    
    def analyze_print_statement(self, node: PrintStatement):
        """Analyze print statement"""
        self.analyze_expression(node.expression)
    
    def analyze_expression(self, node: ASTNode) -> DataType:
        """
        Analyze an expression and return its type
        
        Args:
            node: Expression AST node
            
        Returns:
            DataType of the expression
        """
        if isinstance(node, Literal):
            return self.analyze_literal(node)
        elif isinstance(node, Identifier):
            return self.analyze_identifier(node)
        elif isinstance(node, BinaryExpression):
            return self.analyze_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self.analyze_unary_expression(node)
        elif isinstance(node, AssignmentExpression):
            return self.analyze_assignment_expression(node)
        elif isinstance(node, CallExpression):
            return self.analyze_call_expression(node)
        else:
            self.error(f"Unknown expression type: {type(node)}", 0, 0)
            return DataType.ERROR
    
    def analyze_literal(self, node: Literal) -> DataType:
        """Analyze literal value"""
        return TypeChecker.get_literal_type(node.literal_type)
    
    def analyze_identifier(self, node: Identifier) -> DataType:
        """Analyze identifier"""
        symbol = self.symbol_table.lookup_symbol(node.name)
        
        if not symbol:
            self.error(
                f"Undefined variable: {node.name}",
                node.line, node.column
            )
            return DataType.ERROR
        
        # Check if variable is initialized
        if symbol.kind == SymbolKind.VARIABLE and not symbol.is_initialized:
            self.error(
                f"Variable '{node.name}' used before initialization",
                node.line, node.column
            )
        
        return symbol.data_type
    
    def analyze_binary_expression(self, node: BinaryExpression) -> DataType:
        """Analyze binary expression"""
        left_type = self.analyze_expression(node.left)
        right_type = self.analyze_expression(node.right)
        
        result_type = TypeChecker.check_binary_operation(
            node.operator, left_type, right_type
        )
        
        if result_type is None:
            self.error(
                f"Invalid operands for '{node.operator}': "
                f"{left_type.value} and {right_type.value}",
                node.line, node.column
            )
            return DataType.ERROR
        
        return result_type
    
    def analyze_unary_expression(self, node: UnaryExpression) -> DataType:
        """Analyze unary expression"""
        operand_type = self.analyze_expression(node.operand)
        
        result_type = TypeChecker.check_unary_operation(
            node.operator, operand_type
        )
        
        if result_type is None:
            self.error(
                f"Invalid operand for '{node.operator}': {operand_type.value}",
                node.line, node.column
            )
            return DataType.ERROR
        
        return result_type
    
    def analyze_assignment_expression(self, node: AssignmentExpression) -> DataType:
        """Analyze assignment expression"""
        # Look up variable
        symbol = self.symbol_table.lookup_symbol(node.identifier)
        
        if not symbol:
            self.error(
                f"Undefined variable: {node.identifier}",
                node.line, node.column
            )
            return DataType.ERROR
        
        # Check if constant
        if symbol.kind == SymbolKind.CONSTANT:
            self.error(
                f"Cannot assign to constant '{node.identifier}'",
                node.line, node.column
            )
            return symbol.data_type
        
        # Check if function
        if symbol.kind == SymbolKind.FUNCTION:
            self.error(
                f"Cannot assign to function '{node.identifier}'",
                node.line, node.column
            )
            return DataType.ERROR
        
        # Analyze value
        value_type = self.analyze_expression(node.value)
        
        # Check type compatibility
        if not TypeChecker.check_assignment(symbol.data_type, value_type):
            self.error(
                f"Cannot assign {value_type.value} to {symbol.data_type.value}",
                node.line, node.column
            )
        
        # Mark as initialized
        self.symbol_table.mark_initialized(node.identifier)
        
        return symbol.data_type
    
    def analyze_call_expression(self, node: CallExpression) -> DataType:
        """Analyze function call"""
        # Look up function
        symbol = self.symbol_table.lookup_symbol(node.identifier)
        
        if not symbol:
            self.error(
                f"Undefined function: {node.identifier}",
                node.line, node.column
            )
            return DataType.ERROR
        
        if symbol.kind != SymbolKind.FUNCTION:
            self.error(
                f"'{node.identifier}' is not a function",
                node.line, node.column
            )
            return DataType.ERROR
        
        # Special handling for built-in functions
        if node.identifier in ['read', 'print']:
            # These have flexible signatures
            for arg in node.arguments:
                self.analyze_expression(arg)
            return DataType.VOID
        
        # Analyze arguments
        arg_types = []
        for arg in node.arguments:
            arg_type = self.analyze_expression(arg)
            arg_types.append(arg_type)
        
        # Check argument count and types
        if not TypeChecker.check_function_call(symbol.parameters, arg_types):
            expected = ', '.join(p.value for p in symbol.parameters)
            got = ', '.join(a.value for a in arg_types)
            self.error(
                f"Function '{node.identifier}' expects ({expected}), got ({got})",
                node.line, node.column
            )
        
        return symbol.return_type


def analyze_program(ast: Program) -> tuple[bool, SymbolTable, List[SemanticError]]:
    """
    Convenience function to analyze a program
    
    Args:
        ast: Program AST node
        
    Returns:
        Tuple of (success, symbol_table, errors)
    """
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    return success, analyzer.symbol_table, analyzer.get_errors()
