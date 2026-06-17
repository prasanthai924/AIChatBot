# 🚀 GitHub Actions Workflows

Automated CI/CD pipelines for testing, building, and securing your project.

---

## 📋 Available Workflows

### 1. **Frontend CI** (`frontend-ci.yml`)
Runs on every push/PR affecting frontend code.

**What it does:**
- ✅ Installs npm dependencies
- ✅ Lints TypeScript code
- ✅ Runs type checking
- ✅ Builds React app
- ✅ Checks for security vulnerabilities
- ✅ Tests with Node.js 16.x, 18.x, 20.x

**Triggered by:**
- Push to `main`, `master`, `develop`
- Changes in `src/`, `package.json`, `tsconfig.json`
- Pull requests to main branches

---

### 2. **Backend CI** (`backend-ci.yml`)
Runs on every push/PR affecting backend code.

**What it does:**
- ✅ Installs Python dependencies
- ✅ Lints Python code with flake8
- ✅ Type checks imports
- ✅ Runs security scan with Bandit
- ✅ Verifies `.env.example` exists
- ✅ Ensures `.env` is in `.gitignore`
- ✅ Tests with Python 3.8, 3.9, 3.10, 3.11

**Triggered by:**
- Push to `main`, `master`, `develop`
- Changes in `backend/`
- Pull requests to main branches

---

### 3. **Security Scan** (`security.yml`)
Comprehensive security checking.

**What it does:**
- ✅ Scans for secrets (API keys, tokens)
- ✅ Checks npm dependencies for vulnerabilities
- ✅ Verifies `.gitignore` rules
- ✅ Ensures `.env` files aren't tracked
- ✅ Checks code quality with ESLint

**Triggers:**
- On every push/PR
- Daily at 2 AM UTC (scheduled)

---

### 4. **CodeQL Analysis** (`codeql.yml`)
Static analysis for security vulnerabilities.

**What it does:**
- ✅ Analyzes JavaScript code
- ✅ Analyzes Python code
- ✅ Detects security issues
- ✅ Identifies code quality problems
- ✅ Uploads results to GitHub Security tab

**Triggers:**
- On every push/PR
- Daily at 3 AM UTC (scheduled)

---

### 5. **Documentation Check** (`documentation.yml`)
Ensures documentation quality.

**What it does:**
- ✅ Lints markdown files
- ✅ Verifies README.md exists
- ✅ Verifies SECURITY.md exists
- ✅ Checks all links are valid
- ✅ Ensures minimum documentation standards

**Triggers:**
- When markdown files change
- On every push/PR

---

## ✅ Status Badges

Add these to your README.md to show workflow status:

```markdown
![Frontend CI](https://github.com/YOUR_USERNAME/react-chat-frontend/actions/workflows/frontend-ci.yml/badge.svg)
![Backend CI](https://github.com/YOUR_USERNAME/react-chat-frontend/actions/workflows/backend-ci.yml/badge.svg)
![Security Scan](https://github.com/YOUR_USERNAME/react-chat-frontend/actions/workflows/security.yml/badge.svg)
```

---

## 🔍 Viewing Results

### On GitHub
1. Go to your repository
2. Click **Actions** tab
3. See all workflow runs
4. Click a workflow to see details

### On Pull Requests
Workflow results appear automatically on every PR:
- ✅ Passing checks show green
- ❌ Failing checks show red
- Can't merge until all checks pass

---

## 🛠️ Requirements

### Frontend
- Node.js 16.x, 18.x, or 20.x
- npm or yarn

### Backend
- Python 3.8+
- pip

### Both
- All dependencies in `requirements.txt` and `package.json`

---

## 🚨 Common Issues

### "npm ci fails"
```bash
# Ensure package-lock.json is committed
git add package-lock.json
git commit -m "Add package-lock.json"
```

### "Python import error"
```bash
# Ensure all imports can be resolved
# Check sys.path includes backend/ directory
```

### "ESLint warnings fail build"
```bash
# Max warnings is 10, fix linting issues
npm run lint --fix
```

### "Secret detected in repo"
```bash
# Review what was detected
# If it's a false positive, update .gitignore-gitleaks
# Remove actual secrets before pushing
```

---

## ⚙️ Customization

### Modify workflow triggers
Edit the `on:` section in any `.yml` file:

```yaml
on:
  push:
    branches: [main, develop]  # Add/remove branches
  pull_request:
    branches: [main]
```

### Add more checks
Add steps to any workflow file:

```yaml
- name: 📝 My Custom Check
  run: npm run my-check
```

### Disable a workflow
Rename the file or remove the `on:` section.

---

## 📊 Workflow Performance

| Workflow | Time | Frequency |
|----------|------|-----------|
| Frontend CI | ~2-3 min | Every push/PR |
| Backend CI | ~1-2 min | Every push/PR |
| Security | ~2 min | Every push/PR + daily |
| CodeQL | ~5-10 min | Every push/PR + daily |
| Documentation | ~1 min | Markdown changes |

---

## 🔐 Secrets & Tokens

Workflows use:
- `GITHUB_TOKEN` - Automatically provided by GitHub
- No external secrets needed for these workflows

For deployment workflows (future), you would add:
- `DEPLOY_KEY` - For deployment
- `API_KEYS` - For production services

---

## 📚 Documentation

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

---

## ✨ Next Steps

1. Push this branch to GitHub
2. Workflows run automatically
3. Check **Actions** tab to see results
4. Fix any failing checks
5. Merge when all checks pass

---

**Last Updated:** 2026-06-17
