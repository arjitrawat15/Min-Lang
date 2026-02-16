# MinLang Compiler - Complete File Structure

## Overview

This document describes the complete file structure of the MinLang Compiler project, including the purpose of each file and directory.

## Directory Tree

```
minlang-compiler/
├── README.md                      # Main project README with quick start guide
├── LICENSE                        # MIT License file
├── ARCHITECTURE.md               # Architecture documentation
├── CONTRIBUTING.md               # Contribution guidelines
├── .gitignore                    # Git ignore rules
├── setup.py                      # Package installation configuration
├── requirements.txt              # Python dependencies
├── main.py                       # Main entry point for the compiler
│
├── src/                          # Source code directory
│   ├── lexer/                    # Lexical analyzer package
│   │   ├── __init__.py          # Package initialization
│   │   ├── tokenizer.py         # Main tokenizer implementation (COMPLETE)
│   │   └── token_types.py       # Token type definitions (COMPLETE)
│   │
│   ├── parser/                   # Syntax analyzer package
│   │   ├── __init__.py          # Package initialization
│   │   ├── parser.py            # Recursive descent parser (30% COMPLETE)
│   │   └── ast_nodes.py         # AST node class definitions (COMPLETE)
│   │
│   ├── semantic/                 # Semantic analyzer package (TODO)
│   │   ├── __init__.py          # Package initialization (placeholder)
│   │   ├── analyzer.py          # Type checker and semantic validator (TODO)
│   │   └── symbol_table.py      # Symbol table implementation (TODO)
│   │
│   ├── codegen/                  # Code generation package (TODO)
│   │   ├── __init__.py          # Package initialization (placeholder)
│   │   ├── ir_generator.py      # IR (TAC) generation (TODO)
│   │   ├── optimizer.py         # Optimization passes (TODO)
│   │   └── target_generator.py  # Target code emission (TODO)
│   │
│   └── utils/                    # Utility modules
│       ├── __init__.py          # Package initialization
│       ├── error_handler.py     # Error reporting and management (COMPLETE)
│       └── logger.py            # Logging utilities (TODO)
│
├── tests/                        # Test suite directory
│   ├── test_lexer.py            # Lexer unit tests (COMPLETE - 50+ tests)
│   ├── test_parser.py           # Parser unit tests (PARTIAL - 40+ tests)
│   ├── test_semantic.py         # Semantic analyzer tests (TODO)
│   ├── test_codegen.py          # Code generation tests (TODO)
│   └── fixtures/                # Test fixtures and data
│       └── sample_programs/     # Sample MinLang programs for testing
│
├── examples/                     # Example MinLang programs
│   ├── hello_world.min          # Simple I/O example
│   ├── calculator.min           # Arithmetic and functions
│   └── fibonacci.min            # Loops and variables
│
├── docs/                         # Documentation directory
│   ├── DETAILED_DESCRIPTION.md  # Comprehensive project description
│   ├── GITHUB_WORKFLOW.md       # GitHub workflow and branching guide
│   ├── GRAMMAR_SPECIFICATION.md # Formal grammar (TODO)
│   ├── API_DOCUMENTATION.md     # API reference (TODO)
│   └── USER_GUIDE.md            # User guide (TODO)
│
└── diagrams/                     # Architecture and design diagrams
    ├── architecture.svg         # System architecture diagram
    └── compilation_flow.svg     # Compilation flow diagram (TODO)
```

## File Details

### Root Directory Files

#### README.md (11 KB)
**Purpose:** Main project documentation and quick start guide  
**Status:** ✅ Complete  
**Contents:**
- Project overview
- Features
- Installation instructions
- Usage examples
- Project structure
- Development guide
- Team information

#### LICENSE (1 KB)
**Purpose:** MIT License for the project  
**Status:** ✅ Complete

#### ARCHITECTURE.md (15 KB)
**Purpose:** Detailed architecture documentation  
**Status:** ✅ Complete  
**Contents:**
- System architecture
- Component details
- Data flow
- Design patterns
- Interface specifications

#### CONTRIBUTING.md (8 KB)
**Purpose:** Guidelines for contributing to the project  
**Status:** ✅ Complete  
**Contents:**
- Development workflow
- Code style guidelines
- Pull request process
- Testing requirements

#### .gitignore (1 KB)
**Purpose:** Specify files to ignore in version control  
**Status:** ✅ Complete

#### setup.py (2 KB)
**Purpose:** Package configuration for installation  
**Status:** ✅ Complete  
**Features:**
- Package metadata
- Dependencies
- Entry points
- Classifiers

#### requirements.txt (< 1 KB)
**Purpose:** Python package dependencies  
**Status:** ✅ Complete

#### main.py (6 KB)
**Purpose:** Main entry point for compiler  
**Status:** ✅ Complete (for current features)  
**Features:**
- Command-line interface
- Compilation orchestration
- Verbose output
- Error handling

---

### Source Code Directory (`src/`)

#### Lexer Package (`src/lexer/`)

##### tokenizer.py (8 KB)
**Status:** ✅ 100% Complete  
**Lines of Code:** ~500  
**Test Coverage:** 100%

**Classes:**
- `Tokenizer`: Main tokenization class
- `LexerError`: Custom exception

**Key Methods:**
- `tokenize()`: Main tokenization function
- `read_number()`: Parse numeric literals
- `read_identifier()`: Parse identifiers/keywords
- `read_char_literal()`: Parse character literals
- `read_string_literal()`: Parse string literals
- `skip_comment()`: Handle comments

**Features:**
- Complete MinLang tokenization
- Error detection and reporting
- Line/column tracking
- Comment support
- Escape sequences

##### token_types.py (4 KB)
**Status:** ✅ 100% Complete  
**Lines of Code:** ~200

**Contents:**
- `TokenType` enum: All token types
- `Token` dataclass: Token structure
- `KEYWORDS` dict: Keyword mappings
- `OPERATORS` dict: Operator mappings
- `DELIMITERS` dict: Delimiter mappings

---

#### Parser Package (`src/parser/`)

##### parser.py (15 KB)
**Status:** 🔄 30% Complete  
**Lines of Code:** ~600  
**Test Coverage:** ~60%

**Classes:**
- `Parser`: Recursive descent parser
- `ParserError`: Custom exception

**Implemented Methods:**
- `parse()`: Entry point
- `parse_expression()`: Expression parsing
- `parse_statement()`: Basic statements
- `parse_declaration()`: Variable declarations
- `parse_function_declaration()`: Function structure

**TODO Methods:**
- `parse_if_statement()`: If-else parsing
- `parse_while_statement()`: While loop parsing
- `parse_for_statement()`: For loop parsing
- Complete error recovery

**Features:**
- Expression parsing with precedence
- Basic statement parsing
- Function declarations
- Assignment statements

##### ast_nodes.py (12 KB)
**Status:** ✅ 100% Complete  
**Lines of Code:** ~500

**Classes:**
- `ASTNode`: Base class
- `Program`: Root node
- `Declaration`: Declaration base
- `VariableDeclaration`: Variable declarations
- `FunctionDeclaration`: Function declarations
- `Statement`: Statement base
- `Expression`: Expression base
- Multiple expression types
- `ASTVisitor`: Visitor interface
- `ASTPrinter`: Debug printer

---

#### Semantic Package (`src/semantic/`)

##### analyzer.py
**Status:** ⏳ TODO  
**Estimated Lines:** ~600  

**Planned Classes:**
- `SemanticAnalyzer`: Main analyzer
- `SemanticError`: Custom exception

**Planned Features:**
- Type checking
- Scope management
- Function validation
- Semantic error reporting

##### symbol_table.py
**Status:** ⏳ TODO  
**Estimated Lines:** ~400

**Planned Classes:**
- `SymbolTable`: Symbol management
- `Scope`: Scope representation
- `Symbol`: Symbol entry

---

#### Codegen Package (`src/codegen/`)

##### ir_generator.py
**Status:** ⏳ TODO  
**Estimated Lines:** ~700

**Planned Classes:**
- `IRGenerator`: TAC generation
- `TACInstruction`: IR instruction

##### optimizer.py
**Status:** ⏳ TODO  
**Estimated Lines:** ~500

**Planned Classes:**
- `Optimizer`: Optimization coordinator
- Various optimization passes

##### target_generator.py
**Status:** ⏳ TODO  
**Estimated Lines:** ~600

**Planned Classes:**
- `TargetGenerator`: Code emission
- `RegisterAllocator`: Register management

---

#### Utils Package (`src/utils/`)

##### error_handler.py (3 KB)
**Status:** ✅ Complete  
**Lines of Code:** ~120

**Classes:**
- `CompilerError`: Base error class
- `ErrorHandler`: Centralized error management

**Features:**
- Error reporting
- Warning tracking
- Formatted output
- Error summary

---

### Tests Directory (`tests/`)

#### test_lexer.py (8 KB)
**Status:** ✅ Complete  
**Test Count:** 50+  
**Coverage:** 100%

**Test Classes:**
- `TestBasicTokens`: Basic token recognition
- `TestComplexTokenization`: Complex code
- `TestComments`: Comment handling
- `TestErrors`: Error detection
- `TestLineTracking`: Position tracking

#### test_parser.py (7 KB)
**Status:** 🔄 Partial  
**Test Count:** 40+  
**Coverage:** ~60%

**Test Classes:**
- `TestBasicParsing`: Basic parsing
- `TestFunctions`: Function parsing
- `TestStatements`: Statement parsing
- `TestExpressions`: Expression parsing
- `TestErrors`: Error detection

---

### Examples Directory (`examples/`)

#### hello_world.min (< 1 KB)
**Purpose:** Basic I/O demonstration  
**Features:** Variable declaration, read, print

#### calculator.min (1 KB)
**Purpose:** Functions and arithmetic  
**Features:** Multiple functions, calculations

#### fibonacci.min (1 KB)
**Purpose:** Loops and variables  
**Features:** Loop demonstration (when complete)

---

### Documentation Directory (`docs/`)

#### DETAILED_DESCRIPTION.md (25 KB)
**Status:** ✅ Complete  
**Contents:**
- Project overview
- Language specification
- Architecture details
- Implementation details
- Team structure
- Development roadmap
- Educational value

#### GITHUB_WORKFLOW.md (12 KB)
**Status:** ✅ Complete  
**Contents:**
- Repository setup
- Branching strategy
- Team workflow
- Pull request process
- Best practices

---

### Diagrams Directory (`diagrams/`)

#### architecture.svg (5 KB)
**Status:** ✅ Complete  
**Type:** SVG diagram  
**Contents:** Visual system architecture

---

## Statistics Summary

### Completed Components
- **Lexer:** 100% (500 LOC)
- **Token Types:** 100% (200 LOC)
- **AST Nodes:** 100% (500 LOC)
- **Parser:** 30% (600 LOC)
- **Error Handler:** 100% (120 LOC)
- **Tests:** Lexer 100%, Parser 60%
- **Documentation:** Core docs 100%

### Pending Components
- **Semantic Analyzer:** 0% (~600 LOC planned)
- **Symbol Table:** 0% (~400 LOC planned)
- **IR Generator:** 0% (~700 LOC planned)
- **Optimizer:** 0% (~500 LOC planned)
- **Target Generator:** 0% (~600 LOC planned)

### Overall Statistics
- **Total Lines Implemented:** ~2,000
- **Total Lines Planned:** ~6,000
- **Completion:** ~30%
- **Test Coverage:** ~85% (for implemented components)
- **Documentation:** ~80% complete

---

## Navigation Guide

### For New Contributors

**Start Here:**
1. `README.md` - Project overview
2. `CONTRIBUTING.md` - Contribution guidelines
3. `docs/GITHUB_WORKFLOW.md` - Git workflow
4. `ARCHITECTURE.md` - System design

**For Coding:**
1. `src/lexer/` - Study completed lexer
2. `src/parser/` - See partial parser
3. `tests/` - Understand testing approach
4. Your assigned component

### For Understanding the Code

**Compilation Flow:**
1. `main.py` - Entry point
2. `src/lexer/tokenizer.py` - First phase
3. `src/parser/parser.py` - Second phase
4. `src/parser/ast_nodes.py` - AST structure

**Testing Flow:**
1. `tests/test_lexer.py` - Lexer tests
2. `tests/test_parser.py` - Parser tests
3. `examples/` - Test programs

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**Maintainers:** MinLang Compiler Team
