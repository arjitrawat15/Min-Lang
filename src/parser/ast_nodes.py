"""
Abstract Syntax Tree (AST) node definitions for MinLang
Represents the hierarchical structure of the program
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from enum import Enum


class NodeType(Enum):
    """Types of AST nodes"""
    PROGRAM = "Program"
    FUNCTION_DECL = "FunctionDeclaration"
    VAR_DECL = "VariableDeclaration"
    PARAM_DECL = "ParameterDeclaration"
    BLOCK = "Block"
    IF_STMT = "IfStatement"
    WHILE_STMT = "WhileStatement"
    FOR_STMT = "ForStatement"
    RETURN_STMT = "ReturnStatement"
    EXPR_STMT = "ExpressionStatement"
    ASSIGN_EXPR = "AssignmentExpression"
    BINARY_EXPR = "BinaryExpression"
    UNARY_EXPR = "UnaryExpression"
    CALL_EXPR = "CallExpression"
    IDENTIFIER = "Identifier"
    LITERAL = "Literal"
    READ_STMT = "ReadStatement"
    PRINT_STMT = "PrintStatement"


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    node_type: NodeType
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"{self.node_type.value}"


@dataclass
class Program(ASTNode):
    """Root node representing the entire program"""
    declarations: List[Any]
    
    def __init__(self, declarations: List[Any], line: int = 0, column: int = 0):
        super().__init__(NodeType.PROGRAM, line, column)
        self.declarations = declarations


@dataclass
class VariableDeclaration(ASTNode):
    """Variable declaration node"""
    var_type: str
    identifier: str
    initializer: Optional[Any] = None
    is_const: bool = False
    
    def __init__(self, var_type: str, identifier: str, 
                 initializer: Optional[Any] = None, is_const: bool = False,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.var_type = var_type
        self.identifier = identifier
        self.initializer = initializer
        self.is_const = is_const


@dataclass
class ParameterDeclaration(ASTNode):
    """Function parameter node"""
    param_type: str
    identifier: str
    
    def __init__(self, param_type: str, identifier: str, 
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.PARAM_DECL, line, column)
        self.param_type = param_type
        self.identifier = identifier


@dataclass
class FunctionDeclaration(ASTNode):
    """Function declaration node"""
    return_type: str
    identifier: str
    parameters: List[ParameterDeclaration]
    body: 'Block'
    
    def __init__(self, return_type: str, identifier: str,
                 parameters: List[ParameterDeclaration], body: 'Block',
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.FUNCTION_DECL, line, column)
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.body = body


@dataclass
class Block(ASTNode):
    """Block of statements"""
    statements: List[Any]
    
    def __init__(self, statements: List[Any], line: int = 0, column: int = 0):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements


@dataclass
class IfStatement(ASTNode):
    """If statement"""
    condition: Any
    then_branch: Any
    else_branch: Optional[Any] = None
    
    def __init__(self, condition: Any, then_branch: Any,
                 else_branch: Optional[Any] = None,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.IF_STMT, line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


@dataclass
class WhileStatement(ASTNode):
    """While loop"""
    condition: Any
    body: Any
    
    def __init__(self, condition: Any, body: Any,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.WHILE_STMT, line, column)
        self.condition = condition
        self.body = body


@dataclass
class ForStatement(ASTNode):
    """For loop"""
    init: Optional[Any]
    condition: Any
    increment: Optional[Any]
    body: Any
    
    def __init__(self, init: Optional[Any], condition: Any,
                 increment: Optional[Any], body: Any,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.FOR_STMT, line, column)
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body


@dataclass
class ReturnStatement(ASTNode):
    """Return statement"""
    value: Optional[Any] = None
    
    def __init__(self, value: Optional[Any] = None,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.RETURN_STMT, line, column)
        self.value = value


@dataclass
class ExpressionStatement(ASTNode):
    """Expression used as a statement"""
    expression: Any
    
    def __init__(self, expression: Any, line: int = 0, column: int = 0):
        super().__init__(NodeType.EXPR_STMT, line, column)
        self.expression = expression


@dataclass
class AssignmentExpression(ASTNode):
    """Assignment expression"""
    identifier: str
    value: Any
    
    def __init__(self, identifier: str, value: Any,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.ASSIGN_EXPR, line, column)
        self.identifier = identifier
        self.value = value


@dataclass
class BinaryExpression(ASTNode):
    """Binary expression"""
    operator: str
    left: Any
    right: Any
    
    def __init__(self, operator: str, left: Any, right: Any,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.BINARY_EXPR, line, column)
        self.operator = operator
        self.left = left
        self.right = right


@dataclass
class UnaryExpression(ASTNode):
    """Unary expression"""
    operator: str
    operand: Any
    
    def __init__(self, operator: str, operand: Any,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.UNARY_EXPR, line, column)
        self.operator = operator
        self.operand = operand


@dataclass
class CallExpression(ASTNode):
    """Function call"""
    identifier: str
    arguments: List[Any]
    
    def __init__(self, identifier: str, arguments: List[Any],
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.CALL_EXPR, line, column)
        self.identifier = identifier
        self.arguments = arguments


@dataclass
class Identifier(ASTNode):
    """Identifier node"""
    name: str
    
    def __init__(self, name: str, line: int = 0, column: int = 0):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


@dataclass
class Literal(ASTNode):
    """Literal value node"""
    value: Any
    literal_type: str
    
    def __init__(self, value: Any, literal_type: str,
                 line: int = 0, column: int = 0):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type


@dataclass
class ReadStatement(ASTNode):
    """Read statement"""
    identifier: str
    
    def __init__(self, identifier: str, line: int = 0, column: int = 0):
        super().__init__(NodeType.READ_STMT, line, column)
        self.identifier = identifier


@dataclass
class PrintStatement(ASTNode):
    """Print statement"""
    expression: Any
    
    def __init__(self, expression: Any, line: int = 0, column: int = 0):
        super().__init__(NodeType.PRINT_STMT, line, column)
        self.expression = expression
