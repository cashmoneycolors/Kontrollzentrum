# 🔗 QUELLCODEVERWALTUNGS-HANDBUCH

**Git Workflow, Best Practices & Collaboration Guide**

---

## 📖 GIT BASICS

### Repository Setup

**1. Clone Main Repository**
```bash
git clone https://github.com/user/kontrollzentrum-master.git
cd kontrollzentrum-master
```

**2. Initialize Submodules**
```bash
git submodule update --init --recursive
```

**3. Create Local Branches**
```bash
git checkout -b develop origin/develop
git checkout -b feature/my-feature develop
```

---

## 🌳 BRANCHING STRATEGY (Git Flow)

### Branch Types

**1. Main Branch (Production)**
```bash
# Only for releases
git checkout main
git merge --no-ff release/v5.0
git tag -a v5.0 -m "Release v5.0"
```

**2. Develop Branch (Integration)**
```bash
# Integration branch for features
git checkout develop
git merge --no-ff feature/new-module
```

**3. Feature Branches**
```bash
# Create feature branch
git checkout -b feature/new-module develop

# Work on feature
git add .
git commit -m "feat: add new module"

# Push to remote
git push -u origin feature/new-module

# Create Pull Request on GitHub
# After review and approval:
git checkout develop
git merge --no-ff feature/new-module
git push origin develop
```

**4. Release Branches**
```bash
# Create release branch
git checkout -b release/v5.1 develop

# Update version
echo "5.1" > VERSION
git add VERSION
git commit -m "chore: bump version to 5.1"

# Merge to main
git checkout main
git merge --no-ff release/v5.1
git tag -a v5.1 -m "Release v5.1"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/v5.1
git push origin develop

# Delete release branch
git branch -d release/v5.1
git push origin --delete release/v5.1
```

**5. Hotfix Branches**
```bash
# Create hotfix branch from main
git checkout -b hotfix/critical-bug main

# Fix the bug
git add .
git commit -m "fix: critical bug in module X"

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v5.0.1 -m "Hotfix v5.0.1"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/critical-bug
git push origin develop

# Delete hotfix branch
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

---

## 📝 COMMIT CONVENTIONS

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style (formatting, etc)
- **refactor**: Code refactoring
- **perf**: Performance improvement
- **test**: Test addition/modification
- **chore**: Build, dependencies, etc

### Examples

```bash
# Feature
git commit -m "feat(modules): add new ai_assistant module"

# Bug Fix
git commit -m "fix(api): resolve authentication issue"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Performance
git commit -m "perf(database): optimize query performance"

# Test
git commit -m "test(modules): add unit tests for ai_assistant"

# Chore
git commit -m "chore(deps): update dependencies"
```

---

## 🔄 WORKFLOW EXAMPLES

### Adding a New Module

**1. Create Feature Branch**
```bash
git checkout -b feature/new-module develop
```

**2. Develop Module**
```bash
# Create module file
touch modules/new_module.py

# Add code
echo "def run(): return 'Hello'" > modules/new_module.py

# Create tests
touch tests/test_new_module.py

# Add tests
echo "import unittest" > tests/test_new_module.py
```

**3. Commit Changes**
```bash
git add modules/new_module.py tests/test_new_module.py
git commit -m "feat(modules): add new_module with tests"
```

**4. Push to Remote**
```bash
git push -u origin feature/new-module
```

**5. Create Pull Request**
- Go to GitHub
- Create Pull Request from `feature/new-module` to `develop`
- Add description
- Request review

**6. Code Review & Merge**
```bash
# After approval:
git checkout develop
git pull origin develop
git merge --no-ff feature/new-module
git push origin develop

# Delete feature branch
git branch -d feature/new-module
git push origin --delete feature/new-module
```

### Fixing a Bug

**1. Create Hotfix Branch**
```bash
git checkout -b hotfix/bug-fix main
```

**2. Fix Bug**
```bash
# Edit file
nano modules/buggy_module.py

# Test fix
python -m pytest tests/test_buggy_module.py
```

**3. Commit Fix**
```bash
git add modules/buggy_module.py
git commit -m "fix(modules): resolve bug in buggy_module"
```

**4. Merge to Main & Develop**
```bash
# Merge to main
git checkout main
git merge --no-ff hotfix/bug-fix
git tag -a v5.0.1 -m "Hotfix v5.0.1"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/bug-fix
git push origin develop

# Cleanup
git branch -d hotfix/bug-fix
git push origin --delete hotfix/bug-fix
```

### Releasing a Version

**1. Create Release Branch**
```bash
git checkout -b release/v5.1 develop
```

**2. Update Version**
```bash
echo "5.1" > VERSION
git add VERSION
git commit -m "chore: bump version to 5.1"
```

**3. Update Changelog**
```bash
# Edit CHANGELOG.md
nano CHANGELOG.md

git add CHANGELOG.md
git commit -m "docs: update changelog for v5.1"
```

**4. Merge to Main**
```bash
git checkout main
git merge --no-ff release/v5.1
git tag -a v5.1 -m "Release v5.1"
git push origin main --tags
```

**5. Merge Back to Develop**
```bash
git checkout develop
git merge --no-ff release/v5.1
git push origin develop
```

**6. Cleanup**
```bash
git branch -d release/v5.1
git push origin --delete release/v5.1
```

---

## 🔍 USEFUL GIT COMMANDS

### Viewing History
```bash
# View commit log
git log --oneline

# View commits for specific file
git log --oneline -- modules/ai_assistant.py

# View commits with diff
git log -p

# View graph
git log --graph --oneline --all
```

### Branching
```bash
# List local branches
git branch

# List remote branches
git branch -r

# List all branches
git branch -a

# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature
```

### Stashing
```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply

# Pop stash
git stash pop

# Delete stash
git stash drop
```

### Undoing Changes
```bash
# Undo uncommitted changes
git checkout -- modules/file.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit)
git revert <commit-hash>
```

### Rebasing
```bash
# Rebase current branch on develop
git rebase develop

# Interactive rebase
git rebase -i HEAD~3

# Continue rebase after conflict
git rebase --continue

# Abort rebase
git rebase --abort
```

---

## 🚨 CONFLICT RESOLUTION

### When Conflicts Occur

**1. Identify Conflicts**
```bash
git status
# Shows files with conflicts
```

**2. View Conflicts**
```bash
# Open conflicted file
nano modules/conflicted_file.py

# Shows:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name
```

**3. Resolve Conflicts**
```bash
# Edit file to resolve conflicts
# Remove conflict markers
# Keep desired changes

git add modules/conflicted_file.py
git commit -m "fix: resolve merge conflict"
```

**4. Complete Merge**
```bash
git merge --continue
# or
git rebase --continue
```

---

## 📊 PULL REQUEST WORKFLOW

### Creating a Pull Request

**1. Push Feature Branch**
```bash
git push -u origin feature/new-module
```

**2. Create PR on GitHub**
- Go to repository
- Click "New Pull Request"
- Select `feature/new-module` → `develop`
- Add title and description
- Click "Create Pull Request"

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Testing
- [ ] Unit tests added
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

### Code Review Process

**1. Reviewer Reviews Code**
- Check code quality
- Verify tests
- Check documentation
- Request changes if needed

**2. Author Addresses Feedback**
```bash
# Make requested changes
git add .
git commit -m "review: address feedback"
git push origin feature/new-module
```

**3. Approval & Merge**
- Reviewer approves
- Merge PR to develop
- Delete feature branch

---

## 🔐 SECURITY BEST PRACTICES

### Protecting Sensitive Data

**1. Never Commit Secrets**
```bash
# .gitignore
.env
.env.local
*.key
*.pem
secrets.json
```

**2. Use Environment Variables**
```bash
# .env (never commit)
OPENAI_API_KEY=sk_...
STRIPE_API_KEY=sk_...
DATABASE_URL=postgresql://...
```

**3. Scan for Secrets**
```bash
# Install git-secrets
brew install git-secrets

# Scan repository
git secrets --scan

# Prevent commits with secrets
git secrets --install
```

### Branch Protection

**1. Protect Main Branch**
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Dismiss stale pull request approvals

**2. Protect Develop Branch**
- Require pull request reviews
- Require status checks to pass

---

## 🤖 CI/CD INTEGRATION

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/
    - name: Run linting
      run: |
        pylint modules/
```

### Automated Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: docker build -t kontrollzentrum:latest .
    - name: Push to registry
      run: docker push kontrollzentrum:latest
    - name: Deploy to Kubernetes
      run: kubectl apply -f kubernetes.yml
```

---

## 📚 RESOURCES

### Git Documentation
- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)

### Tools
- **Git GUI**: GitHub Desktop, GitKraken, SourceTree
- **IDE Integration**: VS Code, PyCharm, Visual Studio
- **Git Hooks**: Husky, Pre-commit

---

## ✅ CHECKLIST

Before committing:
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] No debug code left
- [ ] No secrets in code
- [ ] Documentation updated
- [ ] Commit message is clear

Before pushing:
- [ ] Branch is up to date
- [ ] All tests pass
- [ ] No conflicts
- [ ] Ready for review

Before merging:
- [ ] Code review approved
- [ ] CI/CD passes
- [ ] Tests pass
- [ ] Documentation complete

---

**🚀 Ready for Collaborative Development!**

Nächster Schritt: Team Training durchführen
