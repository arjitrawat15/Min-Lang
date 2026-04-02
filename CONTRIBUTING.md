# Contributing to MinLang Compiler

Thank you for your interest in contributing to the MinLang Compiler project! This document provides guidelines for contributing to the project.

## Project Status

Current Implementation: **30% Complete**
- ✅ Lexical Analyzer (Complete)
- ✅ Basic Parser (30% Complete)
- ⏳ Semantic Analyzer (To be implemented)
- ⏳ IR Generator (To be implemented)
- ⏳ Optimizer (To be implemented)
- ⏳ Code Generator (To be implemented)

## Team Structure

This project is organized as a group project with different team members responsible for different components:

| Component | Status | Branch | Owner |
|-----------|--------|--------|-------|
| Lexer | ✅ Complete | `main` | Team Lead |
| Parser | 🔄 In Progress | `feature/parser` | Member 2 |
| Semantic Analyzer | ⏳ Pending | `feature/semantic` | Member 3 |
| Code Generator | ⏳ Pending | `feature/codegen` | Member 4 |
| Testing | 🔄 Ongoing | `feature/testing` | All Members |
| Documentation | 🔄 Ongoing | `feature/docs` | All Members |

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/minlang-compiler.git
cd minlang-compiler
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 isort mypy
```

### 3. Create a Feature Branch

```bash
# Create your feature branch
git checkout -b feature/your-feature-name

# Examples:
# git checkout -b feature/parser-if-statements
# git checkout -b feature/semantic-type-checker
# git checkout -b fix/lexer-float-parsing
```

## Development Workflow

### 1. Write Code

- Follow PEP 8 style guidelines
- Write clear, self-documenting code
- Add docstrings to all functions and classes
- Keep functions small and focused

### 2. Write Tests

```bash
# Run tests
pytest tests/

# Run specific test file
pytest tests/test_lexer.py

# Run with coverage
pytest --cov=src tests/
```

### 3. Format Code

```bash
# Format with black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add if-statement parsing support"

# Commit message format:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# test: Test additions/changes
# refactor: Code refactoring
# style: Code formatting
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Then create a Pull Request on GitHub
```

## Code Style Guidelines

### Python Style

Follow PEP 8 with these specifics:

```python
# Use 4 spaces for indentation
# Maximum line length: 88 characters (black default)
# Use type hints where appropriate

def parse_expression(self, tokens: List[Token]) -> Expression:
    """
    Parse an expression from tokens.
    
    Args:
        tokens: List of tokens to parse
        
    Returns:
        Parsed Expression AST node
        
    Raises:
        ParserError: If parsing fails
    """
    pass
```

### Naming Conventions

- **Classes**: PascalCase (`TokenType`, `Parser`)
- **Functions/Methods**: snake_case (`parse_expression`, `get_token`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_TOKENS`, `EOF`)
- **Private methods**: Prefix with underscore (`_internal_method`)

### Documentation

- Every module should have a module docstring
- Every class should have a class docstring
- Every public function/method should have a docstring
- Use Google-style docstrings

## Testing Guidelines

### Test Structure

```python
class TestFeatureName:
    """Test suite for specific feature"""
    
    def test_basic_functionality(self):
        """Test basic behavior"""
        # Arrange
        input_data = "..."
        
        # Act
        result = function(input_data)
        
        # Assert
        assert result == expected
```

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and error cases
- Test edge cases and boundary conditions
- Include integration tests for complete workflows

## Pull Request Process

### Before Submitting

1. ✅ All tests pass: `pytest tests/`
2. ✅ Code is formatted: `black src/ tests/`
3. ✅ No linting errors: `flake8 src/ tests/`
4. ✅ Documentation updated
5. ✅ CHANGELOG.md updated (if applicable)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] No linting errors
```

### Review Process

1. At least one team member must review and approve
2. All CI checks must pass
3. No unresolved conversations
4. Merge conflicts resolved

## Component-Specific Guidelines

### Parser Development

If working on the parser:
1. Update grammar specification in `docs/GRAMMAR_SPECIFICATION.md`
2. Add AST node classes to `ast_nodes.py`
3. Implement parsing methods in `parser.py`
4. Add comprehensive tests
5. Update examples with new language features

### Semantic Analyzer Development

If working on semantic analysis:
1. Implement symbol table structure
2. Add type checking rules
3. Handle scope management
4. Provide clear error messages
5. Test with valid and invalid programs

### Code Generator Development

If working on code generation:
1. Define IR format clearly
2. Implement IR generation from AST
3. Add optimization passes (optional)
4. Generate target code
5. Verify correctness with test programs

## Common Tasks

### Adding a New Token Type

1. Add to `TokenType` enum in `token_types.py`
2. Update `KEYWORDS`, `OPERATORS`, or `DELIMITERS` dict
3. Add tokenization logic in `tokenizer.py`
4. Add tests in `test_lexer.py`

### Adding a New Statement Type

1. Define AST node class in `ast_nodes.py`
2. Add parsing method in `parser.py`
3. Update grammar documentation
4. Add tests in `test_parser.py`
5. Add example program using the feature

### Adding a New Built-in Function

1. Add keyword token if needed
2. Update parser to recognize function
3. Add semantic checking rules
4. Implement in code generator
5. Add tests and examples

## Getting Help

- 💬 Open an issue for bugs or questions
- 📧 Email team lead for urgent matters
- 📚 Check documentation in `docs/` directory
- 🤝 Ask teammates in team meetings

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy toward other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Project documentation
- Release notes
- Academic paper (if published)

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the `question` label
4. Contact the team lead

Thank you for contributing to MinLang Compiler! 🚀
