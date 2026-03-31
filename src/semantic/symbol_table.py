"""Symbol table and scope management for semantic analysis."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Symbol:
    """Represents a declared name in a scope."""

    name: str
    symbol_type: str
    kind: str
    is_const: bool = False
    parameters: Optional[List[str]] = None
    return_type: Optional[str] = None
    line: int = 0
    column: int = 0


@dataclass
class Scope:
    """A single lexical scope containing declared symbols."""

    name: str
    parent: Optional["Scope"] = None
    symbols: Dict[str, Symbol] = field(default_factory=dict)

    def define(self, symbol: Symbol) -> None:
        """Define a symbol in the current scope."""
        if symbol.name in self.symbols:
            raise ValueError(f"'{symbol.name}' is already declared in scope '{self.name}'")
        self.symbols[symbol.name] = symbol

    def resolve(self, name: str, current_only: bool = False) -> Optional[Symbol]:
        """Find a symbol by name, optionally only in this scope."""
        if name in self.symbols:
            return self.symbols[name]
        if current_only or self.parent is None:
            return None
        return self.parent.resolve(name)


class SymbolTable:
    """Manages the active scope stack during semantic analysis."""

    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope

    def enter_scope(self, name: str) -> Scope:
        """Push a new child scope and make it current."""
        new_scope = Scope(name=name, parent=self.current_scope)
        self.current_scope = new_scope
        return new_scope

    def exit_scope(self) -> Scope:
        """Pop to parent scope."""
        parent = self.current_scope.parent
        if parent is None:
            raise ValueError("Cannot exit the global scope")
        previous = self.current_scope
        self.current_scope = parent
        return previous

    def define(self, symbol: Symbol) -> None:
        """Define symbol in current scope."""
        self.current_scope.define(symbol)

    def lookup(self, name: str, current_only: bool = False) -> Optional[Symbol]:
        """Look up symbol from current scope outward."""
        return self.current_scope.resolve(name, current_only=current_only)
