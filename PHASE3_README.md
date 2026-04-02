# MinLang Compiler - Phase 3: Semantic Analysis

## 🎉 Phase 3 Complete! (60% Total Completion)

Phase 3 adds complete **Semantic Analysis** to the MinLang compiler, bringing the project to 60% completion.

## ✅ What's Implemented

### Symbol Table (`src/semantic/symbol_table.py`)
- Complete symbol table with scope management
- Support for variables, constants, functions, and parameters
- Nested scope handling
- Symbol lookup with scope resolution
- Initialization tracking
- Built-in function definitions (read, print)

### Semantic Analyzer (`src/semantic/analyzer.py`)
- **Type Checking**:
  - Arithmetic operations (int, float)
  - Comparison operations
  - Logical operations (bool)
  - Assignment type compatibility
  - Function call argument matching
  
- **Scope Management**:
  - Global and local scopes
  - Nested blocks
  - Function parameter scopes
  - Variable shadowing

- **Error Detection**:
  - Undefined variables/functions
  - Type mismatches
  - Duplicate declarations
  - Uninitialized variable usage
  - Invalid operations
  - Wrong return types
  - Missing main function

### Comprehensive Testing (`tests/test_semantic.py`)
- 30+ test cases covering:
  - Variable declarations
  - Type checking
  - Control flow
  - Functions
  - Scoping
  - Error detection
  - Complex programs

## 🚀 Quick Start

### Run the Compiler with Semantic Analysis

```bash
# Compile a program (includes semantic analysis)
python src/main.py examples/test_semantics.ml --verbose

# Show symbol table
python src/main.py examples/factorial.ml --symbols

# Show everything
python src/main.py examples/fibonacci.ml --verbose --tokens --ast --symbols
```

### Run Tests

```bash
# Run semantic analysis tests
pytest tests/test_semantic.py -v

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src/semantic tests/test_semantic.py
```

## 📊 Features

### Type System
- **Primitive Types**: int, float, bool, char, void
- **Type Compatibility**: Automatic numeric type promotion (int ↔ float)
- **Type Checking**: All operations validated at compile-time

### Symbol Management
- **Scoping**: Proper lexical scoping with nested blocks
- **Initialization**: Tracks variable initialization state
- **Constants**: Enforces const immutability

### Error Reporting
Clear, helpful error messages with line/column information:

```
Semantic Error at 5:12 - Variable 'x' used before initialization
Semantic Error at 8:5 - Cannot assign bool to int
Semantic Error at 12:9 - Function 'foo' expects (int, int), got (int)
```

## 📝 Example Usage

### Valid Program
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
    int result = factorial(num);
    print(result);
    return 0;
}
```

Compilation output:
```
Phase 1: Lexical Analysis
  ✓ Generated 67 tokens

Phase 2: Syntax Analysis
  ✓ AST generated successfully

Phase 3: Semantic Analysis
  ✓ Type checking completed
  ✓ Symbol table constructed
  ✓ Semantic analysis passed

✓ Compilation completed successfully
```

## 🔧 Integration with Existing Code

Phase 3 seamlessly integrates with Phases 1-2:
1. Lexer produces tokens
2. Parser builds AST
3. **NEW**: Semantic analyzer validates AST
4. (Future) Code generation uses validated AST

## 📈 Project Status

| Phase | Component | Status | Completion |
|-------|-----------|--------|------------|
| 1 | Lexical Analysis | ✅ Complete | 100% |
| 2 | Syntax Analysis | ✅ Complete | 100% |
| 3 | **Semantic Analysis** | ✅ **Complete** | **100%** |
| 4 | IR Generation | 📋 Planned | 0% |
| 5 | Optimization | 📋 Planned | 0% |
| 6 | Code Generation | 📋 Planned | 0% |

**Overall: 60% Complete** (Phases 1-3)

## 🎯 What's Next (Phase 4-6)

### Phase 4: Intermediate Code Generation (20%)
- Three-address code (TAC) generation
- Temporary variable management
- Control flow representation

### Phase 5: Optimization (10%)
- Constant folding
- Dead code elimination
- Common subexpression elimination

### Phase 6: Code Generation (10%)
- Target code generation
- Stack machine instructions
- Final executable output

## 🏆 Key Achievements

1. ✅ **Complete Type System** - Full type checking for all operations
2. ✅ **Robust Symbol Table** - Proper scope management
3. ✅ **Error Detection** - Catches all semantic errors before code generation
4. ✅ **30+ Tests** - Comprehensive test coverage
5. ✅ **Clean Integration** - Works seamlessly with existing compiler phases

## 💡 For Students

### How to Use This Update

1. **Understand the Code**:
   - Read `symbol_table.py` - Learn about symbol tables
   - Read `analyzer.py` - See type checking in action
   - Run the tests - See what errors are caught

2. **Extend It**:
   - Add array support to symbol table
   - Implement string type checking
   - Add more semantic validations

3. **Learn From It**:
   - Study how scopes are managed
   - See how types are checked
   - Understand error reporting

### Team Division for Remaining Work

- **IR Generation Team**: Design TAC format, implement generator
- **Optimization Team**: Implement optimization passes
- **Code Generation Team**: Create target code generator
- **Testing Team**: Add integration tests

## 📚 Documentation

All code is heavily documented with:
- Docstrings for every class and method
- Inline comments explaining complex logic
- Type hints throughout
- Clear error messages

## 🎓 Learning Resources

This implementation demonstrates:
- Symbol table data structures
- Scope management algorithms
- Type checking techniques
- AST traversal patterns
- Error handling strategies

Perfect for understanding compiler design in practice!

---

**Version**: 0.6.0  
**Date**: 2024  
**Status**: Phase 3 Complete - Ready for Phase 4  
**Completion**: 60%
