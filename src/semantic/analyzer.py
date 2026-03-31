"""Semantic analyzer for MinLang."""

from dataclasses import dataclass
from typing import Optional

from ..parser.ast_nodes import (
    AssignmentExpression,
    AssignmentStatement,
    BinaryExpression,
    Block,
    CallExpression,
    ExpressionStatement,
    ForStatement,
    FunctionDeclaration,
    Identifier,
    IfStatement,
    Literal,
    PrintStatement,
    Program,
    ReadStatement,
    ReturnStatement,
    UnaryExpression,
    VariableDeclaration,
    WhileStatement,
)
from .symbol_table import Symbol, SymbolTable


@dataclass
class SemanticError(Exception):
    """Semantic error with source location."""

    message: str
    line: int = 0
    column: int = 0

    def __str__(self) -> str:
        if self.line > 0 and self.column > 0:
            return f"Semantic Error at {self.line}:{self.column} - {self.message}"
        return f"Semantic Error: {self.message}"


class SemanticAnalyzer:
    """Performs type checking and scope validation on the AST."""

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_function: Optional[FunctionDeclaration] = None
        self.current_function_return_type: Optional[str] = None
        self.has_return_in_current_function = False

    def analyze(self, program: Program) -> Program:
        """Analyze a full program and raise on semantic violations."""
        if not isinstance(program, Program):
            raise SemanticError("Expected Program node as semantic input")

        # Pass 1: define globals and function signatures.
        for declaration in program.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self._declare_function(declaration)
            elif isinstance(declaration, VariableDeclaration):
                self._declare_variable(declaration)
            else:
                raise SemanticError(
                    f"Unsupported top-level declaration: {type(declaration).__name__}",
                    declaration.line,
                    declaration.column,
                )

        # Pass 2: analyze function bodies.
        for declaration in program.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self._analyze_function(declaration)

        return program

    def _declare_function(self, declaration: FunctionDeclaration) -> None:
        param_types = [param.param_type for param in declaration.parameters]
        symbol = Symbol(
            name=declaration.identifier,
            symbol_type="function",
            kind="function",
            parameters=param_types,
            return_type=declaration.return_type,
            line=declaration.line,
            column=declaration.column,
        )
        try:
            self.symbol_table.global_scope.define(symbol)
        except ValueError as error:
            raise SemanticError(str(error), declaration.line, declaration.column)

    def _declare_variable(self, declaration: VariableDeclaration) -> None:
        symbol = Symbol(
            name=declaration.identifier,
            symbol_type=declaration.var_type,
            kind="variable",
            is_const=declaration.is_const,
            line=declaration.line,
            column=declaration.column,
        )
        try:
            self.symbol_table.define(symbol)
        except ValueError as error:
            raise SemanticError(str(error), declaration.line, declaration.column)

        if declaration.initializer is not None:
            init_type = self._analyze_expression(declaration.initializer)
            self._require_assignable(
                expected=declaration.var_type,
                actual=init_type,
                line=declaration.line,
                column=declaration.column,
                context=f"initializer for '{declaration.identifier}'",
            )
        elif declaration.is_const:
            raise SemanticError(
                f"Const variable '{declaration.identifier}' must be initialized",
                declaration.line,
                declaration.column,
            )

    def _analyze_function(self, declaration: FunctionDeclaration) -> None:
        self.current_function = declaration
        self.current_function_return_type = declaration.return_type
        self.has_return_in_current_function = False

        self.symbol_table.enter_scope(f"function:{declaration.identifier}")
        try:
            for parameter in declaration.parameters:
                param_symbol = Symbol(
                    name=parameter.identifier,
                    symbol_type=parameter.param_type,
                    kind="parameter",
                    line=parameter.line,
                    column=parameter.column,
                )
                try:
                    self.symbol_table.define(param_symbol)
                except ValueError as error:
                    raise SemanticError(str(error), parameter.line, parameter.column)

            self._analyze_block(declaration.body, create_scope=False)

            if declaration.return_type != "void" and not self.has_return_in_current_function:
                raise SemanticError(
                    f"Function '{declaration.identifier}' must return a value of type {declaration.return_type}",
                    declaration.line,
                    declaration.column,
                )
        finally:
            self.symbol_table.exit_scope()
            self.current_function = None
            self.current_function_return_type = None

    def _analyze_block(self, block: Block, create_scope: bool = True) -> None:
        if create_scope:
            self.symbol_table.enter_scope("block")

        try:
            for statement in block.statements:
                self._analyze_statement(statement)
        finally:
            if create_scope:
                self.symbol_table.exit_scope()

    def _analyze_statement(self, statement) -> None:
        if isinstance(statement, VariableDeclaration):
            self._declare_variable(statement)
            return

        if isinstance(statement, AssignmentStatement):
            self._analyze_expression(statement)
            return

        if isinstance(statement, ExpressionStatement):
            self._analyze_expression(statement.expression)
            return

        if isinstance(statement, IfStatement):
            condition_type = self._analyze_expression(statement.condition)
            self._require_type(
                actual=condition_type,
                expected="bool",
                line=statement.line,
                column=statement.column,
                context="if condition",
            )
            self._analyze_statement(statement.then_branch)
            if statement.else_branch is not None:
                self._analyze_statement(statement.else_branch)
            return

        if isinstance(statement, WhileStatement):
            condition_type = self._analyze_expression(statement.condition)
            self._require_type(
                actual=condition_type,
                expected="bool",
                line=statement.line,
                column=statement.column,
                context="while condition",
            )
            self._analyze_statement(statement.body)
            return

        if isinstance(statement, ForStatement):
            self.symbol_table.enter_scope("for")
            try:
                if statement.init is not None:
                    if isinstance(statement.init, VariableDeclaration):
                        self._declare_variable(statement.init)
                    else:
                        self._analyze_expression(statement.init)

                condition_type = self._analyze_expression(statement.condition)
                self._require_type(
                    actual=condition_type,
                    expected="bool",
                    line=statement.line,
                    column=statement.column,
                    context="for condition",
                )

                if statement.increment is not None:
                    self._analyze_expression(statement.increment)

                self._analyze_statement(statement.body)
            finally:
                self.symbol_table.exit_scope()
            return

        if isinstance(statement, ReturnStatement):
            self._analyze_return(statement)
            return

        if isinstance(statement, ReadStatement):
            symbol = self.symbol_table.lookup(statement.identifier)
            if symbol is None:
                raise SemanticError(
                    f"Cannot read into undeclared variable '{statement.identifier}'",
                    statement.line,
                    statement.column,
                )
            if symbol.is_const:
                raise SemanticError(
                    f"Cannot read into const variable '{statement.identifier}'",
                    statement.line,
                    statement.column,
                )
            return

        if isinstance(statement, PrintStatement):
            self._analyze_expression(statement.expression)
            return

        if isinstance(statement, Block):
            self._analyze_block(statement, create_scope=True)
            return

        raise SemanticError(
            f"Unsupported statement type: {type(statement).__name__}",
            statement.line,
            statement.column,
        )

    def _analyze_return(self, statement: ReturnStatement) -> None:
        if self.current_function_return_type is None:
            raise SemanticError("Return statement outside of function", statement.line, statement.column)

        self.has_return_in_current_function = True
        if self.current_function_return_type == "void":
            if statement.value is not None:
                raise SemanticError("Void function cannot return a value", statement.line, statement.column)
            return

        if statement.value is None:
            raise SemanticError(
                f"Function must return a value of type {self.current_function_return_type}",
                statement.line,
                statement.column,
            )

        value_type = self._analyze_expression(statement.value)
        self._require_assignable(
            expected=self.current_function_return_type,
            actual=value_type,
            line=statement.line,
            column=statement.column,
            context="return value",
        )

    def _analyze_expression(self, expression) -> str:
        if isinstance(expression, Literal):
            return expression.literal_type

        if isinstance(expression, Identifier):
            symbol = self.symbol_table.lookup(expression.name)
            if symbol is None:
                raise SemanticError(
                    f"Use of undeclared identifier '{expression.name}'",
                    expression.line,
                    expression.column,
                )
            return symbol.symbol_type

        if isinstance(expression, AssignmentExpression):
            symbol = self.symbol_table.lookup(expression.identifier)
            if symbol is None:
                raise SemanticError(
                    f"Assignment to undeclared identifier '{expression.identifier}'",
                    expression.line,
                    expression.column,
                )
            if symbol.is_const:
                raise SemanticError(
                    f"Cannot assign to const variable '{expression.identifier}'",
                    expression.line,
                    expression.column,
                )
            value_type = self._analyze_expression(expression.value)
            self._require_assignable(
                expected=symbol.symbol_type,
                actual=value_type,
                line=expression.line,
                column=expression.column,
                context=f"assignment to '{expression.identifier}'",
            )
            return symbol.symbol_type

        if isinstance(expression, UnaryExpression):
            operand_type = self._analyze_expression(expression.operand)
            if expression.operator == "-":
                if not self._is_numeric(operand_type):
                    raise SemanticError("Unary '-' requires numeric operand", expression.line, expression.column)
                return operand_type
            if expression.operator == "!":
                self._require_type(
                    actual=operand_type,
                    expected="bool",
                    line=expression.line,
                    column=expression.column,
                    context="unary '!'",
                )
                return "bool"
            raise SemanticError(f"Unsupported unary operator '{expression.operator}'", expression.line, expression.column)

        if isinstance(expression, BinaryExpression):
            return self._analyze_binary_expression(expression)

        if isinstance(expression, CallExpression):
            function_symbol = self.symbol_table.global_scope.resolve(expression.identifier)
            if function_symbol is None or function_symbol.kind != "function":
                raise SemanticError(
                    f"Call to undeclared function '{expression.identifier}'",
                    expression.line,
                    expression.column,
                )

            expected_args = function_symbol.parameters or []
            if len(expected_args) != len(expression.arguments):
                raise SemanticError(
                    f"Function '{expression.identifier}' expects {len(expected_args)} argument(s), got {len(expression.arguments)}",
                    expression.line,
                    expression.column,
                )

            for index, (expected_type, arg_expr) in enumerate(zip(expected_args, expression.arguments), start=1):
                actual_type = self._analyze_expression(arg_expr)
                self._require_assignable(
                    expected=expected_type,
                    actual=actual_type,
                    line=arg_expr.line,
                    column=arg_expr.column,
                    context=f"argument {index} of '{expression.identifier}'",
                )

            return function_symbol.return_type or "void"

        raise SemanticError(
            f"Unsupported expression type: {type(expression).__name__}",
            expression.line,
            expression.column,
        )

    def _analyze_binary_expression(self, expression: BinaryExpression) -> str:
        left_type = self._analyze_expression(expression.left)
        right_type = self._analyze_expression(expression.right)
        op = expression.operator

        arithmetic_ops = {"+", "-", "*", "/", "%"}
        relational_ops = {"<", ">", "<=", ">="}
        equality_ops = {"==", "!="}
        logical_ops = {"&&", "||"}

        if op in arithmetic_ops:
            if not (self._is_numeric(left_type) and self._is_numeric(right_type)):
                raise SemanticError(
                    f"Operator '{op}' requires numeric operands",
                    expression.line,
                    expression.column,
                )
            if op == "%" and (left_type != "int" or right_type != "int"):
                raise SemanticError("Operator '%' requires integer operands", expression.line, expression.column)
            if op == "/":
                return "float"
            if left_type == "float" or right_type == "float":
                return "float"
            return "int"

        if op in relational_ops:
            if not (self._is_numeric(left_type) and self._is_numeric(right_type)):
                raise SemanticError(
                    f"Operator '{op}' requires numeric operands",
                    expression.line,
                    expression.column,
                )
            return "bool"

        if op in equality_ops:
            if not self._types_compatible(left_type, right_type):
                raise SemanticError(
                    f"Cannot compare values of type '{left_type}' and '{right_type}'",
                    expression.line,
                    expression.column,
                )
            return "bool"

        if op in logical_ops:
            self._require_type(
                actual=left_type,
                expected="bool",
                line=expression.line,
                column=expression.column,
                context=f"left operand of '{op}'",
            )
            self._require_type(
                actual=right_type,
                expected="bool",
                line=expression.line,
                column=expression.column,
                context=f"right operand of '{op}'",
            )
            return "bool"

        raise SemanticError(f"Unsupported binary operator '{op}'", expression.line, expression.column)

    @staticmethod
    def _is_numeric(type_name: str) -> bool:
        return type_name in {"int", "float"}

    @staticmethod
    def _types_compatible(left_type: str, right_type: str) -> bool:
        if left_type == right_type:
            return True
        return {left_type, right_type} == {"int", "float"}

    def _require_assignable(self, expected: str, actual: str, line: int, column: int, context: str) -> None:
        if expected == actual:
            return
        if expected == "float" and actual == "int":
            return
        raise SemanticError(
            f"Type mismatch in {context}: expected '{expected}', got '{actual}'",
            line,
            column,
        )

    def _require_type(self, actual: str, expected: str, line: int, column: int, context: str) -> None:
        if actual != expected:
            raise SemanticError(
                f"Type mismatch in {context}: expected '{expected}', got '{actual}'",
                line,
                column,
            )
