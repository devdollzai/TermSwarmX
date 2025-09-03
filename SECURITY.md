# 🔒 Security Guide - DevDollz Atelier Edition

## 🚨 IMPORTANT: Never Commit Secrets!

This repository is designed to be **100% safe** for public sharing. All sensitive information is properly excluded and protected.

## 🛡️ What's Protected

### ✅ Automatically Ignored (Safe to Commit)
- Source code
- Documentation
- Configuration templates
- Example files
- Tests

### ❌ Never Committed (Automatically Protected)
- `.env` files
- API keys and secrets
- Database files (`*.db`)
- Memory files
- Personal configuration
- Access tokens
- Passwords

## 🔐 How to Use This Repository Safely

### 1. Environment Variables
Create a `.env` file in your local directory (never commit this):

```bash
# .env (LOCAL ONLY - NEVER COMMIT)
OLLAMA_API_KEY=your_actual_key_here
TWITTER_CONSUMER_KEY=your_twitter_key
TWITTER_CONSUMER_SECRET=your_twitter_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
```

### 2. Configuration Files
Use the provided template files:
- `config_template.py` → Copy to `config.py` and add your secrets
- `devdollz/constants_template.py` → Copy to `devdollz/constants.py`

### 3. Database Files
All `.db` files are automatically ignored. Create your own locally.

## 🚫 What NOT to Do

```bash
# ❌ NEVER do this:
git add .env
git add *.db
git add config.py  # if it contains secrets
git commit -m "added my secrets"  # NEVER!

# ✅ ALWAYS do this:
git add .gitignore
git add SECURITY.md
git add config_template.py
git add *.py  # source code only
```

## 🔍 Verification Commands

Before committing, verify no secrets are included:

```bash
# Check what will be committed
git status

# Check for any .env files
find . -name ".env" -type f

# Check for database files
find . -name "*.db" -type f

# Review staged changes
git diff --cached
```

## 🆘 If You Accidentally Commit Secrets

1. **IMMEDIATELY** revoke/rotate the exposed secrets
2. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch .env' \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push: `git push --force-with-lease origin main`
4. **ALWAYS** rotate the exposed secrets

## 📋 Security Checklist

Before pushing to public:
- [ ] `.env` file exists locally but is NOT committed
- [ ] No API keys in source code
- [ ] No passwords in source code
- [ ] No database files committed
- [ ] `.gitignore` is properly configured
- [ ] `SECURITY.md` is committed
- [ ] All template files are committed
- [ ] No personal information in code

## 🎯 Safe Public Sharing

This repository is designed to be:
- ✅ **100% safe** for public viewing
- ✅ **Educational** for other developers
- ✅ **Secure** by design
- ✅ **Professional** and well-documented

## 📞 Security Issues

If you find a security vulnerability:
1. **DO NOT** create a public issue
2. **DO** contact the maintainer privately
3. **DO** provide detailed reproduction steps

---

**Remember: When in doubt, don't commit it!** 🔒
