# 📚 Documentation Guide

This guide explains which documentation files should be shared (pushed to git) and which should remain private (ignored).

---

## ✅ **PUSH to Git** (Team Documentation)

Public documentation that should be shared with all team members and contributors:

```
README.md                    ✅ Main project documentation
SECURITY.md                  ✅ Security guidelines & best practices
GIT_PUSH_SETUP.md           ✅ Git setup instructions
README_DEPLOYMENT.md        ✅ Deployment & environment setup
GITIGNORE_GUIDE.md          ✅ Git ignore guide
DOCUMENTATION_GUIDE.md      ✅ This file (documentation standards)
```

**These files are:**
- Part of the public repository
- Visible on GitHub
- Essential for team onboarding
- Referenced in README
- Updated collaboratively

---

## ❌ **DO NOT PUSH** (Ignored by Git)

Private/internal documentation that stays local:

### Draft/Temporary Files
```
NOTES.md                     ❌ Personal research notes
TODO.md                      ❌ Internal task tracking
SCRATCH.md                   ❌ Scratch/experimental ideas
*.draft.md                   ❌ Draft documentation
*.tmp.md                     ❌ Temporary notes
```

### Internal Folders
```
INTERNAL/                    ❌ Internal documentation folder
docs-internal/               ❌ Private documentation
private-docs/                ❌ Private documentation
```

### Examples
```
project-planning.draft.md    ❌ Ignored
team-notes.md                ❌ Ignored (not in repo)
NOTES.md                     ❌ Ignored
TODO.md                       ❌ Ignored
SCRATCH.md                    ❌ Ignored
internal-architecture.md     ❌ Ignored (in INTERNAL/ folder)
```

---

## 📖 **Documentation File Types**

### Public Documentation (Push ✅)

**README.md**
- Project overview
- Features
- Quick start guide
- Tech stack
- Troubleshooting
- For: All users & contributors

**SECURITY.md**
- Security guidelines
- API key protection
- Environment variables
- Best practices
- For: Developers & DevOps

**GIT_PUSH_SETUP.md**
- Git configuration
- Branching strategy
- Commit guidelines
- Push instructions
- For: Team members

**README_DEPLOYMENT.md**
- Deployment procedures
- Environment setup
- Production checklist
- For: DevOps & developers

**GITIGNORE_GUIDE.md**
- What to push/ignore
- File explanations
- Git safety rules
- For: All developers

---

### Private Documentation (Ignore ❌)

**NOTES.md**
- Personal research
- Investigation notes
- Design exploration
- For: Personal use only

**TODO.md**
- Internal task lists
- Work tracking
- Private reminders
- For: Personal use only

**SCRATCH.md**
- Experimental ideas
- Draft content
- Temporary thoughts
- For: Personal use only

**INTERNAL/ folder**
- Internal architecture notes
- Private decisions
- Non-shareable research
- For: Team internal use

---

## 🎯 **How to Use**

### Creating Public Documentation
```bash
# Create in root directory
touch NEW_PUBLIC_GUIDE.md
git add NEW_PUBLIC_GUIDE.md
git commit -m "Add new documentation guide"
git push
```

### Creating Private Documentation
```bash
# Option 1: Use ignored file names
touch NOTES.md              # Automatically ignored
touch TODO.md               # Automatically ignored
touch SCRATCH.md            # Automatically ignored

# Option 2: Use ignored file patterns
touch my-research.draft.md  # Matches *.draft.md pattern
touch my-ideas.tmp.md       # Matches *.tmp.md pattern

# Option 3: Use ignored folders
mkdir INTERNAL
touch INTERNAL/private.md   # Folder is ignored

# Verify it won't be pushed
git status | grep ".md"     # Should NOT show ignored files
```

---

## ✨ **Best Practices**

### For Public Documentation
- ✅ Keep organized and clear
- ✅ Include code examples
- ✅ Update with changes
- ✅ Link between docs
- ✅ Use consistent formatting

### For Private Documentation
- ✅ Use for quick notes
- ✅ Keep experimental ideas
- ✅ Track personal progress
- ✅ Not part of official docs
- ✅ Can be messy/informal

---

## 📋 **Checklist Before Pushing**

```bash
# Verify only public docs will be pushed
git status | grep "\.md"
# Should show ONLY:
# - README.md
# - SECURITY.md
# - GIT_PUSH_SETUP.md
# - README_DEPLOYMENT.md
# - GITIGNORE_GUIDE.md
# - DOCUMENTATION_GUIDE.md

# Should NOT show:
# - NOTES.md
# - TODO.md
# - SCRATCH.md
# - *.draft.md
# - *.tmp.md
```

---

## 🔄 **Example Workflows**

### Adding a New Public Guide
```bash
# Create the guide
nano NEW_GUIDE.md

# Add content
# Save and exit

# Add to git
git add NEW_GUIDE.md

# Commit
git commit -m "Add new guide: [title]"

# Push
git push
```

### Taking Personal Notes
```bash
# Create notes (automatically ignored)
nano NOTES.md

# Add whatever you want
# No need to worry about git

# These stay local only
# Not visible to others
```

### Draft Documentation
```bash
# Create draft
nano feature-design.draft.md

# Work on it locally
# Refine the content

# When ready, rename to public
mv feature-design.draft.md FEATURE_DESIGN.md

# Then add to git
git add FEATURE_DESIGN.md
git commit -m "Add feature design documentation"
git push
```

---

## 📊 **Current Ignored Patterns**

View `.gitignore` to see all ignored patterns:

```bash
cat .gitignore

# Documentation - Internal/Draft section should show:
NOTES.md
TODO.md
SCRATCH.md
*.draft.md
*.tmp.md
INTERNAL/
docs-internal/
private-docs/
```

---

## 🚀 **Deploying Only Public Docs**

When deploying, only these files are included:
- README.md
- SECURITY.md
- GIT_PUSH_SETUP.md
- README_DEPLOYMENT.md
- GITIGNORE_GUIDE.md
- DOCUMENTATION_GUIDE.md

Private docs never reach GitHub or production.

---

## 💡 **Examples**

### ✅ Good: Personal Notes (Ignored)
```bash
# File: NOTES.md
Investigation into performance optimization:
- Tried caching approach
- Results showed 10% improvement
- Need to test under load
- TODO: benchmark with larger datasets
```

### ✅ Good: Public Documentation (Pushed)
```bash
# File: PERFORMANCE_GUIDE.md
## Performance Optimization

### Caching Strategy
We implemented a caching layer that improves response times by 10%.

### Implementation
[Details here...]

### Results
[Metrics here...]
```

### ❌ Bad: Pushing Private Notes
```bash
# File: NOTES.md (in git - WRONG!)
Random thoughts about the project...
Not suitable for public repository
```

---

## 📞 **Questions?**

- Check `.gitignore` for current patterns
- Read the ignored file names/patterns
- When in doubt, put in `INTERNAL/` folder
- Use `.draft.md` suffix for draft files

---

## ✅ **Summary**

| Type | Action | Example |
|------|--------|---------|
| Public docs | ✅ PUSH | README.md, SECURITY.md |
| Private notes | ❌ IGNORE | NOTES.md, TODO.md |
| Draft content | ❌ IGNORE | *.draft.md, *.tmp.md |
| Internal docs | ❌ IGNORE | INTERNAL/ folder |

**Rule of thumb:** If it's not for the whole team → ignore it!

---

**Last Updated:** 2026-06-17
