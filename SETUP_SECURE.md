# 🔐 Secure Setup Guide - DevDollz Atelier Edition

## 🚀 Quick Start (Secure)

This guide will help you set up DevDollz Atelier Edition **100% securely** for public sharing.

## 📋 Prerequisites

- Python 3.8+
- Git
- Ollama (for local AI models)
- Twitter Developer Account (optional)

## 🔒 Step 1: Clone and Secure

```bash
# Clone the repository
git clone <your-repo-url>
cd AiTSwarmX

# Verify .gitignore is in place
ls -la .gitignore
```

## 🔐 Step 2: Create Environment File

**NEVER commit this file!**

```bash
# Create .env file (automatically ignored by git)
cat > .env << 'EOF'
# DevDollz: Atelier Edition - Environment Variables
# NEVER COMMIT THIS FILE!

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_API_KEY=your_ollama_api_key_here

# Twitter API (Optional)
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Development
DEV_DEBUG=false
LOG_LEVEL=INFO
MAX_THREADS=4
MEMORY_LIMIT=2GB
EOF

# Verify .env is created but not tracked
git status
# Should NOT show .env in tracked files
```

## ⚙️ Step 3: Configure Application

### Option A: Use Template Files (Recommended)

```bash
# Copy template files
cp config_template.py config.py
cp devdollz/constants_template.py devdollz/constants.py

# Edit with your secrets
nano config.py
nano devdollz/constants.py
```

### Option B: Create from Scratch

```bash
# Create config.py with your settings
nano config.py
# Add your configuration (see config_template.py for structure)

# Create constants.py
nano devdollz/constants.py
# Add your constants (see constants_template.py for structure)
```

## 🧪 Step 4: Test Configuration

```bash
# Test that secrets are loaded correctly
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OLLAMA_API_KEY:', '***' if os.getenv('OLLAMA_API_KEY') else 'NOT SET')
print('TWITTER_CONSUMER_KEY:', '***' if os.getenv('TWITTER_CONSUMER_KEY') else 'NOT SET')
"

# Test application startup
python demo_atelier.py
```

## 🔍 Step 5: Security Verification

Before committing, verify NO secrets are exposed:

```bash
# Check what will be committed
git status

# Search for potential secrets in staged files
git diff --cached | grep -i "api_key\|secret\|password\|token"

# Check for .env files
find . -name ".env" -type f

# Check for database files
find . -name "*.db" -type f

# Verify .gitignore is working
git check-ignore .env
git check-ignore *.db
```

## 🚫 Step 6: Remove Hardcoded Secrets

If you find any hardcoded secrets in the codebase:

```bash
# Search for hardcoded secrets
grep -r "api_key\|secret\|password\|token" . --exclude-dir=.git --exclude=*.db

# Replace with environment variables or remove
# Example: Replace hardcoded "devdolls" with os.getenv()
```

## 📤 Step 7: Safe Public Push

```bash
# Add all safe files
git add .

# Verify no secrets are included
git diff --cached

# Commit with security message
git commit -m "🔒 Secure public release - No secrets included

- Added comprehensive security documentation
- Included template configuration files
- Verified .gitignore protection
- All secrets properly externalized"

# Push to public repository
git push origin main
```

## 🛡️ Security Checklist

Before pushing publicly, verify:

- [ ] `.env` file exists locally but is NOT committed
- [ ] `config.py` contains your secrets but is NOT committed
- [ ] `devdollz/constants.py` contains your secrets but is NOT committed
- [ ] All `*.db` files are ignored
- [ ] No API keys in source code
- [ ] No passwords in source code
- [ ] `.gitignore` is properly configured
- [ ] `SECURITY.md` is committed
- [ ] Template files are committed
- [ ] No personal information exposed

## 🔧 Troubleshooting

### "File not found" errors
- Ensure you copied template files to actual config files
- Check file paths in your configuration

### "API key not found" errors
- Verify `.env` file exists and has correct format
- Check environment variable names match your code

### Git still tracking sensitive files
```bash
# Remove from git tracking (but keep local file)
git rm --cached .env
git rm --cached config.py
git rm --cached devdollz/constants.py
git rm --cached *.db

# Commit the removal
git commit -m "Remove sensitive files from tracking"
```

## 🎯 Best Practices

1. **Always use environment variables** for secrets
2. **Never hardcode** API keys or passwords
3. **Test locally** before pushing
4. **Use templates** for configuration
5. **Regular security audits** of your codebase
6. **Rotate secrets** periodically
7. **Monitor for accidental commits**

## 🆘 Emergency Response

If you accidentally commit secrets:

1. **IMMEDIATELY** revoke/rotate exposed secrets
2. **Remove from git history** (see SECURITY.md)
3. **Force push** to overwrite public history
4. **Notify affected services** of compromise
5. **Review security practices**

---

**Remember: Security is not optional - it's essential! 🔒**

Your DevDollz Atelier Edition is now ready for **100% secure public sharing**! 🚀
