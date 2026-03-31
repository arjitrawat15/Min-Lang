"""Parser for MinLang using recursive descent."""

from typing import List, Optional

from ..lexer import Lexer, Token, TokenType
from .ast_nodes import (
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
    IntegerLiteral,
    Literal,
    ParameterDeclaration,
    PrintStatement,
    Program,
    ReadStatement,
    ReturnStatement,
    UnaryExpression,
    VariableDeclaration,
    WhileStatement,
)


class ParserError(Exception):
    """Raised when parser finds invalid syntax."""

    def __init__(self, message: str, token: Optional[Token]):
        if token is None:
            super().__init__(f"Parser Error: {message}")
        else:
            super().__init__(f"Parser Error at {token.line}:{token.column} - {message}")


class Parser:
    """Recursive-descent parser for MinLang."""

    TYPE_TOKENS = (TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR, TokenType.VOID)
    LOCAL_TYPE_TOKENS = (TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR)

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self) -> Optional[Token]:
        previous = self.current_token
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        return previous

    def expect(self, token_type: TokenType) -> Token:
        if self.current_token is None or self.current_token.type != token_type:
            raise ParserError(f"Expected {token_type.name}", self.current_token)
        return self.advance()

    def match(self, *token_types: TokenType) -> bool:
        return self.current_token is not None and self.current_token.type in token_types

    def parse(self) -> Program:
        declarations = []
        while not self.match(TokenType.EOF):
            declarations.append(self.parse_declaration())
        return Program(declarations)

    def parse_type_name(self, allow_void: bool = False) -> Token:
        expected = self.TYPE_TOKENS if allow_void else self.LOCAL_TYPE_TOKENS
        if not self.match(*expected):
            raise ParserError("Expected a type name", self.current_token)
        return self.advance()

    def parse_declaration(self):
        is_const = False
        if self.match(TokenType.CONST):
            is_const = True
            self.advance()

        type_token = self.parse_type_name(allow_void=True)
        name_token = self.expect(TokenType.IDENTIFIER)

        if self.match(TokenType.LPAREN):
            if is_const:
                raise ParserError("Functions cannot be declared as const", self.current_token)
            return self.parse_function(type_token, name_token)

        if type_token.type == TokenType.VOID:
            raise ParserError("Variables cannot use type void", type_token)

        return self.finish_variable_declaration(type_token, name_token, is_const=is_const, require_semicolon=True)

    def parse_function(self, return_type: Token, name_token: Token) -> FunctionDeclaration:
        self.expect(TokenType.LPAREN)
        parameters = []
        if not self.match(TokenType.RPAREN):
            parameters = self.parse_parameters()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()

        return FunctionDeclaration(
            return_type.value,
            name_token.value,
            parameters,
            body,
            return_type.line,
            return_type.column,
        )

    def parse_parameters(self) -> List[ParameterDeclaration]:
        params = []
        while True:
            type_token = self.parse_type_name(allow_void=False)
            name_token = self.expect(TokenType.IDENTIFIER)
            params.append(
                ParameterDeclaration(
                    type_token.value,
                    name_token.value,
                    type_token.line,
                    type_token.column,
                )
            )

            if not self.match(TokenType.COMMA):
                break
            self.advance()

        return params

    def finish_variable_declaration(
        self,
        type_token: Token,
        name_token: Token,
        is_const: bool,
        require_semicolon: bool,
    ) -> VariableDeclaration:
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.parse_expression()
        elif is_const:
            raise ParserError("Const declaration must include an initializer", name_token)

        if require_semicolon:
            self.expect(TokenType.SEMICOLON)

        return VariableDeclaration(
            type_token.value,
            name_token.value,
            initializer,
            is_const,
            type_token.line,
            type_token.column,
        )

    def parse_block(self) -> Block:
        brace = self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return Block(statements, brace.line, brace.column)

    def parse_statement(self):
        if self.match(TokenType.CONST, *self.LOCAL_TYPE_TOKENS):
            return self.parse_local_variable_statement()
        if self.match(TokenType.IF):
            return self.parse_if()
        if self.match(TokenType.WHILE):
            return self.parse_while()
        if self.match(TokenType.FOR):
            return self.parse_for()
        if self.match(TokenType.RETURN):
            return self.parse_return()
        if self.match(TokenType.READ):
            return self.parse_read()
        if self.match(TokenType.PRINT):
            return self.parse_print()
        if self.match(TokenType.LBRACE):
            return self.parse_block()

        expression = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        if isinstance(expression, AssignmentExpression):
            return AssignmentStatement(
                expression.identifier,
                expression.value,
                expression.line,
                expression.column,
            )
        return ExpressionStatement(expression, expression.line, expression.column)

    def parse_local_variable_statement(self) -> VariableDeclaration:
        is_const = False
        if self.match(TokenType.CONST):
            is_const = True
            self.advance()

        type_token = self.parse_type_name(allow_void=False)
        name_token = self.expect(TokenType.IDENTIFIER)
        return self.finish_variable_declaration(type_token, name_token, is_const, require_semicolon=True)

    def parse_if(self) -> IfStatement:
        if_token = self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_branch = self.parse_statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_branch = self.parse_statement()

        return IfStatement(condition, then_branch, else_branch, if_token.line, if_token.column)

    def parse_while(self) -> WhileStatement:
        while_token = self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_statement()
        return WhileStatement(condition, body, while_token.line, while_token.column)

    def parse_for(self) -> ForStatement:
        for_token = self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)

        init = None
        if not self.match(TokenType.SEMICOLON):
            init = self.parse_for_initializer()
        self.expect(TokenType.SEMICOLON)

        if self.match(TokenType.SEMICOLON):
            condition = Literal(True, "bool", for_token.line, for_token.column)
        else:
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        increment = None
        if not self.match(TokenType.RPAREN):
            increment = self.parse_expression()
        self.expect(TokenType.RPAREN)

        body = self.parse_statement()
        return ForStatement(init, condition, increment, body, for_token.line, for_token.column)

    def parse_for_initializer(self):
        if self.match(TokenType.CONST, *self.LOCAL_TYPE_TOKENS):
            is_const = False
            if self.match(TokenType.CONST):
                is_const = True
                self.advance()
            type_token = self.parse_type_name(allow_void=False)
            name_token = self.expect(TokenType.IDENTIFIER)
            return self.finish_variable_declaration(type_token, name_token, is_const, require_semicolon=False)
        return self.parse_expression()

    def parse_return(self) -> ReturnStatement:
        return_token = self.expect(TokenType.RETURN)
        value = None if self.match(TokenType.SEMICOLON) else self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value, return_token.line, return_token.column)

    def parse_read(self) -> ReadStatement:
        read_token = self.expect(TokenType.READ)
        self.expect(TokenType.LPAREN)
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return ReadStatement(identifier.value, read_token.line, read_token.column)

    def parse_print(self) -> PrintStatement:
        print_token = self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expression = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(expression, print_token.line, print_token.column)

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        expression = self.parse_logical_or()
        if self.match(TokenType.ASSIGN):
            assign_token = self.advance()
            if not isinstance(expression, Identifier):
                raise ParserError("Invalid assignment target", assign_token)
            value = self.parse_assignment()
            return AssignmentExpression(expression.name, value, expression.line, expression.column)
        return expression

    def parse_logical_or(self):
        expression = self.parse_logical_and()
        while self.match(TokenType.OR):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_logical_and(), op.line, op.column)
        return expression

    def parse_logical_and(self):
        expression = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_equality(), op.line, op.column)
        return expression

    def parse_equality(self):
        expression = self.parse_relational()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_relational(), op.line, op.column)
        return expression

    def parse_relational(self):
        expression = self.parse_additive()
        while self.match(
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
        ):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_additive(), op.line, op.column)
        return expression

    def parse_additive(self):
        expression = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_multiplicative(), op.line, op.column)
        return expression

    def parse_multiplicative(self):
        expression = self.parse_unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance()
            expression = BinaryExpression(op.value, expression, self.parse_unary(), op.line, op.column)
        return expression

    def parse_unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance()
            operand = self.parse_unary()
            return UnaryExpression(op.value, operand, op.line, op.column)
        return self.parse_postfix()

    def parse_postfix(self):
        expression = self.parse_primary()
        while self.match(TokenType.LPAREN):
            open_paren = self.advance()
            args = []
            if not self.match(TokenType.RPAREN):
                args.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            if not isinstance(expression, Identifier):
                raise ParserError("Only identifiers can be called", open_paren)
            expression = CallExpression(expression.name, args, open_paren.line, open_paren.column)
        return expression

    def parse_primary(self):
        if self.match(TokenType.INTEGER_LITERAL):
            token = self.advance()
            return IntegerLiteral(token.value, token.line, token.column)
        if self.match(TokenType.FLOAT_LITERAL):
            token = self.advance()
            return Literal(token.value, "float", token.line, token.column)
        if self.match(TokenType.TRUE, TokenType.FALSE):
            token = self.advance()
            return Literal(token.value, "bool", token.line, token.column)
        if self.match(TokenType.CHAR_LITERAL):
            token = self.advance()
            return Literal(token.value, "char", token.line, token.column)
        if self.match(TokenType.STRING_LITERAL):
            token = self.advance()
            return Literal(token.value, "string", token.line, token.column)
        if self.match(TokenType.IDENTIFIER):
            token = self.advance()
            return Identifier(token.value, token.line, token.column)
        if self.match(TokenType.LPAREN):
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expression
        raise ParserError("Unexpected token", self.current_token)


def parse(tokens: List[Token]) -> Program:
    """Convenience function for parsing an existing token list."""
    return Parser(tokens).parse()


def parse_file(filename: str) -> Program:
    """Parse a source file and return its AST."""
    with open(filename, "r", encoding="utf-8") as source_file:
        lexer = Lexer(source_file.read())
    return Parser(lexer.tokenize()).parse()


def parse_string(source: str) -> Program:
    """Parse a source string and return its AST."""
    return Parser(Lexer(source).tokenize()).parse()
