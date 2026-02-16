# GitHub Workflow and Branching Strategy

## Complete Guide to Managing the MinLang Compiler Project on GitHub

This document provides step-by-step instructions for setting up the project on GitHub and managing branches for collaborative development.

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [Repository Configuration](#repository-configuration)
3. [Branching Strategy](#branching-strategy)
4. [Workflow for Team Members](#workflow-for-team-members)
5. [Pull Request Process](#pull-request-process)
6. [Branch Management](#branch-management)
7. [Continuous Integration](#continuous-integration)

---

## 1. Initial Setup

### Step 1: Create GitHub Repository

```bash
# On GitHub.com:
# 1. Click "New Repository"
# 2. Name: minlang-compiler
# 3. Description: Educational compiler implementation for MinLang
# 4. Public/Private: Choose based on your needs
# 5. Initialize: Do NOT initialize (we have files already)
# 6. Click "Create Repository"
```

### Step 2: Initialize Local Git Repository

```bash
# Navigate to project directory
cd minlang-compiler

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Lexer and basic parser implementation (30%)"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/minlang-compiler.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

```bash
# Check that all files are uploaded
git log
git status

# Visit your GitHub repository to verify
```

---

## 2. Repository Configuration

### Setting Up Branch Protection

```
On GitHub:
1. Go to Settings → Branches
2. Add branch protection rule for 'main':
   ☑ Require pull request reviews before merging
   ☑ Require status checks to pass before merging
   ☑ Require branches to be up to date before merging
   ☑ Include administrators
3. Save changes
```

### Setting Up Labels

Create these labels for issue management:

```
Labels to create (Settings → Labels):
- bug (red) - Something isn't working
- enhancement (green) - New feature
- documentation (blue) - Documentation improvements
- help wanted (yellow) - Extra attention needed
- good first issue (purple) - Good for newcomers
- lexer (light blue) - Lexer component
- parser (orange) - Parser component
- semantic (pink) - Semantic analyzer component
- codegen (brown) - Code generation component
- testing (gray) - Testing related
```

### Setting Up Project Board (Optional)

```
1. Go to Projects → New Project
2. Name: "MinLang Compiler Development"
3. Template: "Automated kanban"
4. Columns: To Do, In Progress, Review, Done
```

---

## 3. Branching Strategy

### Branch Structure

```
main (protected)
  ├── feature/parser          # Parser development
  ├── feature/semantic        # Semantic analyzer
  ├── feature/codegen         # Code generation
  ├── feature/testing         # Testing improvements
  ├── feature/docs            # Documentation
  ├── fix/bug-name            # Bug fixes
  └── experimental/idea       # Experimental features
```

### Branch Naming Conventions

```
feature/<component-name>     # New features
fix/<bug-description>        # Bug fixes
docs/<topic>                 # Documentation
test/<test-name>             # Test additions
refactor/<component>         # Code refactoring
experimental/<idea>          # Experimental work
```

### Creating All Team Branches

```bash
# Create all feature branches from main
git checkout main

# Create parser branch
git checkout -b feature/parser
git push -u origin feature/parser

# Create semantic branch
git checkout main
git checkout -b feature/semantic
git push -u origin feature/semantic

# Create codegen branch
git checkout main
git checkout -b feature/codegen
git push -u origin feature/codegen

# Create testing branch
git checkout main
git checkout -b feature/testing
git push -u origin feature/testing

# Create docs branch
git checkout main
git checkout -b feature/docs
git push -u origin feature/docs

# Return to main
git checkout main
```

---

## 4. Workflow for Team Members

### A. Getting Started (One-time setup)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/minlang-compiler.git
cd minlang-compiler

# 2. Set up development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 4. Verify setup
pytest tests/
```

### B. Starting Work on Your Component

**Example: Working on Parser (Member 2)**

```bash
# 1. Ensure you're up to date
git checkout main
git pull origin main

# 2. Switch to your feature branch
git checkout feature/parser

# 3. Sync with main
git merge main

# 4. Start working
# ... make changes ...

# 5. Test your changes
pytest tests/test_parser.py
pytest tests/  # Run all tests

# 6. Stage and commit
git add src/parser/parser.py
git commit -m "feat(parser): Implement if-statement parsing"

# 7. Push to GitHub
git push origin feature/parser
```

### C. Daily Development Workflow

```bash
# Morning: Update your branch
git checkout feature/your-component
git fetch origin
git merge origin/main

# Work throughout the day
# ... code, test, commit ...

# Commits should be frequent and atomic
git add <files>
git commit -m "descriptive message"

# Evening: Push your work
git push origin feature/your-component
```

### D. Commit Message Guidelines

```
Format: <type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Tests
- refactor: Code refactoring
- style: Formatting
- chore: Maintenance

Examples:
✓ feat(parser): Add while loop parsing support
✓ fix(lexer): Handle escaped quotes in strings
✓ docs(readme): Update installation instructions
✓ test(parser): Add tests for binary expressions
✗ updated stuff
✗ fixed bug
```

---

## 5. Pull Request Process

### Creating a Pull Request

```bash
# 1. Ensure all tests pass
pytest tests/
black src/ tests/
flake8 src/ tests/

# 2. Push final changes
git push origin feature/your-component

# 3. On GitHub:
# - Go to "Pull Requests" → "New Pull Request"
# - Base: main
# - Compare: feature/your-component
# - Fill in template (see below)
# - Assign reviewers
# - Add labels
# - Create pull request
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Changes Made
- Added X functionality
- Fixed Y bug
- Updated Z documentation

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] All tests pass locally

## Related Issues
Closes #<issue-number>

## Screenshots (if applicable)
```

### Code Review Process

**For Reviewers:**
1. Check out the branch locally
2. Run tests
3. Review code quality
4. Check documentation
5. Leave comments
6. Approve or request changes

**For Authors:**
1. Address all comments
2. Make requested changes
3. Push updates
4. Respond to comments
5. Request re-review

### Merging Pull Requests

```bash
# Option 1: Merge via GitHub UI (recommended)
# - Click "Merge pull request"
# - Choose "Squash and merge" or "Create merge commit"
# - Confirm merge

# Option 2: Merge locally
git checkout main
git merge feature/your-component
git push origin main
```

---

## 6. Branch Management

### Keeping Branches Updated

```bash
# Update your branch with latest main
git checkout feature/your-component
git fetch origin
git merge origin/main

# Or use rebase (cleaner history)
git checkout feature/your-component
git rebase origin/main
```

### Resolving Conflicts

```bash
# When conflicts occur during merge/rebase:

# 1. See conflicted files
git status

# 2. Open and manually resolve conflicts
# Look for markers: <<<<<<<, =======, >>>>>>>

# 3. Mark as resolved
git add <resolved-files>

# 4. Continue merge/rebase
git merge --continue
# or
git rebase --continue
```

### Syncing Forks (If using forked workflow)

```bash
# 1. Add upstream remote (one-time)
git remote add upstream https://github.com/ORIGINAL_OWNER/minlang-compiler.git

# 2. Fetch upstream changes
git fetch upstream

# 3. Merge into your branch
git checkout main
git merge upstream/main

# 4. Push to your fork
git push origin main
```

### Cleaning Up Branches

```bash
# Delete local branch
git branch -d feature/completed-feature

# Delete remote branch
git push origin --delete feature/completed-feature

# Prune deleted remote branches
git fetch --prune
```

---

## 7. Continuous Integration

### Setting Up GitHub Actions

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, feature/* ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov black flake8
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
    
    - name: Check formatting with black
      run: |
        black --check src/ tests/
    
    - name: Run tests with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 8. Team Member Assignments

### Branch Assignments

| Team Member | Component | Branch | Responsibilities |
|-------------|-----------|--------|------------------|
| Member 1 (Lead) | Integration | `main` | Code review, architecture, integration |
| Member 2 | Parser | `feature/parser` | Complete parser implementation |
| Member 3 | Semantic | `feature/semantic` | Type checking, symbol table |
| Member 4 | Codegen | `feature/codegen` | IR generation, code emission |
| All Members | Testing | `feature/testing` | Test coverage improvements |

### Workflow Example for Each Member

**Member 2 (Parser Development):**
```bash
# Daily workflow
git checkout feature/parser
git merge origin/main
# ... work on parser ...
git add src/parser/parser.py
git commit -m "feat(parser): Add for-loop parsing"
git push origin feature/parser
```

**Member 3 (Semantic Analysis):**
```bash
# Daily workflow
git checkout feature/semantic
git merge origin/main
# ... work on semantic analyzer ...
git add src/semantic/analyzer.py
git commit -m "feat(semantic): Implement type checking"
git push origin feature/semantic
```

---

## 9. Best Practices

### DO:
✅ Commit frequently with clear messages  
✅ Write tests for new features  
✅ Update documentation  
✅ Keep branches up to date with main  
✅ Review others' code  
✅ Ask for help when stuck  

### DON'T:
❌ Commit directly to main  
❌ Push untested code  
❌ Make huge commits  
❌ Ignore merge conflicts  
❌ Skip code review  
❌ Leave broken code in branches  

---

## 10. Troubleshooting

### Common Issues

**Issue: Merge conflicts**
```bash
# Abort merge and try again
git merge --abort

# Or resolve conflicts manually
# Edit conflicted files
git add <resolved-files>
git merge --continue
```

**Issue: Pushed wrong commit**
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1
git push origin feature/branch --force-with-lease
```

**Issue: Need to update branch from main**
```bash
git checkout feature/your-branch
git fetch origin
git rebase origin/main
```

---

## 11. Quick Reference

```bash
# Common commands
git status                    # Check status
git log --oneline            # View commit history
git diff                     # See changes
git stash                    # Temporarily save changes
git stash pop                # Restore stashed changes
git branch -a                # List all branches
git remote -v                # List remotes
git fetch --all              # Fetch all branches
git clean -fd                # Remove untracked files
```

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**For Questions:** Contact team lead or open an issue
