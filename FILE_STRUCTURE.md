# MinLang Compiler - Complete File Structure

## Project Tree

```
minlang-compiler/
├── README.md                           # Main project documentation
├── PROJECT_DESCRIPTION.md              # Detailed project description
├── GITHUB_SETUP.md                     # Git and GitHub setup guide
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
├── requirements-dev.txt                # Development dependencies
├── setup.py                            # Package setup configuration
├── pytest.ini                          # Pytest configuration
│
├── src/                                # Source code directory
│   ├── main.py                         # CLI entry point (✅ 30% Complete)
│   │
│   ├── lexer/                          # Lexical analysis module (✅ Complete)
│   │   ├── __init__.py                 # Package initialization
│   │   ├── token.py                    # Token class and types
│   │   └── lexer.py                    # Lexer implementation
│   │
│   ├── parser/                         # Syntax analysis module (✅ Complete)
│   │   ├── __init__.py                 # Package initialization
│   │   ├── ast_nodes.py                # AST node definitions
│   │   └── parser.py                   # Recursive descent parser
│   │
│   ├── semantic/                       # Semantic analysis module (📋 Planned)
│   │   ├── __init__.py                 # Package initialization
│   │   ├── symbol_table.py             # Symbol table implementation
│   │   └── analyzer.py                 # Semantic analyzer
│   │
│   ├── codegen/                        # Code generation module (📋 Planned)
│   │   ├── __init__.py                 # Package initialization
│   │   ├── intermediate.py             # IR generator (TAC)
│   │   └── target.py                   # Target code generator
│   │
│   ├── optimizer/                      # Optimization module (📋 Planned)
│   │   ├── __init__.py                 # Package initialization
│   │   └── optimizer.py                # Optimization passes
│   │
│   └── utils/                          # Utility modules (🚧 Partial)
│       ├── __init__.py                 # Package initialization
│       ├── error_handler.py            # Error reporting utilities
│       └── visualizer.py               # AST visualization tools
│
├── tests/                              # Test suite
│   ├── __init__.py                     # Test package initialization
│   ├── test_lexer.py                   # Lexer unit tests (✅ Complete)
│   ├── test_parser.py                  # Parser unit tests (📋 Planned)
│   ├── test_semantic.py                # Semantic analysis tests (📋 Planned)
│   ├── test_codegen.py                 # Code generation tests (📋 Planned)
│   └── test_integration.py             # Integration tests (📋 Planned)
│
├── examples/                           # Example MinLang programs
│   ├── hello.ml                        # Hello world program
│   ├── fibonacci.ml                    # Fibonacci sequence
│   ├── factorial.ml                    # Factorial calculation
│   └── simple_calc.ml                  # Simple calculator
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                 # System architecture (✅ Complete)
│   ├── LANGUAGE_SPEC.md                # Language specification (📋 Planned)
│   ├── API.md                          # API documentation (📋 Planned)
│   ├── CONTRIBUTING.md                 # Contribution guidelines (📋 Planned)
│   └── TEAM_GUIDE.md                   # Team workflow guide (📋 Planned)
│
├── config/                             # Configuration files
│   └── compiler_config.yaml            # Compiler configuration (📋 Planned)
│
└── scripts/                            # Utility scripts (📋 Planned)
    ├── setup.sh                        # Setup script
    └── run_tests.sh                    # Test runner script
```

## File Descriptions

### Root Level Files

#### README.md
- **Purpose**: Main project documentation and quick start guide
- **Status**: ✅ Complete
- **Contents**:
  - Project overview
  - Installation instructions
  - Usage examples
  - Contributing guidelines
  - Team information

#### PROJECT_DESCRIPTION.md
- **Purpose**: Detailed project description and specifications
- **Status**: ✅ Complete
- **Contents**:
  - Comprehensive project scope
  - Technical specifications
  - Implementation phases
  - Learning outcomes

#### GITHUB_SETUP.md
- **Purpose**: Git and GitHub workflow guide
- **Status**: ✅ Complete
- **Contents**:
  - Repository setup instructions
  - Branching strategy
  - Pull request workflow
  - Team collaboration guidelines

#### LICENSE
- **Purpose**: MIT License for open-source distribution
- **Status**: ✅ Complete

#### .gitignore
- **Purpose**: Specify files to ignore in version control
- **Status**: ✅ Complete
- **Includes**:
  - Python bytecode
  - Virtual environments
  - IDE files
  - Test coverage reports

#### requirements.txt
- **Purpose**: Production dependencies
- **Status**: ✅ Complete
- **Dependencies**:
  - pytest
  - colorama
  - pyyaml
  - graphviz

#### requirements-dev.txt
- **Purpose**: Development dependencies
- **Status**: ✅ Complete
- **Dependencies**:
  - flake8
  - pylint
  - black
  - mypy
  - pre-commit

#### setup.py
- **Purpose**: Package configuration for distribution
- **Status**: ✅ Complete

### Source Code (src/)

#### main.py
- **Purpose**: Command-line interface and entry point
- **Status**: ✅ Complete (30%)
- **Features**:
  - Argument parsing
  - File compilation
  - Token/AST output
  - Error handling

#### Lexer Module (src/lexer/)

##### token.py
- **Purpose**: Token definitions and enumerations
- **Status**: ✅ Complete
- **Contents**:
  - TokenType enum
  - Token class
  - Keyword mappings
  - Operator mappings

##### lexer.py
- **Purpose**: Lexical analyzer implementation
- **Status**: ✅ Complete
- **Features**:
  - Character scanning
  - Token recognition
  - Comment handling
  - Error detection

#### Parser Module (src/parser/)

##### ast_nodes.py
- **Purpose**: AST node class definitions
- **Status**: ✅ Complete
- **Contents**:
  - Base ASTNode class
  - Program node
  - Declaration nodes
  - Statement nodes
  - Expression nodes

##### parser.py
- **Purpose**: Recursive descent parser
- **Status**: ✅ Complete
- **Features**:
  - Grammar rule implementation
  - AST construction
  - Syntax error handling
  - Operator precedence

#### Semantic Module (src/semantic/)

##### symbol_table.py
- **Purpose**: Symbol table for tracking identifiers
- **Status**: 📋 Planned (Future work)
- **Will include**:
  - Scope management
  - Symbol insertion/lookup
  - Type information storage

##### analyzer.py
- **Purpose**: Semantic analysis and type checking
- **Status**: 📋 Planned (Future work)
- **Will include**:
  - Type checking
  - Scope resolution
  - Semantic validation

#### Code Generation Module (src/codegen/)

##### intermediate.py
- **Purpose**: Three-address code generation
- **Status**: 📋 Planned (Future work)
- **Will include**:
  - TAC instruction generation
  - Temporary variable management
  - Control flow handling

##### target.py
- **Purpose**: Target code generation
- **Status**: 📋 Planned (Future work)
- **Will include**:
  - Stack machine code generation
  - Instruction emission

#### Optimizer Module (src/optimizer/)

##### optimizer.py
- **Purpose**: Code optimization passes
- **Status**: 📋 Planned (Future work)
- **Will include**:
  - Constant folding
  - Dead code elimination
  - Common subexpression elimination

#### Utils Module (src/utils/)

##### error_handler.py
- **Purpose**: Unified error reporting
- **Status**: 🚧 Partial
- **Features**:
  - Error formatting
  - Stack traces
  - User-friendly messages

##### visualizer.py
- **Purpose**: AST visualization tools
- **Status**: 🚧 Partial
- **Features**:
  - Tree rendering
  - Graph generation
  - Pretty printing

### Tests (tests/)

#### test_lexer.py
- **Purpose**: Unit tests for lexer
- **Status**: ✅ Complete
- **Tests**:
  - Keyword recognition
  - Operator recognition
  - Number parsing
  - String handling
  - Error cases

#### test_parser.py
- **Purpose**: Unit tests for parser
- **Status**: 📋 Planned
- **Will test**:
  - Expression parsing
  - Statement parsing
  - AST generation

#### test_semantic.py
- **Purpose**: Unit tests for semantic analysis
- **Status**: 📋 Planned

#### test_codegen.py
- **Purpose**: Unit tests for code generation
- **Status**: 📋 Planned

#### test_integration.py
- **Purpose**: End-to-end integration tests
- **Status**: 📋 Planned

### Examples (examples/)

All example files demonstrate MinLang syntax and features:

- **hello.ml**: Basic program structure
- **fibonacci.ml**: Loops and arithmetic
- **factorial.ml**: Recursion
- **simple_calc.ml**: Functions and I/O

### Documentation (docs/)

#### ARCHITECTURE.md
- **Purpose**: System design and architecture
- **Status**: ✅ Complete
- **Contains**:
  - Component diagrams
  - Data flow diagrams
  - Class hierarchies
  - Module dependencies

#### LANGUAGE_SPEC.md
- **Purpose**: Formal language specification
- **Status**: 📋 Planned
- **Will include**:
  - Grammar definition
  - Type system
  - Semantics

#### API.md
- **Purpose**: API documentation for developers
- **Status**: 📋 Planned

## Implementation Status Summary

| Category | Status | Completion |
|----------|--------|------------|
| Project Setup | ✅ Complete | 100% |
| Documentation | ✅ Complete | 100% |
| Lexer | ✅ Complete | 100% |
| Parser | ✅ Complete | 100% |
| Semantic Analysis | 📋 Planned | 0% |
| Code Generation | 📋 Planned | 0% |
| Optimization | 📋 Planned | 0% |
| Tests | 🚧 Partial | 30% |
| Examples | ✅ Complete | 100% |

**Overall Project Completion: 30%**

## Key Implementation Notes

### What's Implemented (30%)

1. **Complete Lexer** (Phase 1)
   - All token types
   - Keyword recognition
   - Operator parsing
   - String/character literals
   - Comment handling
   - Error reporting

2. **Complete Parser** (Phase 2)
   - Recursive descent implementation
   - Full AST generation
   - All language constructs
   - Expression precedence
   - Error handling

3. **Project Infrastructure**
   - Git configuration
   - Testing framework
   - Documentation
   - Example programs
   - CLI interface

### What's Planned (70%)

1. **Semantic Analysis** (Phase 3)
   - Symbol table
   - Type checking
   - Scope resolution

2. **Code Generation** (Phase 4-6)
   - Intermediate representation
   - Optimization passes
   - Target code generation

3. **Advanced Features**
   - Better error messages
   - AST visualization
   - Debugging support

## Usage Instructions

### Running the Compiler

```bash
# Tokenize a file
python src/main.py examples/hello.ml --tokens

# Parse and show AST
python src/main.py examples/hello.ml --ast

# Verbose output
python src/main.py examples/hello.ml -v --tokens --ast
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run lexer tests only
pytest tests/test_lexer.py

# With coverage
pytest --cov=src tests/
```

## Future File Additions

As the project progresses to 100%, these files will be added:

- `src/semantic/symbol_table.py`
- `src/semantic/analyzer.py`
- `src/codegen/intermediate.py`
- `src/codegen/target.py`
- `src/optimizer/optimizer.py`
- `tests/test_parser.py`
- `tests/test_semantic.py`
- `tests/test_codegen.py`
- `tests/test_integration.py`
- `docs/LANGUAGE_SPEC.md`
- `docs/API.md`
- `docs/CONTRIBUTING.md`

## Notes for Team Members

- **Lexer Team**: Implementation complete, focus on testing edge cases
- **Parser Team**: Implementation complete, add more unit tests
- **Semantic Team**: Begin with symbol table design
- **CodeGen Team**: Study IR formats and start design
- **Testing Team**: Expand test coverage, add integration tests
- **Docs Team**: Keep documentation synchronized with code changes

---

**Last Updated**: [Current Date]  
**Project Status**: 30% Complete (Phase 1-2)  
**Next Milestone**: Semantic Analysis Implementation
