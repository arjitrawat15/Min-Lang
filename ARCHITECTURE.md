# MinLang Compiler Architecture

## Overview

This document describes the architectural design of the MinLang compiler, including component organization, data flow, interfaces, and design decisions.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [Data Flow](#data-flow)
4. [Design Patterns](#design-patterns)
5. [Interface Specifications](#interface-specifications)
6. [Directory Structure](#directory-structure)
7. [Extensibility](#extensibility)

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────┐
│                   MinLang Compiler                    │
│                                                        │
│  ┌───────────┐   ┌────────┐   ┌──────────┐          │
│  │  Source   │──▶│ Lexer  │──▶│  Parser  │          │
│  │   Code    │   └────────┘   └──────────┘          │
│  └───────────┘        │              │                │
│                       ▼              ▼                │
│                  Token Stream    Parse Tree/AST      │
│                                        │              │
│                                        ▼              │
│                              ┌─────────────────┐     │
│                              │    Semantic     │     │
│                              │    Analyzer     │     │
│                              └─────────────────┘     │
│                                        │              │
│                                        ▼              │
│                                  Annotated AST       │
│                                        │              │
│                                        ▼              │
│                              ┌─────────────────┐     │
│                              │   IR Generator  │     │
│                              │      (TAC)      │     │
│                              └─────────────────┘     │
│                                        │              │
│                                        ▼              │
│                              ┌─────────────────┐     │
│                              │   Optimizer     │     │
│                              │   (Optional)    │     │
│                              └─────────────────┘     │
│                                        │              │
│                                        ▼              │
│                              ┌─────────────────┐     │
│                              │  Code Generator │     │
│                              └─────────────────┘     │
│                                        │              │
│                                        ▼              │
│  ┌───────────┐                   Target Code         │
│  │  Output   │◀────────────────────────┘             │
│  └───────────┘                                        │
└──────────────────────────────────────────────────────┘

Supporting Components:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Error Handler│  │ Symbol Table │  │   Logger     │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 1.2 Layered Architecture

```
┌─────────────────────────────────────────┐
│        Application Layer                 │
│     (main.py - CLI Interface)           │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│       Compilation Pipeline Layer         │
│  (Orchestrates compiler phases)         │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│      Analysis and Transform Layer        │
│  Lexer │ Parser │ Semantic │ Codegen    │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Utility Layer                    │
│  Error │ Logger │ Symbol Table          │
└─────────────────────────────────────────┘
```

## 2. Component Details

### 2.1 Lexical Analyzer (Lexer)

**Purpose:** Tokenize source code

**Location:** `src/lexer/`

**Key Classes:**
- `Tokenizer`: Main tokenization logic
- `Token`: Token data structure
- `TokenType`: Token type enumeration

**Input:** Source code string  
**Output:** List of tokens

**Key Responsibilities:**
- Character stream processing
- Token recognition
- Error detection (invalid characters, malformed literals)
- Position tracking (line, column)
- Comment removal

**Design Decisions:**
- Single-pass scanning for efficiency
- Lookahead for multi-character operators
- Separate keyword/identifier handling

### 2.2 Syntax Analyzer (Parser)

**Purpose:** Build Abstract Syntax Tree

**Location:** `src/parser/`

**Key Classes:**
- `Parser`: Recursive descent parser
- `ASTNode`: Base class for AST nodes
- Multiple AST node subclasses (Expression, Statement, etc.)

**Input:** Token stream  
**Output:** Abstract Syntax Tree (Program node)

**Key Responsibilities:**
- Syntax validation
- Parse tree construction
- Error recovery
- AST generation

**Design Decisions:**
- Recursive descent approach for clarity
- Operator precedence climbing for expressions
- Visitor pattern for AST traversal
- Immutable AST nodes (dataclasses)

### 2.3 Semantic Analyzer

**Purpose:** Validate semantics and types

**Location:** `src/semantic/`

**Key Classes:**
- `SemanticAnalyzer`: Type checker
- `SymbolTable`: Symbol management
- `Scope`: Scope representation

**Input:** AST  
**Output:** Annotated AST + Symbol Table

**Key Responsibilities:**
- Type checking
- Variable declaration verification
- Scope management
- Function signature validation
- Semantic error detection

**Design Decisions:**
- Hierarchical symbol tables
- AST visitor pattern for traversal
- Type inference where applicable

### 2.4 Intermediate Representation Generator

**Purpose:** Generate Three-Address Code

**Location:** `src/codegen/`

**Key Classes:**
- `IRGenerator`: TAC generation
- `TACInstruction`: IR instruction
- `ControlFlowGraph`: CFG construction

**Input:** Annotated AST  
**Output:** TAC instruction list

**Key Responsibilities:**
- IR instruction generation
- Temporary variable management
- Control flow translation
- Basic block identification

**Design Decisions:**
- Three-address code format
- Unlimited temporaries (for clarity)
- Linear IR with explicit jumps

### 2.5 Optimizer (Optional)

**Purpose:** Improve code efficiency

**Location:** `src/codegen/`

**Key Classes:**
- `Optimizer`: Optimization coordinator
- Various optimization passes

**Input:** TAC  
**Output:** Optimized TAC

**Planned Optimizations:**
- Constant folding
- Dead code elimination
- Common subexpression elimination
- Copy propagation
- Constant propagation

### 2.6 Code Generator

**Purpose:** Generate target code

**Location:** `src/codegen/`

**Key Classes:**
- `TargetGenerator`: Code emission
- `RegisterAllocator`: Register management

**Input:** Optimized TAC  
**Output:** Target code (assembly/VM code)

**Design Decisions:**
- Stack-based VM code (initial target)
- Simple register allocation
- Platform-independent intermediate form

## 3. Data Flow

### 3.1 Token Flow

```
Source Code
     │
     ▼
┌─────────┐
│ Lexer   │
└─────────┘
     │
     ▼
[Token List]
│
├─ Token { type: INT, value: "int", line: 1, col: 1 }
├─ Token { type: IDENTIFIER, value: "main", line: 1, col: 5 }
├─ Token { type: LEFT_PAREN, value: "(", line: 1, col: 9 }
└─ ...
```

### 3.2 AST Flow

```
Token Stream
     │
     ▼
┌─────────┐
│ Parser  │
└─────────┘
     │
     ▼
Program
  ├─ Declarations[]
  │    └─ VariableDeclaration { type: "int", name: "x" }
  └─ Functions[]
       └─ FunctionDeclaration
            ├─ name: "main"
            ├─ returnType: "int"
            ├─ parameters: []
            └─ body: Block
                 └─ statements[]
```

### 3.3 Symbol Table Flow

```
AST
 │
 ▼
┌──────────────┐
│  Semantic    │
│  Analyzer    │
└──────────────┘
 │
 ▼
Symbol Table
┌────────────────────────────────┐
│ Scope 0 (Global)               │
│  ├─ main: { type: function }   │
│  └─ add: { type: function }    │
├────────────────────────────────┤
│ Scope 1 (main)                 │
│  ├─ x: { type: int }           │
│  └─ y: { type: int }           │
└────────────────────────────────┘
```

### 3.4 IR Flow

```
AST
 │
 ▼
┌──────────────┐
│ IR Generator │
└──────────────┘
 │
 ▼
TAC Instructions
┌────────────────────┐
│ t1 = a + b         │
│ t2 = t1 * c        │
│ x = t2             │
│ if t1 < 0 goto L1  │
│ ...                │
└────────────────────┘
```

## 4. Design Patterns

### 4.1 Visitor Pattern

**Used in:** AST traversal, semantic analysis, code generation

```python
class ASTVisitor(ABC):
    @abstractmethod
    def visit_program(self, node: Program): pass
    
    @abstractmethod
    def visit_expression(self, node: Expression): pass
    # ... other visit methods

class SemanticAnalyzer(ASTVisitor):
    def visit_program(self, node: Program):
        # Perform semantic analysis
        pass
```

**Benefits:**
- Separation of concerns
- Easy to add new operations
- Type-safe traversal

### 4.2 Factory Pattern

**Used in:** AST node creation

```python
class ASTFactory:
    @staticmethod
    def create_binary_expr(left, op, right):
        return BinaryExpression(left, op, right)
```

### 4.3 Strategy Pattern

**Used in:** Optimization passes

```python
class OptimizationStrategy(ABC):
    @abstractmethod
    def optimize(self, ir): pass

class ConstantFolding(OptimizationStrategy):
    def optimize(self, ir):
        # Perform constant folding
        pass
```

### 4.4 Builder Pattern

**Used in:** IR construction

```python
class IRBuilder:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
    
    def add_instruction(self, inst):
        self.instructions.append(inst)
    
    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
```

## 5. Interface Specifications

### 5.1 Lexer Interface

```python
def tokenize(source_code: str, filename: str = "<stdin>") -> List[Token]:
    """
    Tokenize source code.
    
    Args:
        source_code: Source code string
        filename: Source file name (for error reporting)
        
    Returns:
        List of tokens
        
    Raises:
        LexerError: On tokenization failure
    """
```

### 5.2 Parser Interface

```python
def parse(tokens: List[Token]) -> Program:
    """
    Parse tokens into AST.
    
    Args:
        tokens: Token list from lexer
        
    Returns:
        Program AST node
        
    Raises:
        ParserError: On parsing failure
    """
```

### 5.3 Semantic Analyzer Interface

```python
def analyze(ast: Program) -> Tuple[Program, SymbolTable]:
    """
    Perform semantic analysis.
    
    Args:
        ast: Abstract Syntax Tree
        
    Returns:
        Tuple of (annotated AST, symbol table)
        
    Raises:
        SemanticError: On semantic violation
    """
```

### 5.4 IR Generator Interface

```python
def generate_ir(ast: Program, symbol_table: SymbolTable) -> List[TACInstruction]:
    """
    Generate intermediate representation.
    
    Args:
        ast: Annotated AST
        symbol_table: Symbol table
        
    Returns:
        List of TAC instructions
    """
```

## 6. Directory Structure

```
minlang-compiler/
├── src/                       # Source code
│   ├── lexer/                # Lexical analyzer
│   │   ├── __init__.py
│   │   ├── tokenizer.py      # Main tokenizer
│   │   └── token_types.py    # Token definitions
│   ├── parser/               # Syntax analyzer
│   │   ├── __init__.py
│   │   ├── parser.py         # Parser implementation
│   │   └── ast_nodes.py      # AST node classes
│   ├── semantic/             # Semantic analyzer
│   │   ├── __init__.py
│   │   ├── analyzer.py       # Type checker
│   │   └── symbol_table.py   # Symbol table
│   ├── codegen/              # Code generation
│   │   ├── __init__.py
│   │   ├── ir_generator.py   # IR generation
│   │   ├── optimizer.py      # Optimizations
│   │   └── target_generator.py # Code emission
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── error_handler.py  # Error management
│       └── logger.py         # Logging
├── tests/                    # Test suite
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_codegen.py
│   └── fixtures/             # Test data
├── examples/                 # Example programs
│   ├── hello_world.min
│   ├── calculator.min
│   └── fibonacci.min
├── docs/                     # Documentation
│   ├── DETAILED_DESCRIPTION.md
│   ├── GRAMMAR_SPECIFICATION.md
│   ├── API_DOCUMENTATION.md
│   └── USER_GUIDE.md
├── diagrams/                 # Architecture diagrams
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
├── setup.py                  # Package config
├── README.md                 # Project README
├── CONTRIBUTING.md           # Contribution guide
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## 7. Extensibility

### 7.1 Adding New Token Types

1. Add to `TokenType` enum
2. Update keyword/operator maps
3. Add tokenization logic
4. Add tests

### 7.2 Adding New AST Nodes

1. Create node class inheriting `ASTNode`
2. Add visitor method to `ASTVisitor`
3. Update parser to construct node
4. Add tests

### 7.3 Adding New Optimizations

1. Create optimization class
2. Implement optimization logic
3. Register with optimizer
4. Add tests

### 7.4 Adding New Target Platforms

1. Create target generator class
2. Implement code emission
3. Register with code generator
4. Add tests

## 8. Error Handling Strategy

### 8.1 Error Hierarchy

```
CompilerError
├── LexerError
│   ├── InvalidCharacterError
│   ├── UnterminatedStringError
│   └── InvalidNumberError
├── ParserError
│   ├── SyntaxError
│   └── UnexpectedTokenError
├── SemanticError
│   ├── TypeMismatchError
│   ├── UndeclaredVariableError
│   └── DuplicateDeclarationError
└── CodegenError
    └── ...
```

### 8.2 Error Recovery

- **Lexer:** Skip invalid character, continue
- **Parser:** Synchronize on statement boundaries
- **Semantic:** Continue checking after error
- **Codegen:** Fail fast on errors

## 9. Performance Considerations

### 9.1 Time Complexity

- **Lexer:** O(n) where n = source length
- **Parser:** O(n) where n = token count
- **Semantic:** O(n) where n = AST nodes
- **IR Gen:** O(n) where n = AST nodes
- **Optimization:** Varies by pass
- **Codegen:** O(n) where n = IR instructions

### 9.2 Space Complexity

- **Token storage:** O(n) tokens
- **AST storage:** O(n) nodes
- **Symbol table:** O(s) symbols
- **IR storage:** O(i) instructions

### 9.3 Optimization Opportunities

- Lazy evaluation
- Caching frequently accessed data
- Pool allocation for temporaries
- Incremental compilation

## 10. Testing Architecture

### 10.1 Test Levels

1. **Unit Tests:** Test individual components
2. **Integration Tests:** Test component interaction
3. **System Tests:** Test entire compilation
4. **Regression Tests:** Prevent regressions

### 10.2 Test Organization

```
tests/
├── unit/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── ...
├── integration/
│   ├── test_lexer_parser.py
│   └── ...
├── system/
│   ├── test_end_to_end.py
│   └── ...
└── fixtures/
    └── sample_programs/
```

## 11. Deployment

### 11.1 Package Distribution

- PyPI package: `pip install minlang-compiler`
- Docker container
- Binary distribution

### 11.2 Installation Methods

1. **Development:**
   ```bash
   git clone repo
   pip install -e .
   ```

2. **Production:**
   ```bash
   pip install minlang-compiler
   ```

## 12. Future Architecture Enhancements

- Plugin system for extensions
- Parallel compilation
- Incremental compilation
- JIT compilation support
- LLVM backend integration
- Language server protocol

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Maintainers:** MinLang Compiler Team
