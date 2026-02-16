# MinLang Compiler - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

This guide will help you get the MinLang Compiler up and running quickly.

## Step 1: Extract the Project

```bash
# Extract the zip file
unzip minlang-compiler.zip
cd minlang-compiler
```

## Step 2: Set Up Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# For development (optional)
pip install pytest pytest-cov black flake8
```

## Step 4: Verify Installation

```bash
# Run a simple test
python main.py examples/hello_world.min --verbose

# You should see:
# ✓ Lexical analysis complete
# ✓ Syntax analysis complete
# ✓ Compilation successful!
```

## Step 5: Explore the Project

### View Token Stream
```bash
python main.py examples/calculator.min --tokens
```

### View Abstract Syntax Tree
```bash
python main.py examples/hello_world.min --ast
```

### Run Tests (if pytest installed)
```bash
pytest tests/ -v
```

## Understanding the Output

When you run a program, you'll see:

```
[PHASE 1] Running Lexical Analysis...
✓ Lexical analysis complete: X tokens generated

[PHASE 2] Running Syntax Analysis (Parsing)...
✓ Syntax analysis complete: AST generated

[PHASE 3] Semantic Analysis (Not yet implemented)
[PHASE 4] IR Generation (Not yet implemented)
[PHASE 6] Code Generation (Not yet implemented)

✓ Compilation successful!
```

## Writing Your First MinLang Program

Create a file `myprogram.min`:

```c
int main() {
    int a;
    int b;
    int sum;
    
    a = 10;
    b = 20;
    sum = a + b;
    
    print(sum);
    return 0;
}
```

Compile it:
```bash
python main.py myprogram.min --verbose --ast
```

## Project Structure Overview

```
minlang-compiler/
├── main.py              # Run this to compile
├── src/                 # Source code
│   ├── lexer/          # ✅ Complete
│   ├── parser/         # 🔄 30% Complete
│   ├── semantic/       # ⏳ TODO
│   └── codegen/        # ⏳ TODO
├── tests/              # Test suite
├── examples/           # Example programs
└── docs/               # Documentation
```

## Next Steps

### For Students/Contributors

1. **Read the Documentation**
   - `README.md` - Project overview
   - `ARCHITECTURE.md` - System design
   - `CONTRIBUTING.md` - How to contribute
   - `docs/GITHUB_WORKFLOW.md` - Git workflow

2. **Choose Your Component**
   - Parser: Complete the remaining 70%
   - Semantic: Type checking and symbol table
   - Codegen: IR generation and code emission

3. **Set Up Your Branch**
   ```bash
   git checkout -b feature/your-component
   # Start coding!
   ```

### For Instructors

1. **Course Integration**
   - Use as semester project
   - Assign components to teams
   - Week-by-week milestones
   - See `docs/DETAILED_DESCRIPTION.md`

2. **Grading Rubric Ideas**
   - Code quality: 30%
   - Functionality: 40%
   - Testing: 15%
   - Documentation: 15%

## Common Commands

```bash
# Compile a program
python main.py program.min

# Verbose mode
python main.py program.min --verbose

# Show tokens
python main.py program.min --tokens

# Show AST
python main.py program.min --ast

# Run tests
pytest tests/

# Format code
black src/ tests/

# Check code style
flake8 src/ tests/
```

## Troubleshooting

### Problem: "No module named 'src'"

**Solution:** Make sure you're in the project root directory:
```bash
cd minlang-compiler
python main.py examples/hello_world.min
```

### Problem: "Module not found: pytest"

**Solution:** Install test dependencies:
```bash
pip install pytest pytest-cov
```

### Problem: "Permission denied"

**Solution:** Make main.py executable:
```bash
chmod +x main.py
```

## Getting Help

- 📖 Read documentation in `docs/` directory
- 🐛 Check existing issues on GitHub
- 💬 Ask questions in team meetings
- 📧 Contact project maintainer

## What's Implemented (30%)

✅ **Complete:**
- Lexical analysis (100%)
- Token types and handling
- Error reporting
- Basic parser structure
- Expression parsing
- Function declarations
- Example programs

⏳ **TODO:**
- Complete parser (70% remaining)
- Semantic analysis
- IR generation
- Optimization
- Code generation

## Resources

- **Documentation:** See `docs/` folder
- **Examples:** See `examples/` folder
- **Tests:** See `tests/` folder
- **Architecture:** `ARCHITECTURE.md`

## Success!

If you see "✓ Compilation successful!" then you're all set!

Start exploring the code and happy hacking! 🎉

---

**Need Help?** Check `CONTRIBUTING.md` or open an issue on GitHub.

**Version:** 0.3.0  
**Last Updated:** February 2026
