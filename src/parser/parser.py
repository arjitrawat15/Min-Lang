"""Parser for MinLang - Simplified recursive descent parser"""
from typing import List
from ..lexer import Token, TokenType, Lexer
from .ast_nodes import *

class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"Parser Error at {token.line}:{token.column} - {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def advance(self):
        old = self.current_token
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        return old
    
    def expect(self, token_type: TokenType):
        if not self.current_token or self.current_token.type != token_type:
            raise ParserError(f"Expected {token_type.name}", self.current_token)
        return self.advance()
    
    def match(self, *token_types):
        return self.current_token and self.current_token.type in token_types
    
    def parse(self):
        declarations = []
        while not self.match(TokenType.EOF):
            declarations.append(self.parse_declaration())
        return Program(declarations)
    
    def parse_declaration(self):
        # Simplified - handles only basic variable and function declarations
        if not self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR, TokenType.VOID):
            raise ParserError("Expected type", self.current_token)
        var_type = self.advance().value
        identifier = self.expect(TokenType.IDENTIFIER).value
        if self.match(TokenType.LPAREN):
            return self.parse_function(var_type, identifier, 0, 0)
        return self.parse_variable(var_type, identifier)
    
    def parse_function(self, ret_type, name, line, col):
        self.expect(TokenType.LPAREN)
        params = []
        if not self.match(TokenType.RPAREN):
            params = self.parse_parameters()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDeclaration(ret_type, name, params, body, line, col)
    
    def parse_parameters(self):
        params = []
        while True:
            ptype = self.advance().value
            pname = self.expect(TokenType.IDENTIFIER).value
            params.append(ParameterDeclaration(ptype, pname))
            if not self.match(TokenType.COMMA):
                break
            self.advance()
        return params
    
    def parse_variable(self, vtype, name):
        init = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            init = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return VariableDeclaration(vtype, name, init)
    
    def parse_block(self):
        self.expect(TokenType.LBRACE)
        stmts = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return Block(stmts)
    
    def parse_statement(self):
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR):
            return self.parse_local_var()
        if self.match(TokenType.IF):
            return self.parse_if()
        if self.match(TokenType.WHILE):
            return self.parse_while()
        if self.match(TokenType.RETURN):
            return self.parse_return()
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def parse_local_var(self):
        vtype = self.advance().value
        name = self.expect(TokenType.IDENTIFIER).value
        init = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            init = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return VariableDeclaration(vtype, name, init)
    
    def parse_if(self):
        self.advance()
        self.expect(TokenType.LPAREN)
        cond = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_b = self.parse_statement()
        else_b = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_b = self.parse_statement()
        return IfStatement(cond, then_b, else_b)
    
    def parse_while(self):
        self.advance()
        self.expect(TokenType.LPAREN)
        cond = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_statement()
        return WhileStatement(cond, body)
    
    def parse_return(self):
        self.advance()
        val = None if self.match(TokenType.SEMICOLON) else self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(val)
    
    def parse_expression(self):
        return self.parse_assignment()
    
    def parse_assignment(self):
        expr = self.parse_logical_or()
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, Identifier):
                raise ParserError("Invalid assignment target", self.current_token)
            self.advance()
            val = self.parse_assignment()
            return AssignmentExpression(expr.name, val)
        return expr
    
    def parse_logical_or(self):
        expr = self.parse_logical_and()
        while self.match(TokenType.OR):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_logical_and())
        return expr
    
    def parse_logical_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_equality())
        return expr
    
    def parse_equality(self):
        expr = self.parse_relational()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_relational())
        return expr
    
    def parse_relational(self):
        expr = self.parse_additive()
        while self.match(TokenType.LESS_THAN, TokenType.GREATER_THAN, 
                         TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_additive())
        return expr
    
    def parse_additive(self):
        expr = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_multiplicative())
        return expr
    
    def parse_multiplicative(self):
        expr = self.parse_unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            expr = BinaryExpression(op, expr, self.parse_unary())
        return expr
    
    def parse_unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            return UnaryExpression(op, self.parse_unary())
        return self.parse_postfix()
    
    def parse_postfix(self):
        expr = self.parse_primary()
        while self.match(TokenType.LPAREN):
            self.advance()
            args = []
            if not self.match(TokenType.RPAREN):
                args.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            if not isinstance(expr, Identifier):
                raise ParserError("Only identifiers can be called", self.current_token)
            expr = CallExpression(expr.name, args)
        return expr
    
    def parse_primary(self):
        if self.match(TokenType.INTEGER_LITERAL):
            return Literal(self.advance().value, 'int')
        if self.match(TokenType.FLOAT_LITERAL):
            return Literal(self.advance().value, 'float')
        if self.match(TokenType.TRUE, TokenType.FALSE):
            return Literal(self.advance().value, 'bool')
        if self.match(TokenType.STRING_LITERAL):
            return Literal(self.advance().value, 'string')
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.advance().value)
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        raise ParserError(f"Unexpected token", self.current_token)

def parse_file(filename):
    with open(filename) as f:
        lexer = Lexer(f.read())
    return Parser(lexer.tokenize()).parse()

def parse_string(source):
    return Parser(Lexer(source).tokenize()).parse()
