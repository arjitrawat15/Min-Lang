"""
Symbol Table for MinLang Compiler
Manages scopes, symbols, and type information
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class SymbolKind(Enum):
    """Kind of symbol"""
    VARIABLE = "variable"
    CONSTANT = "constant"
    FUNCTION = "function"
    PARAMETER = "parameter"


class DataType(Enum):
    """Data types in MinLang"""
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    CHAR = "char"
    VOID = "void"
    ERROR = "error"  # For error recovery
    
    @classmethod
    def from_string(cls, type_str: str) -> 'DataType':
        """Convert string to DataType"""
        type_map = {
            'int': cls.INT,
            'float': cls.FLOAT,
            'bool': cls.BOOL,
            'char': cls.CHAR,
            'void': cls.VOID,
        }
        return type_map.get(type_str.lower(), cls.ERROR)
    
    def is_numeric(self) -> bool:
        """Check if type is numeric"""
        return self in (DataType.INT, DataType.FLOAT)
    
    def is_compatible_with(self, other: 'DataType') -> bool:
        """Check if types are compatible for operations"""
        if self == other:
            return True
        # Numeric types are compatible with each other
        if self.is_numeric() and other.is_numeric():
            return True
        return False


@dataclass
class Symbol:
    """
    Represents a symbol in the symbol table
    
    Attributes:
        name: Symbol identifier
        kind: Kind of symbol (variable, function, etc.)
        data_type: Data type of the symbol
        scope_level: Scope depth where symbol is defined
        is_initialized: Whether variable has been initialized
        parameters: For functions, list of parameter types
        return_type: For functions, return type
        line: Line number where declared
        column: Column number where declared
    """
    name: str
    kind: SymbolKind
    data_type: DataType
    scope_level: int
    is_initialized: bool = False
    parameters: Optional[List[DataType]] = None
    return_type: Optional[DataType] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self) -> str:
        if self.kind == SymbolKind.FUNCTION:
            params = ', '.join(str(p.value) for p in (self.parameters or []))
            return f"Function {self.name}({params}) -> {self.return_type.value}"
        return f"{self.kind.value} {self.name}: {self.data_type.value}"


class Scope:
    """
    Represents a single scope in the program
    
    Attributes:
        level: Scope nesting level (0 = global)
        symbols: Dictionary of symbols in this scope
        parent: Parent scope (None for global scope)
    """
    
    def __init__(self, level: int, parent: Optional['Scope'] = None):
        self.level = level
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent
    
    def define(self, symbol: Symbol) -> bool:
        """
        Define a new symbol in this scope
        
        Args:
            symbol: Symbol to define
            
        Returns:
            True if successful, False if symbol already exists
        """
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in this scope only
        
        Args:
            name: Symbol name
            
        Returns:
            Symbol if found, None otherwise
        """
        return self.symbols.get(name)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in this scope and parent scopes
        
        Args:
            name: Symbol name
            
        Returns:
            Symbol if found, None otherwise
        """
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        if self.parent is not None:
            return self.parent.lookup(name)
        return None
    
    def __repr__(self) -> str:
        symbols_str = ', '.join(self.symbols.keys())
        return f"Scope(level={self.level}, symbols=[{symbols_str}])"


class SymbolTable:
    """
    Symbol table with scope management
    
    Manages nested scopes and symbol lookup with proper scoping rules
    """
    
    def __init__(self):
        """Initialize with global scope"""
        self.global_scope = Scope(level=0)
        self.current_scope = self.global_scope
        self.scope_stack: List[Scope] = [self.global_scope]
        self._initialize_built_ins()
    
    def _initialize_built_ins(self):
        """Initialize built-in functions"""
        # read() function - void read(identifier)
        read_symbol = Symbol(
            name="read",
            kind=SymbolKind.FUNCTION,
            data_type=DataType.VOID,
            scope_level=0,
            is_initialized=True,
            parameters=[],  # Takes identifier, handled specially
            return_type=DataType.VOID
        )
        self.global_scope.define(read_symbol)
        
        # print() function - void print(any)
        print_symbol = Symbol(
            name="print",
            kind=SymbolKind.FUNCTION,
            data_type=DataType.VOID,
            scope_level=0,
            is_initialized=True,
            parameters=[],  # Takes any type
            return_type=DataType.VOID
        )
        self.global_scope.define(print_symbol)
    
    def enter_scope(self):
        """Enter a new scope (e.g., function body, block)"""
        new_level = self.current_scope.level + 1
        new_scope = Scope(level=new_level, parent=self.current_scope)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """Exit the current scope"""
        if len(self.scope_stack) <= 1:
            raise RuntimeError("Cannot exit global scope")
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
    
    def define_symbol(self, name: str, kind: SymbolKind, data_type: DataType,
                     line: int = 0, column: int = 0,
                     parameters: Optional[List[DataType]] = None,
                     return_type: Optional[DataType] = None) -> bool:
        """
        Define a new symbol in the current scope
        
        Args:
            name: Symbol name
            kind: Symbol kind
            data_type: Data type
            line: Line number
            column: Column number
            parameters: For functions, parameter types
            return_type: For functions, return type
            
        Returns:
            True if successful, False if already defined in current scope
        """
        symbol = Symbol(
            name=name,
            kind=kind,
            data_type=data_type,
            scope_level=self.current_scope.level,
            is_initialized=(kind == SymbolKind.FUNCTION),
            parameters=parameters,
            return_type=return_type,
            line=line,
            column=column
        )
        return self.current_scope.define(symbol)
    
    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in current and parent scopes
        
        Args:
            name: Symbol name
            
        Returns:
            Symbol if found, None otherwise
        """
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol only in the current scope
        
        Args:
            name: Symbol name
            
        Returns:
            Symbol if found in current scope, None otherwise
        """
        return self.current_scope.lookup_local(name)
    
    def mark_initialized(self, name: str):
        """
        Mark a variable as initialized
        
        Args:
            name: Variable name
        """
        symbol = self.lookup_symbol(name)
        if symbol:
            symbol.is_initialized = True
    
    def is_initialized(self, name: str) -> bool:
        """
        Check if a variable is initialized
        
        Args:
            name: Variable name
            
        Returns:
            True if initialized, False otherwise
        """
        symbol = self.lookup_symbol(name)
        return symbol.is_initialized if symbol else False
    
    def get_current_scope_level(self) -> int:
        """Get the current scope level"""
        return self.current_scope.level
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols from all scopes"""
        symbols = []
        for scope in self.scope_stack:
            symbols.extend(scope.symbols.values())
        return symbols
    
    def print_table(self):
        """Print the symbol table (for debugging)"""
        print("\n=== SYMBOL TABLE ===")
        for scope in self.scope_stack:
            print(f"\nScope Level {scope.level}:")
            for name, symbol in scope.symbols.items():
                init_status = "✓" if symbol.is_initialized else "✗"
                print(f"  [{init_status}] {symbol}")
        print("=" * 20 + "\n")


class TypeChecker:
    """
    Helper class for type checking operations
    """
    
    @staticmethod
    def check_binary_operation(op: str, left_type: DataType, 
                               right_type: DataType) -> Optional[DataType]:
        """
        Check if binary operation is valid and return result type
        
        Args:
            op: Operator (+, -, *, /, etc.)
            left_type: Left operand type
            right_type: Right operand type
            
        Returns:
            Result type if valid, None if invalid
        """
        # Arithmetic operators: +, -, *, /, %
        if op in ['+', '-', '*', '/', '%']:
            if left_type.is_numeric() and right_type.is_numeric():
                # If either is float, result is float
                if left_type == DataType.FLOAT or right_type == DataType.FLOAT:
                    return DataType.FLOAT
                return DataType.INT
            return None
        
        # Relational operators: <, >, <=, >=
        elif op in ['<', '>', '<=', '>=']:
            if left_type.is_numeric() and right_type.is_numeric():
                return DataType.BOOL
            return None
        
        # Equality operators: ==, !=
        elif op in ['==', '!=']:
            if left_type.is_compatible_with(right_type):
                return DataType.BOOL
            return None
        
        # Logical operators: &&, ||
        elif op in ['&&', '||']:
            if left_type == DataType.BOOL and right_type == DataType.BOOL:
                return DataType.BOOL
            return None
        
        return None
    
    @staticmethod
    def check_unary_operation(op: str, operand_type: DataType) -> Optional[DataType]:
        """
        Check if unary operation is valid and return result type
        
        Args:
            op: Operator (-, !)
            operand_type: Operand type
            
        Returns:
            Result type if valid, None if invalid
        """
        # Unary minus
        if op == '-':
            if operand_type.is_numeric():
                return operand_type
            return None
        
        # Logical NOT
        elif op == '!':
            if operand_type == DataType.BOOL:
                return DataType.BOOL
            return None
        
        return None
    
    @staticmethod
    def check_assignment(var_type: DataType, value_type: DataType) -> bool:
        """
        Check if assignment is valid
        
        Args:
            var_type: Variable type
            value_type: Value type
            
        Returns:
            True if valid, False otherwise
        """
        # Exact match
        if var_type == value_type:
            return True
        
        # Numeric types are compatible
        if var_type.is_numeric() and value_type.is_numeric():
            return True
        
        return False
    
    @staticmethod
    def check_function_call(func_params: List[DataType], 
                           call_args: List[DataType]) -> bool:
        """
        Check if function call arguments match parameters
        
        Args:
            func_params: Function parameter types
            call_args: Call argument types
            
        Returns:
            True if valid, False otherwise
        """
        if len(func_params) != len(call_args):
            return False
        
        for param_type, arg_type in zip(func_params, call_args):
            if not param_type.is_compatible_with(arg_type):
                return False
        
        return True
    
    @staticmethod
    def get_literal_type(literal_type_str: str) -> DataType:
        """
        Get DataType from literal type string
        
        Args:
            literal_type_str: Literal type ('int', 'float', 'bool', etc.)
            
        Returns:
            Corresponding DataType
        """
        return DataType.from_string(literal_type_str)
