# GitHub Setup and Branch Management Guide

## Table of Contents
1. [Initial Repository Setup](#initial-repository-setup)
2. [Branch Strategy](#branch-strategy)
3. [Setting Up Branches](#setting-up-branches)
4. [Workflow Guidelines](#workflow-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Team Collaboration](#team-collaboration)
7. [Best Practices](#best-practices)

## Initial Repository Setup

### Step 1: Create GitHub Repository

1. **Log into GitHub** and navigate to [github.com](https://github.com)

2. **Create New Repository**
   - Click the "+" icon in the top right → "New repository"
   - Repository name: `minlang-compiler`
   - Description: "Educational compiler for MinLang programming language"
   - Visibility: Public (or Private for team-only access)
   - ✅ Initialize with README (skip if you have local code)
   - Add `.gitignore`: Choose "Python"
   - Choose license: MIT License

3. **Click "Create repository"**

### Step 2: Clone Repository Locally

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/minlang-compiler.git

# Navigate into the directory
cd minlang-compiler

# Verify remote
git remote -v
```

### Step 3: Initial Project Setup

```bash
# Add all project files
git add .

# Make initial commit
git commit -m "Initial project setup with basic structure"

# Push to main branch
git push origin main
```

### Step 4: Protect Main Branch

1. Go to repository **Settings** → **Branches**
2. Click **Add rule** under "Branch protection rules"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings

## Branch Strategy

### Branch Naming Convention

We use **Git Flow** branching model with the following structure:

```
main (production-ready)
  │
  └─── develop (integration)
         │
         ├─── feature/lexer-implementation
         ├─── feature/parser-ast-generation
         ├─── feature/semantic-analysis
         ├─── feature/code-generation
         ├─── feature/optimization
         ├─── bugfix/lexer-string-handling
         ├─── hotfix/critical-parser-bug
         └─── docs/update-readme
```

### Branch Types

#### 1. Main Branch (`main`)
- **Purpose**: Production-ready code
- **Rules**: 
  - Never commit directly
  - Only merge from `develop` via Pull Request
  - All code must be tested and reviewed
  - Tagged with version numbers (v1.0, v1.1, etc.)

#### 2. Development Branch (`develop`)
- **Purpose**: Integration branch for features
- **Rules**:
  - Never commit directly (except for minor fixes)
  - Merge completed features here
  - Must always be in a working state
  - CI/CD tests must pass

#### 3. Feature Branches (`feature/*`)
- **Purpose**: New feature development
- **Naming**: `feature/<feature-name>`
- **Examples**:
  - `feature/lexer-implementation`
  - `feature/parser-expressions`
  - `feature/symbol-table`
  - `feature/ast-visualization`
- **Lifecycle**: Branch from `develop`, merge back to `develop`

#### 4. Bugfix Branches (`bugfix/*`)
- **Purpose**: Fix non-critical bugs
- **Naming**: `bugfix/<bug-description>`
- **Examples**:
  - `bugfix/lexer-token-recognition`
  - `bugfix/parser-error-handling`
- **Lifecycle**: Branch from `develop`, merge back to `develop`

#### 5. Hotfix Branches (`hotfix/*`)
- **Purpose**: Fix critical production bugs
- **Naming**: `hotfix/<critical-issue>`
- **Examples**:
  - `hotfix/lexer-crash-on-empty-file`
  - `hotfix/parser-infinite-loop`
- **Lifecycle**: Branch from `main`, merge to both `main` and `develop`

#### 6. Documentation Branches (`docs/*`)
- **Purpose**: Documentation updates
- **Naming**: `docs/<doc-topic>`
- **Examples**:
  - `docs/update-readme`
  - `docs/api-documentation`
- **Lifecycle**: Branch from `develop`, merge back to `develop`

## Setting Up Branches

### Create and Set Up Develop Branch

```bash
# Ensure you're on main
git checkout main

# Create develop branch
git checkout -b develop

# Push develop to remote
git push -u origin develop

# Set develop as default branch on GitHub (optional)
# Go to: Settings → Branches → Default branch → Change to 'develop'
```

### Create Task-Specific Branches

#### For Team Lead / Architecture

```bash
# Create architecture/setup branch
git checkout develop
git checkout -b feature/project-setup
git push -u origin feature/project-setup

# Create documentation branch
git checkout develop
git checkout -b docs/initial-documentation
git push -u origin docs/initial-documentation
```

#### For Lexer Developer

```bash
# Create lexer branch
git checkout develop
git checkout -b feature/lexer-implementation
git push -u origin feature/lexer-implementation

# Create token definition branch
git checkout develop
git checkout -b feature/token-definitions
git push -u origin feature/token-definitions
```

#### For Parser Developer

```bash
# Create parser branch
git checkout develop
git checkout -b feature/parser-implementation
git push -u origin feature/parser-implementation

# Create AST branch
git checkout develop
git checkout -b feature/ast-nodes
git push -u origin feature/ast-nodes
```

#### For Semantic Analysis Developer

```bash
# Create semantic analyzer branch
git checkout develop
git checkout -b feature/semantic-analysis
git push -u origin feature/semantic-analysis

# Create symbol table branch
git checkout develop
git checkout -b feature/symbol-table
git push -u origin feature/symbol-table
```

#### For Code Generation Developer

```bash
# Create IR generator branch
git checkout develop
git checkout -b feature/intermediate-codegen
git push -u origin feature/intermediate-codegen

# Create target code branch
git checkout develop
git checkout -b feature/target-codegen
git push -u origin feature/target-codegen
```

#### For Testing & Documentation

```bash
# Create testing branch
git checkout develop
git checkout -b feature/unit-tests
git push -u origin feature/unit-tests

# Create documentation branch
git checkout develop
git checkout -b docs/comprehensive-docs
git push -u origin docs/comprehensive-docs
```

### Quick Command Reference

```bash
# List all branches
git branch -a

# Switch to a branch
git checkout <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Delete local branch
git branch -d <branch-name>

# Delete remote branch
git push origin --delete <branch-name>

# Update your branch with latest develop
git checkout <your-branch>
git pull origin develop
git merge develop
```

## Workflow Guidelines

### Daily Workflow

#### 1. Start Your Day

```bash
# Update your local develop
git checkout develop
git pull origin develop

# Switch to your feature branch
git checkout feature/your-feature

# Update your branch with latest develop
git merge develop

# Start coding!
```

#### 2. While Working

```bash
# Check status often
git status

# Stage your changes
git add <file>  # or git add . for all files

# Commit with meaningful message
git commit -m "feat: implement token recognition for keywords"

# Push to remote regularly
git push origin feature/your-feature
```

#### 3. Before Ending Your Day

```bash
# Ensure all changes are committed
git status

# Push your work
git push origin feature/your-feature

# Update develop (if needed)
git checkout develop
git pull origin develop
```

### Commit Message Convention

Use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(lexer): add support for float literals"
git commit -m "fix(parser): resolve infinite loop in expression parsing"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(lexer): add unit tests for keyword recognition"
git commit -m "refactor(parser): simplify AST node creation"
```

## Pull Request Process

### Creating a Pull Request

1. **Ensure Your Branch is Up-to-Date**

```bash
git checkout develop
git pull origin develop
git checkout feature/your-feature
git merge develop
```

2. **Push Your Branch**

```bash
git push origin feature/your-feature
```

3. **Create PR on GitHub**
   - Navigate to repository on GitHub
   - Click "Pull requests" → "New pull request"
   - Base: `develop` ← Compare: `feature/your-feature`
   - Click "Create pull request"

4. **Fill PR Template**

```markdown
## Description
Brief description of changes made

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring

## Changes Made
- Implemented X
- Fixed Y
- Updated Z

## Testing
- [ ] Unit tests added
- [ ] All tests passing
- [ ] Tested manually

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Closes #issue-number

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Tests added
```

### Reviewing a Pull Request

**For Reviewers**:

1. **Check Code Quality**
   - Follows coding standards
   - Well-documented
   - No unnecessary complexity

2. **Review Changes**
   - Click "Files changed" tab
   - Add inline comments
   - Suggest improvements

3. **Test Locally**
```bash
# Fetch the branch
git fetch origin
git checkout feature/branch-name

# Run tests
pytest

# Test functionality
python src/main.py examples/test.ml
```

4. **Approve or Request Changes**
   - Leave review comments
   - Approve if ready
   - Request changes if needed

### Merging Strategy

**Squash and Merge** (Recommended):
- Combines all commits into one
- Keeps history clean
- Use for feature branches

**Merge Commit**:
- Preserves all commits
- Shows complete history
- Use for important milestones

**Rebase and Merge**:
- Linear history
- Individual commits preserved
- Use for small, clean PRs

## Team Collaboration

### Setting Up Team Access

1. **Add Collaborators**
   - Go to repository Settings → Collaborators
   - Click "Add people"
   - Enter GitHub usernames
   - Send invitations

2. **Create Teams** (for organizations)
   - Organization settings → Teams
   - Create teams: `minlang-core`, `minlang-contributors`
   - Assign members and permissions

### GitHub Projects for Task Management

1. **Create Project Board**
   - Repository → Projects → New project
   - Choose "Board" template
   - Columns: To Do, In Progress, Review, Done

2. **Create Issues for Tasks**
```markdown
Title: Implement Lexer Token Recognition

## Description
Implement token recognition for all MinLang keywords and operators

## Tasks
- [ ] Define TokenType enum
- [ ] Implement keyword recognition
- [ ] Implement operator recognition
- [ ] Add unit tests
- [ ] Update documentation

## Assigned to: @username
## Labels: enhancement, lexer
## Milestone: Phase 1
```

3. **Link Issues to PRs**
   - Reference issue in PR description: `Closes #5`
   - Automatically closes issue when PR is merged

### Communication Channels

1. **GitHub Discussions**: For general questions and discussions
2. **Issues**: For bugs and feature requests
3. **Pull Request Comments**: For code review
4. **Wiki**: For detailed documentation
5. **README**: For quick reference

## Best Practices

### Do's ✅

1. **Commit Often**
   - Small, logical commits
   - Each commit should work

2. **Write Meaningful Commit Messages**
   - Clear and descriptive
   - Follow conventions

3. **Pull Before Push**
   - Always update before pushing
   - Avoid conflicts

4. **Review Your Own Code**
   - Before creating PR
   - Check for issues

5. **Keep Branches Up-to-Date**
   - Merge develop regularly
   - Resolve conflicts early

6. **Test Before Committing**
   - Run all tests
   - Verify functionality

7. **Document Your Changes**
   - Update relevant docs
   - Add code comments

### Don'ts ❌

1. **Don't Commit to Main Directly**
   - Always use feature branches
   - Always create PR

2. **Don't Commit Generated Files**
   - Add to `.gitignore`
   - Only commit source code

3. **Don't Force Push to Shared Branches**
   - Never use `git push -f` on develop/main
   - Only force push your own feature branches if needed

4. **Don't Commit Large Files**
   - Use Git LFS for large files
   - Keep repository lightweight

5. **Don't Include Secrets**
   - No API keys, passwords
   - Use environment variables

6. **Don't Create Huge PRs**
   - Break into smaller PRs
   - Easier to review

## Troubleshooting

### Common Issues

#### Merge Conflicts

```bash
# Update your branch
git checkout feature/your-feature
git fetch origin
git merge origin/develop

# Conflicts will be marked in files
# Edit files to resolve conflicts
# Look for: <<<<<<< HEAD, =======, >>>>>>> develop

# After resolving
git add <resolved-files>
git commit -m "merge: resolve conflicts with develop"
git push origin feature/your-feature
```

#### Accidentally Committed to Wrong Branch

```bash
# If not pushed yet
git reset HEAD~1  # Undo last commit, keep changes
git stash         # Save changes
git checkout correct-branch
git stash pop     # Apply changes

# If already pushed
# Create new branch from correct base
# Cherry-pick commits
git cherry-pick <commit-hash>
```

#### Need to Update Feature Branch

```bash
# Rebase onto develop (cleaner history)
git checkout feature/your-feature
git rebase develop

# Or merge (preserves history)
git checkout feature/your-feature
git merge develop
```

### Getting Help

1. **GitHub Docs**: [docs.github.com](https://docs.github.com)
2. **Git Documentation**: [git-scm.com](https://git-scm.com/doc)
3. **Team Lead**: Ask project lead for assistance
4. **Stack Overflow**: Search for common issues

## Quick Reference Card

```bash
# Setup
git clone <url>                           # Clone repository
git remote -v                             # View remotes

# Branching
git branch                                # List branches
git checkout -b <branch>                  # Create and switch
git checkout <branch>                     # Switch branch
git branch -d <branch>                    # Delete branch

# Changes
git status                                # Check status
git add <file>                            # Stage file
git add .                                 # Stage all
git commit -m "message"                   # Commit
git push origin <branch>                  # Push

# Updating
git pull origin <branch>                  # Pull changes
git fetch origin                          # Fetch without merge
git merge <branch>                        # Merge branch

# History
git log                                   # View commits
git log --oneline --graph                 # Pretty log
git diff                                  # View changes

# Undoing
git reset HEAD~1                          # Undo last commit
git checkout -- <file>                    # Discard changes
git revert <commit>                       # Revert commit
```

## Automation with GitHub Actions

### Continuous Integration Setup

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 src/ --count --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Conclusion

Following this GitHub workflow ensures:
- **Organized Development**: Clear separation of work
- **Code Quality**: Review process maintains standards
- **Team Collaboration**: Everyone works smoothly together
- **Project History**: Clean, understandable commit history
- **Risk Management**: Protected main branch, tested code

Remember: **When in doubt, create a branch!** It's always safer to experiment in a branch than to break shared code.

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Maintained By**: MinLang Team
