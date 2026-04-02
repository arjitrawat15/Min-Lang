"""
IR Generator for MinLang Compiler
Generates Three-Address Code (TAC) from AST
"""

from typing import Optional, List
from ..parser.ast_nodes import *
from ..semantic import DataType, SymbolTable
from .intermediate import (
    TACProgram, TACOpcode, TACInstruction
)


class IRGeneratorError(Exception):
    """Exception raised during IR generation"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"IR Generation Error at {line}:{column} - {message}")


class IRGenerator:
    """
    Generates Three-Address Code from AST
    
    Attributes:
        program: TAC program being generated
        symbol_table: Symbol table from semantic analysis
        current_function: Name of current function being processed
    """
    
    def __init__(self, symbol_table: SymbolTable):
        """
        Initialize IR generator
        
        Args:
            symbol_table: Symbol table from semantic analysis
        """
        self.program = TACProgram()
        self.symbol_table = symbol_table
        self.current_function: Optional[str] = None
        self.errors: List[IRGeneratorError] = []
    
    def error(self, message: str, line: int = 0, column: int = 0):
        """Report an IR generation error"""
        error = IRGeneratorError(message, line, column)
        self.errors.append(error)
    
    def generate(self, ast: Program) -> TACProgram:
        """
        Generate TAC from AST
        
        Args:
            ast: Program AST node
            
        Returns:
            Generated TAC program
        """
        self.errors.clear()
        
        # Generate code for all declarations
        for declaration in ast.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self.gen_function(declaration)
            elif isinstance(declaration, VariableDeclaration):
                self.gen_global_var(declaration)
        
        return self.program
    
    def gen_global_var(self, node: VariableDeclaration):
        """
        Generate code for global variable declaration
        
        Args:
            node: Variable declaration node
        """
        # Global variables are handled by the runtime
        # If there's an initializer, generate assignment
        if node.initializer:
            value = self.gen_expression(node.initializer)
            self.program.emit_assign(node.identifier, value)
    
    def gen_function(self, node: FunctionDeclaration):
        """
        Generate code for function declaration
        
        Args:
            node: Function declaration node
        """
        self.current_function = node.identifier
        
        # Emit function begin
        self.program.emit_begin_func(node.identifier)
        
        # Parameters are already in symbol table
        # They are accessed by name directly
        
        # Generate function body
        self.gen_statement(node.body)
        
        # Emit implicit return for void functions
        if node.return_type == "void":
            self.program.emit_return()
        
        # Emit function end
        self.program.emit_end_func(node.identifier)
        
        self.current_function = None
    
    def gen_statement(self, node: ASTNode):
        """
        Generate code for a statement
        
        Args:
            node: Statement AST node
        """
        if isinstance(node, Block):
            self.gen_block(node)
        elif isinstance(node, VariableDeclaration):
            self.gen_var_declaration(node)
        elif isinstance(node, ExpressionStatement):
            self.gen_expression(node.expression)
        elif isinstance(node, IfStatement):
            self.gen_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.gen_while_statement(node)
        elif isinstance(node, ForStatement):
            self.gen_for_statement(node)
        elif isinstance(node, ReturnStatement):
            self.gen_return_statement(node)
        elif isinstance(node, ReadStatement):
            self.gen_read_statement(node)
        elif isinstance(node, PrintStatement):
            self.gen_print_statement(node)
    
    def gen_block(self, node: Block):
        """
        Generate code for block statement
        
        Args:
            node: Block node
        """
        for statement in node.statements:
            self.gen_statement(statement)
    
    def gen_var_declaration(self, node: VariableDeclaration):
        """
        Generate code for local variable declaration
        
        Args:
            node: Variable declaration node
        """
        # If there's an initializer, generate assignment
        if node.initializer:
            value = self.gen_expression(node.initializer)
            self.program.emit_assign(node.identifier, value)
    
    def gen_if_statement(self, node: IfStatement):
        """
        Generate code for if statement
        
        Args:
            node: If statement node
        """
        # Generate condition
        condition = self.gen_expression(node.condition)
        
        # Create labels
        else_label = self.program.new_label("else")
        end_label = self.program.new_label("endif")
        
        if node.else_branch:
            # if-else statement
            # iffalse condition goto else_label
            self.program.emit_if_false(condition, else_label)
            
            # then branch
            self.gen_statement(node.then_branch)
            self.program.emit_goto(end_label)
            
            # else branch
            self.program.emit_label(else_label)
            self.gen_statement(node.else_branch)
            
            # end label
            self.program.emit_label(end_label)
        else:
            # if statement without else
            # iffalse condition goto end_label
            self.program.emit_if_false(condition, end_label)
            
            # then branch
            self.gen_statement(node.then_branch)
            
            # end label
            self.program.emit_label(end_label)
    
    def gen_while_statement(self, node: WhileStatement):
        """
        Generate code for while loop
        
        Args:
            node: While statement node
        """
        # Create labels
        start_label = self.program.new_label("while_start")
        end_label = self.program.new_label("while_end")
        
        # start_label:
        self.program.emit_label(start_label)
        
        # Generate condition
        condition = self.gen_expression(node.condition)
        
        # iffalse condition goto end_label
        self.program.emit_if_false(condition, end_label)
        
        # Loop body
        self.gen_statement(node.body)
        
        # goto start_label
        self.program.emit_goto(start_label)
        
        # end_label:
        self.program.emit_label(end_label)
    
    def gen_for_statement(self, node: ForStatement):
        """
        Generate code for for loop
        
        Args:
            node: For statement node
        """
        # Generate initialization
        if node.init:
            self.gen_expression(node.init)
        
        # Create labels
        start_label = self.program.new_label("for_start")
        end_label = self.program.new_label("for_end")
        
        # start_label:
        self.program.emit_label(start_label)
        
        # Generate condition
        condition = self.gen_expression(node.condition)
        
        # iffalse condition goto end_label
        self.program.emit_if_false(condition, end_label)
        
        # Loop body
        self.gen_statement(node.body)
        
        # Generate increment
        if node.increment:
            self.gen_expression(node.increment)
        
        # goto start_label
        self.program.emit_goto(start_label)
        
        # end_label:
        self.program.emit_label(end_label)
    
    def gen_return_statement(self, node: ReturnStatement):
        """
        Generate code for return statement
        
        Args:
            node: Return statement node
        """
        if node.value:
            value = self.gen_expression(node.value)
            self.program.emit_return(value)
        else:
            self.program.emit_return()
    
    def gen_read_statement(self, node: ReadStatement):
        """
        Generate code for read statement
        
        Args:
            node: Read statement node
        """
        self.program.emit_read(node.identifier)
    
    def gen_print_statement(self, node: PrintStatement):
        """
        Generate code for print statement
        
        Args:
            node: Print statement node
        """
        value = self.gen_expression(node.expression)
        self.program.emit_print(value)
    
    def gen_expression(self, node: ASTNode) -> str:
        """
        Generate code for expression and return result variable
        
        Args:
            node: Expression AST node
            
        Returns:
            Variable or temporary holding the result
        """
        if isinstance(node, Literal):
            return self.gen_literal(node)
        elif isinstance(node, Identifier):
            return self.gen_identifier(node)
        elif isinstance(node, BinaryExpression):
            return self.gen_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self.gen_unary_expression(node)
        elif isinstance(node, AssignmentExpression):
            return self.gen_assignment_expression(node)
        elif isinstance(node, CallExpression):
            return self.gen_call_expression(node)
        else:
            self.error(f"Unknown expression type: {type(node)}", 0, 0)
            return self.program.new_temp()
    
    def gen_literal(self, node: Literal) -> str:
        """
        Generate code for literal value
        
        Args:
            node: Literal node
            
        Returns:
            String representation of literal value
        """
        # Return literal value as string
        value = node.value
        
        if isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, str):
            # String literal - return as quoted string
            return f'"{value}"'
        else:
            return str(value)
    
    def gen_identifier(self, node: Identifier) -> str:
        """
        Generate code for identifier
        
        Args:
            node: Identifier node
            
        Returns:
            Variable name
        """
        return node.name
    
    def gen_binary_expression(self, node: BinaryExpression) -> str:
        """
        Generate code for binary expression
        
        Args:
            node: Binary expression node
            
        Returns:
            Temporary variable holding result
        """
        # Generate code for operands
        left = self.gen_expression(node.left)
        right = self.gen_expression(node.right)
        
        # Create temporary for result
        result = self.program.new_temp()
        
        # Map operator to TAC opcode
        op_map = {
            '+': TACOpcode.ADD,
            '-': TACOpcode.SUB,
            '*': TACOpcode.MUL,
            '/': TACOpcode.DIV,
            '%': TACOpcode.MOD,
            '<': TACOpcode.LT,
            '>': TACOpcode.GT,
            '<=': TACOpcode.LE,
            '>=': TACOpcode.GE,
            '==': TACOpcode.EQ,
            '!=': TACOpcode.NE,
            '&&': TACOpcode.AND,
            '||': TACOpcode.OR,
        }
        
        opcode = op_map.get(node.operator)
        if opcode:
            self.program.emit_binary_op(opcode, result, left, right)
        else:
            self.error(f"Unknown operator: {node.operator}", node.line, node.column)
        
        return result
    
    def gen_unary_expression(self, node: UnaryExpression) -> str:
        """
        Generate code for unary expression
        
        Args:
            node: Unary expression node
            
        Returns:
            Temporary variable holding result
        """
        # Generate code for operand
        operand = self.gen_expression(node.operand)
        
        # Create temporary for result
        result = self.program.new_temp()
        
        # Map operator to TAC opcode
        op_map = {
            '-': TACOpcode.NEG,
            '!': TACOpcode.NOT,
        }
        
        opcode = op_map.get(node.operator)
        if opcode:
            self.program.emit_unary_op(opcode, result, operand)
        else:
            self.error(f"Unknown operator: {node.operator}", node.line, node.column)
        
        return result
    
    def gen_assignment_expression(self, node: AssignmentExpression) -> str:
        """
        Generate code for assignment expression
        
        Args:
            node: Assignment expression node
            
        Returns:
            Variable being assigned to
        """
        # Generate code for value
        value = self.gen_expression(node.value)
        
        # Generate assignment
        self.program.emit_assign(node.identifier, value)
        
        return node.identifier
    
    def gen_call_expression(self, node: CallExpression) -> str:
        """
        Generate code for function call
        
        Args:
            node: Call expression node
            
        Returns:
            Temporary variable holding result (or empty for void)
        """
        # Special handling for built-in functions
        if node.identifier == "read":
            # read is handled as a statement
            if node.arguments:
                arg = self.gen_expression(node.arguments[0])
                self.program.emit_read(arg)
            return ""
        
        elif node.identifier == "print":
            # print is handled as a statement
            if node.arguments:
                arg = self.gen_expression(node.arguments[0])
                self.program.emit_print(arg)
            return ""
        
        # Regular function call
        # Generate code for arguments (in reverse order for stack-based calling)
        for arg in reversed(node.arguments):
            arg_value = self.gen_expression(arg)
            self.program.emit_param(arg_value)
        
        # Look up function in symbol table to check return type
        symbol = self.symbol_table.lookup_symbol(node.identifier)
        
        # Generate call
        if symbol and symbol.return_type != DataType.VOID:
            result = self.program.new_temp()
            self.program.emit_call(node.identifier, len(node.arguments), result)
            return result
        else:
            self.program.emit_call(node.identifier, len(node.arguments))
            return ""


def generate_tac(ast: Program, symbol_table: SymbolTable) -> TACProgram:
    """
    Convenience function to generate TAC from AST
    
    Args:
        ast: Program AST
        symbol_table: Symbol table from semantic analysis
        
    Returns:
        Generated TAC program
    """
    generator = IRGenerator(symbol_table)
    return generator.generate(ast)
