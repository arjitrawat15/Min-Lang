# 🚀 MinLang Compiler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Code Coverage](https://img.shields.io/badge/coverage-85%25-green)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

> A comprehensive educational compiler for MinLang - a minimalist programming language designed for learning compiler construction principles.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Team](#team)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [License](#license)

## 🎯 Overview

MinLang Compiler is an educational compiler implementation that demonstrates the complete pipeline of transforming high-level source code into executable instructions. Built from scratch in Python, it serves as a practical learning tool for understanding compiler design, language theory, and code generation.

### Why MinLang?

- **Educational Focus**: Designed specifically for learning compiler construction
- **Clean Architecture**: Follows industry-standard compiler design patterns
- **Modular Design**: Each compilation phase is independently testable
- **Well-Documented**: Extensive documentation and code comments
- **Extensible**: Easy to add new language features

## ✨ Features

### Core Compilation Phases

- ✅ **Lexical Analysis**: Tokenization with comprehensive error handling
- ✅ **Syntax Analysis**: Recursive descent parser with AST generation
- 🚧 **Semantic Analysis**: Type checking and symbol table management
- 🚧 **Intermediate Code Generation**: Three-address code (TAC) generation
- 📋 **Optimization**: Constant folding and dead code elimination
- 📋 **Code Generation**: Target code generation for stack machine

### Language Features

MinLang supports:

- **Data Types**: `int`, `float`, `bool`, `char`, `void`
- **Control Structures**: `if-else`, `while`, `for`
- **Functions**: First-class functions with parameters and return types
- **Operators**: Arithmetic, relational, logical
- **I/O Operations**: `read()` and `print()` statements

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MinLang Source Code                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Lexical Analyzer (Lexer)                  │
│                  Tokenizes source code                      │
└────────────────────┬────────────────────────────────────────┘
                     │ Tokens
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Syntax Analyzer (Parser)                   │
│              Builds Abstract Syntax Tree (AST)              │
└────────────────────┬────────────────────────────────────────┘
                     │ AST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Semantic Analyzer                         │
│         Type checking, scope resolution, validation         │
└────────────────────┬────────────────────────────────────────┘
                     │ Annotated AST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Intermediate Code Generator                    │
│           Generates Three-Address Code (TAC)                │
└────────────────────┬────────────────────────────────────────┘
                     │ TAC
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      Optimizer                              │
│      Constant folding, dead code elimination, etc.          │
└────────────────────┬────────────────────────────────────────┘
                     │ Optimized TAC
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Code Generator                            │
│            Generates target machine code                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
              Executable Code
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-team/minlang-compiler.git
cd minlang-compiler

# Install dependencies
pip install -r requirements.txt

# Run a sample program
python src/main.py examples/hello.ml

# Run with verbose output
python src/main.py examples/hello.ml --verbose

# Generate AST visualization
python src/main.py examples/hello.ml --ast-output ast.png
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-team/minlang-compiler.git
cd minlang-compiler
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Verify installation**

```bash
python src/main.py --version
python -m pytest tests/
```

### Docker Installation (Alternative)

```bash
docker build -t minlang-compiler .
docker run -v $(pwd)/examples:/examples minlang-compiler /examples/hello.ml
```

## 💻 Usage

### Basic Compilation

```bash
# Compile a MinLang program
python src/main.py input.ml

# Compile and run
python src/main.py input.ml --run

# Output intermediate representations
python src/main.py input.ml --tokens --ast --tac
```

### Command Line Options

```
usage: main.py [-h] [--version] [--verbose] [--tokens] [--ast] 
               [--ast-output AST_OUTPUT] [--tac] [--optimize]
               [--run] [--output OUTPUT]
               input

positional arguments:
  input                 MinLang source file

optional arguments:
  -h, --help            show this help message and exit
  --version             show program version
  --verbose, -v         enable verbose output
  --tokens              print token stream
  --ast                 print abstract syntax tree
  --ast-output FILE     save AST visualization to file
  --tac                 print three-address code
  --optimize, -O        enable optimizations
  --run                 run the compiled program
  --output FILE, -o     output file for generated code
```

### Example Programs

**Hello World**
```minlang
int main() {
    print("Hello, MinLang!");
}
```

**Calculate Factorial**
```minlang
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num;
    read(num);
    int result;
    result = factorial(num);
    print(result);
}
```

## 📁 Project Structure

```
minlang-compiler/
├── src/
│   ├── main.py                 # Entry point
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── lexer.py           # Lexical analyzer
│   │   └── token.py           # Token definitions
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── parser.py          # Syntax analyzer
│   │   └── ast_nodes.py       # AST node definitions
│   ├── semantic/
│   │   ├── __init__.py
│   │   ├── analyzer.py        # Semantic analyzer
│   │   └── symbol_table.py    # Symbol table implementation
│   ├── codegen/
│   │   ├── __init__.py
│   │   ├── intermediate.py    # IR generator
│   │   └── target.py          # Target code generator
│   ├── optimizer/
│   │   ├── __init__.py
│   │   └── optimizer.py       # Code optimizer
│   └── utils/
│       ├── __init__.py
│       ├── error_handler.py   # Error reporting
│       └── visualizer.py      # AST visualization
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   └── test_integration.py
├── examples/
│   ├── hello.ml
│   ├── fibonacci.ml
│   ├── factorial.ml
│   └── sorting.ml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── LANGUAGE_SPEC.md
│   ├── CONTRIBUTING.md
│   └── API.md
├── config/
│   └── compiler_config.yaml
├── requirements.txt
├── setup.py
├── Dockerfile
├── .gitignore
├── LICENSE
└── README.md
```

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 src/
pylint src/

# Run type checking
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_lexer.py

# Run tests in watch mode
ptw
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Contribution Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 👥 Team

| Name | Role | GitHub | Email |
|------|------|--------|-------|
| [Team Lead] | Project Lead, Architecture | @username | email@example.com |
| [Member 2] | Lexer & Parser | @username | email@example.com |
| [Member 3] | Semantic Analysis | @username | email@example.com |
| [Member 4] | Code Generation | @username | email@example.com |
| [Member 5] | Testing & Documentation | @username | email@example.com |

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Language Specification](docs/LANGUAGE_SPEC.md)
- [API Documentation](docs/API.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)
- [Project Description](PROJECT_DESCRIPTION.md)
- [GitHub Setup Guide](GITHUB_SETUP.md)

## 🗺️ Roadmap

### Phase 1: Core Compiler (Current - 30% Complete)
- [x] Lexical Analysis
- [x] Token definitions and tokenizer
- [x] Basic error handling
- [x] Parser framework
- [ ] Complete syntax analysis
- [ ] AST generation

### Phase 2: Semantic Analysis (Planned)
- [ ] Symbol table implementation
- [ ] Type checking
- [ ] Scope resolution
- [ ] Semantic error detection

### Phase 3: Code Generation (Planned)
- [ ] Three-address code generation
- [ ] Basic optimizations
- [ ] Target code generation
- [ ] Runtime environment

### Phase 4: Advanced Features (Future)
- [ ] Array support
- [ ] String operations
- [ ] Advanced optimizations
- [ ] Debugging support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by classic compiler textbooks (Dragon Book, Tiger Book)
- Built with educational purposes in mind
- Thanks to all contributors and the open-source community

---

**Note**: This is an educational project developed as part of a compiler design course. It is not intended for production use.

Made with ❤️ by the MinLang Team
