# MinLang Compiler - Phase 3 Iteration Notes

## Important Scope Decision for This Iteration
This update is intentionally **not the full compiler**.

This branch now completes and verifies only the **next phase** after parsing:

1. Phase 1: Lexical Analysis (already present)
2. Phase 2: Syntax Analysis / Parsing (already present, improved for compatibility)
3. Phase 3: Semantic Analysis (implemented in this iteration)

Phases 4, 5, and 6 are intentionally deferred:

1. Phase 4: Intermediate Code Generation (TAC)
2. Phase 5: Optimization
3. Phase 6: Target Code Generation / Runtime

This matches the requirement: move forward phase-by-phase, keep work runnable and verifiable, and avoid finishing everything in one iteration.

---

## What Is Semantic Analysis (Beginner Explanation)
Think of compilation like checking a school exam in steps:

1. Lexer checks letters/words (tokens)
2. Parser checks grammar (sentence structure)
3. Semantic Analyzer checks meaning

Semantic analysis answers questions like:

1. Was a variable declared before use?
2. Are we assigning the correct type? (like storing true into int)
3. Are function calls using correct argument count and types?
4. Are return statements valid for the function return type?
5. Are const variables protected from reassignment?
6. Are conditions in if/while/for actually boolean?

A program can be grammatically correct but semantically wrong. Example:

- Grammar-correct: `int x; x = true;`
- Semantic error: cannot put bool into int

---

## Runnable + Verifiable Status for This Iteration
The compiler now runs and validates through semantic analysis.

### What Works Now
1. Source file loading
2. Tokenization
3. AST generation
4. Semantic checks (type/scope/function rules)
5. Clear semantic error messages

### What Is Deferred on Purpose
1. TAC printing (`--tac`)
2. Optimization (`-O` / `--optimize`)
3. Output assembly generation (`-o`)
4. Runtime execution (`--run`)

If these options are passed, CLI clearly tells user they are reserved for future phases.

### How to Verify This Phase
Run focused tests:

```bash
pytest -q tests/test_lexer.py tests/test_parser.py tests/test_semantic.py
```

Expected result from this iteration:

- 31 passed

---

## File-by-File Detailed Explanation

## 1) main.py (root)
### Purpose
Repository root entry point.

### What changed
Large old root runner logic was replaced with a clean forwarder:

- Imports `main` from `src.main`
- Calls it in `if __name__ == "__main__"`

### Why this is better
1. Single source of truth for CLI behavior
2. No duplicate pipeline logic in two places
3. Easier maintenance for future phases

### Beginner mental model
`main.py` is now just the front door that forwards to the real compiler entry in `src/main.py`.

---

## 2) src/main.py
### Purpose
Primary command-line compiler flow.

### What changed in this iteration
1. Integrated semantic analysis into the active pipeline
2. Added semantic error handling (`SemanticError`)
3. Limited pipeline to phase 3 only
4. Added explicit message that phases 4+ are deferred
5. Kept future options in CLI but marked as reserved

### Current phase flow
1. Read source file
2. Phase 1: Lexer -> token list
3. Phase 2: Parser -> AST
4. Phase 3: SemanticAnalyzer -> validates AST meaning
5. Stop there (for now)

### Why this matters
This gives a real milestone: language checking is now meaningful, not just syntax parsing.

---

## 3) src/semantic/__init__.py
### Purpose
Public exports for semantic package.

### What changed
Now exports real semantic components:

1. `SemanticAnalyzer`
2. `SemanticError`
3. `Symbol`
4. `Scope`
5. `SymbolTable`

### Why this matters
Other modules can import semantic components from one clean package entry.

---

## 4) src/semantic/symbol_table.py (new)
### Purpose
Implements scope-aware symbol storage.

### Core classes
1. `Symbol`
2. `Scope`
3. `SymbolTable`

### How it works (easy version)
Imagine folders inside folders:

1. Global folder holds global declarations
2. Function folder holds parameters and locals
3. Block folder holds inner block variables

Lookup checks current folder first, then parent folders.

### Key behaviors
1. Duplicate declaration in same scope raises error
2. Entering a block/function creates child scope
3. Exiting scope returns to parent
4. Lookup can be current-only or upward-search

### Why this matters
Without a symbol table, compiler cannot know whether names exist or which declaration they refer to.

---

## 5) src/semantic/analyzer.py (new)
### Purpose
Performs semantic validation over AST.

### Main design
Two-pass analysis at top level:

1. Pass 1: collect global functions and variables
2. Pass 2: analyze function bodies using declared symbols

### Validations implemented
1. Undeclared identifier usage detection
2. Assignment to undeclared names detection
3. Type compatibility in assignment/return/arguments
4. Const enforcement (must initialize, cannot reassign)
5. Function call checks:
   - function exists
   - argument count matches
   - argument types match expected parameter types
6. Return rules:
   - return outside function -> error
   - void function returning value -> error
   - non-void missing return value -> error
7. If/while/for condition must be bool
8. Binary operator typing rules:
   - arithmetic requires numeric
   - relational requires numeric
   - logical requires bool
   - equality requires compatible types

### Type behavior choices in this phase
1. `int` can widen into `float`
2. `int` and `float` are considered compatible in comparisons
3. `%` operator requires integers
4. `/` returns float type

### Error style
Semantic errors include line/column when available:

- `Semantic Error at line:column - message`

### Why this matters
This is the first phase that protects logical correctness of programs, not just grammar.

---

## 6) src/parser/ast_nodes.py
### Purpose
Defines AST node structures.

### What changed
Compatibility and usability improvements were added so parser tests and semantic layer can work smoothly.

#### Added/updated compatibility aliases
1. `Program.functions` property
2. `VariableDeclaration.type_name` alias for `var_type`
3. `ParameterDeclaration.type_name` alias for `param_type`
4. `FunctionDeclaration.name` alias for `identifier`
5. `ReturnStatement.expression` alias for `value`
6. `AssignmentExpression.expression` alias for `value`

#### Added compatibility node
1. `IntegerLiteral` class (subclass of `Literal`)

#### Added statement alias node
1. `AssignmentStatement` (statement-form assignment)

#### Added AST rendering utility
1. `ast_to_string(node, indent=0)`

### Why this matters
1. Existing tests and old API styles continue to work
2. Semantic analyzer can rely on consistent node shapes
3. AST printing is now available from parser package

---

## 7) src/parser/parser.py
### Purpose
Recursive-descent parser.

### What changed
Parser was improved for completeness and semantic-phase readiness.

### Supported constructs now include
1. Global declarations and function declarations
2. Local variable/const declarations
3. Assignment statements and expression statements
4. `if` / `else`
5. `while`
6. `for` loop
7. `return`
8. `read(identifier)`
9. `print(expression)`
10. Function call expressions
11. Unary and binary expressions with precedence

### Expression precedence implemented
From lower to higher:

1. Assignment
2. Logical OR
3. Logical AND
4. Equality
5. Relational
6. Additive
7. Multiplicative
8. Unary
9. Postfix (calls)
10. Primary literals/identifiers/grouping

### Additional API helpers
1. `parse(tokens)` convenience function
2. `parse_file(filename)`
3. `parse_string(source)`

### Why this matters
Semantic analysis needs a rich and stable AST from parser. These updates provide that.

---

## 8) src/parser/__init__.py
### Purpose
Parser package exports.

### What changed
Exports now include:

1. `parse` helper
2. `parse_file`
3. `parse_string`
4. `ast_to_string`

### Why this matters
Cleaner imports in tests and CLI:

- `from src.parser import Parser, parse, ast_to_string`

---

## 9) src/lexer/__init__.py
### Purpose
Lexer package exports.

### What changed
Added compatibility helper:

1. `tokenize(source)` -> calls `tokenize_string(source)`

### Why this matters
Existing tests and older calling style that expect `tokenize(...)` now work without rewriting every caller.

---

## 10) src/utils/error_handler.py
### Purpose
Centralized compiler error formatting helper.

### What changed
Bug fix in location formatting:

- Replaced incorrect `self.column` usage with method parameter `column`

### Why this matters
Prevents wrong attribute access in message formatting and keeps error location output correct.

---

## 11) tests/test_semantic.py (new)
### Purpose
Verifies phase 3 semantic behavior.

### Added coverage
1. Valid program passes
2. Undeclared identifier fails
3. Type mismatch fails
4. Wrong function argument count fails
5. Const reassignment fails

### Why this matters
Confirms semantic analyzer is runnable and catches real misuse cases.

---

## Design Notes for First-Time Compiler Learners

## Why parser and semantic are separate modules
Separation makes debugging easier:

1. Parser answers: “Is syntax structure valid?”
2. Semantic analyzer answers: “Does structure make sense?”

If an error is syntax-related, parser catches it earlier.
If syntax is valid but meaning is wrong, semantic catches it next.

This mirrors real industrial compiler architecture but in beginner-friendly scale.

## How symbol tables connect to scopes
When compiler enters a function or block, it pushes a new scope.
When leaving, it pops that scope.

This naturally supports variable shadowing and proper name resolution.

## Why two passes in semantic analyzer
If function A calls function B, and B appears later in source file:

1. Pass 1 registers function signatures
2. Pass 2 validates bodies and calls

So call checking works even if declaration order differs.

---

## Current Limitations (Intentionally Left for Future Phases)
1. No TAC emission in this phase
2. No optimization pass execution
3. No target machine output file generation
4. No runtime/VM execution

This is intentional to keep the milestone clean and verifiable.

---

## Quick Commands for Reviewers

### Run semantic-phase tests
```bash
pytest -q tests/test_lexer.py tests/test_parser.py tests/test_semantic.py
```

### Run compiler on a sample with verbose output
```bash
python main.py examples/hello.ml --verbose --tokens --ast
```

### Check semantic error behavior (example with undeclared variable)
```bash
python main.py examples/simple_calc.ml --verbose
```

(Use/prepare sources that intentionally violate semantic rules to observe failures.)

---

## Phase Outcome Summary
This iteration delivers a real, test-backed semantic analysis phase while deliberately postponing code generation pipeline stages.

In simple words:

1. The compiler can now read code, parse it, and understand if it "makes sense" semantically.
2. It still does not generate final machine/target code in this branch iteration by design.
3. The phase is runnable and verifiable with passing tests.

That satisfies the requested incremental milestone approach.
