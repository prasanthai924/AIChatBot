# 🔐 Security Guidelines

## Environment Variables

**NEVER** commit `.env` files to git. They contain sensitive information like API keys.

### Setup Instructions

#### 1. **Backend Setup**

```bash
cd backend

# Copy the example file
cp .env.example .env

# Edit .env and add your real API key
nano .env
```

**`.env` content (do NOT commit this file):**
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

#### 2. **Frontend Setup** (if needed)

```bash
# Copy example
cp .env.example .env.local

# Edit if needed
nano .env.local
```

---

## Sensitive Files to Ignore

The `.gitignore` file already excludes:
- ✅ `.env` - Main environment file
- ✅ `.env.local` - Local overrides
- ✅ `backend/.env` - Backend secrets
- ✅ `backend/venv/` - Virtual environment

---

## Best Practices

### ✅ DO:
- Store API keys in `.env` files
- Use `.env.example` as a template
- Add `.env` to `.gitignore`
- Document required variables in `.env.example`
- Use environment variables in code

```python
# ✅ Good: Read from environment
api_key = os.getenv("OPENWEATHER_API_KEY")
```

### ❌ DON'T:
- Hardcode API keys in source files
- Commit `.env` files
- Share API keys in chats or emails
- Use the same key for development and production

```python
# ❌ Bad: Hardcoded key
api_key = "abc123xyz789"  # NEVER DO THIS!
```

---

## If You Accidentally Committed a Secret

If you already pushed a `.env` file with an API key:

1. **Regenerate the API key** (make the old one invalid)
2. **Remove from git history:**
   ```bash
   git rm --cached backend/.env
   git commit -m "Remove .env from tracking"
   git push
   ```
3. **Add to .gitignore** (already done)

---

## Setting Up for Git Push

### Step 1: Verify .gitignore is correct
```bash
git check-ignore backend/.env
# Should output: backend/.env (if properly ignored)
```

### Step 2: Check what will be committed
```bash
git status
# Should NOT show .env files
```

### Step 3: Remove .env from git if already tracked
```bash
git rm --cached backend/.env
git commit -m "Remove .env file from git tracking"
```

### Step 4: Push to GitHub
```bash
git add .gitignore SECURITY.md
git commit -m "Add security guidelines and update gitignore"
git push origin main
```

---

## Environment Variables Reference

### Backend (.env)
| Variable | Source | Purpose |
|----------|--------|---------|
| `OPENWEATHER_API_KEY` | https://openweathermap.org/api | Weather data API |

### Adding New Secrets

When adding new API keys or secrets:

1. Add to `.env.example` with placeholder:
   ```env
   NEW_API_KEY=your_key_here
   ```

2. Add to `.gitignore` if not already covered

3. Load in code:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv("NEW_API_KEY")
   ```

---

## GitHub Secret Management

For CI/CD pipelines, use GitHub Secrets:

1. Go to: Repository → Settings → Secrets
2. Add `OPENWEATHER_API_KEY`
3. Use in workflows: `${{ secrets.OPENWEATHER_API_KEY }}`

---

## Deployment Checklist

Before deploying to production:

- [ ] All secrets in `.env`, not in code
- [ ] `.env` in `.gitignore`
- [ ] No `.env` files in git history
- [ ] Production secrets set in deployment platform
- [ ] API keys rotated if exposed
- [ ] HTTPS enabled
- [ ] CORS properly configured

---

**Last Updated:** 2026-06-17
