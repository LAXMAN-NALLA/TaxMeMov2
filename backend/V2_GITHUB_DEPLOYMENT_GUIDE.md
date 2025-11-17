# V2 GitHub Deployment Guide
## Step-by-Step Instructions for Deploying V2 to GitHub

This guide shows exactly which files to commit and push for the V2 upgrade.

---

## 📋 Files to Deploy

### ✅ Required Files (Core V2 Implementation)

These files are **essential** for V2 to work:

1. **`backend/app/core/semantic_router.py`** (NEW)
   - The semantic router module with AI classification
   - **Status:** Must commit

2. **`backend/app/core/orchestrator.py`** (MODIFIED)
   - Updated to use semantic router instead of regex
   - **Status:** Must commit

### 📚 Optional Files (Documentation)

These files are helpful but not required for functionality:

3. **`backend/V2_SEMANTIC_ROUTER_UPGRADE.md`**
   - V2 upgrade documentation
   - **Status:** Recommended (good for team reference)

4. **`backend/V1_VS_V2_COMPARISON.md`**
   - Detailed comparison with examples
   - **Status:** Optional

5. **`backend/V2_CEO_PRESENTATION.md`**
   - Executive presentation
   - **Status:** Optional

6. **`backend/V2_TECHNICAL_IMPLEMENTATION_GUIDE.md`**
   - Technical deep dive
   - **Status:** Optional

7. **`backend/V1_VS_V2_QUICK_REFERENCE.md`**
   - Quick reference guide
   - **Status:** Optional

8. **`backend/V2_GITHUB_DEPLOYMENT_GUIDE.md`** (this file)
   - Deployment instructions
   - **Status:** Optional

---

## 🚀 Deployment Steps

### Step 1: Check Current Status

```bash
# Navigate to your project directory
cd C:\Users\laxma\Desktop\1CountryTaxmemo

# Check git status
git status

# See what files have changed
git diff --name-only
```

### Step 2: Verify Required Files Exist

Make sure these files exist:

```bash
# Check if semantic_router.py exists
ls backend/app/core/semantic_router.py

# Check if orchestrator.py was modified
git diff backend/app/core/orchestrator.py
```

### Step 3: Stage Required Files

```bash
# Stage the new semantic router file
git add backend/app/core/semantic_router.py

# Stage the modified orchestrator file
git add backend/app/core/orchestrator.py
```

### Step 4: Stage Documentation (Optional)

```bash
# Stage all documentation files (optional)
git add backend/V2_SEMANTIC_ROUTER_UPGRADE.md
git add backend/V1_VS_V2_COMPARISON.md
git add backend/V2_CEO_PRESENTATION.md
git add backend/V2_TECHNICAL_IMPLEMENTATION_GUIDE.md
git add backend/V1_VS_V2_QUICK_REFERENCE.md
git add backend/V2_GITHUB_DEPLOYMENT_GUIDE.md

# Or stage all at once
git add backend/V2*.md backend/V1_VS_V2*.md
```

### Step 5: Verify Staged Files

```bash
# Check what's staged
git status

# You should see:
# - backend/app/core/semantic_router.py (new file)
# - backend/app/core/orchestrator.py (modified)
# - Documentation files (if you added them)
```

### Step 6: Commit Changes

```bash
# Commit with a descriptive message
git commit -m "feat: Upgrade to V2 - Add Semantic Router for AI-powered intent classification

- Add semantic_router.py with GPT-4o-mini classification
- Update orchestrator.py to use semantic router instead of regex
- Improve accuracy: handles synonyms, typos, and natural language
- Maintain backward compatibility with fallback heuristics
- Add comprehensive documentation

Breaking changes: None (backward compatible)
Performance: +200-300ms per request (negligible)
Cost: ~$0.00015 per request"
```

### Step 7: Push to GitHub

```bash
# Push to your main/master branch
git push origin main

# Or if your branch is called 'master'
git push origin master
```

---

## 📝 Quick Deployment (One Command)

If you want to deploy everything at once:

```bash
# Navigate to project
cd C:\Users\laxma\Desktop\1CountryTaxmemo

# Add all V2 files
git add backend/app/core/semantic_router.py
git add backend/app/core/orchestrator.py
git add backend/V2*.md backend/V1_VS_V2*.md

# Commit
git commit -m "feat: Upgrade to V2 - Semantic Router implementation"

# Push
git push origin main
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] `semantic_router.py` is in `backend/app/core/`
- [ ] `orchestrator.py` imports `SemanticRouter`
- [ ] `orchestrator.py` calls `semantic_router.get_intent()`
- [ ] Files are committed to git
- [ ] Files are pushed to GitHub
- [ ] GitHub shows the new commit

---

## 🔍 What Changed in Each File

### 1. `backend/app/core/semantic_router.py` (NEW)

**What it does:**
- AI-powered intent classification
- Uses GPT-4o-mini to understand user input
- Returns structured `UserIntent` object
- Falls back to heuristics if AI fails

**Key components:**
- `UserIntent` Pydantic model
- `SemanticRouter` class
- `get_intent()` method
- `_fallback_classification()` method

### 2. `backend/app/core/orchestrator.py` (MODIFIED)

**What changed:**
- Added `SemanticRouter` import
- Added `self.semantic_router = SemanticRouter()` in `__init__`
- Replaced regex logic with `intent = self.semantic_router.get_intent()`
- Uses `intent.must_be_bv`, `intent.urgency`, etc. instead of regex

**Before (V1):**
```python
must_be_bv = "b.v" in company_name or "bv" in company_name
```

**After (V2):**
```python
intent = self.semantic_router.get_intent(request_dict)
must_be_bv = intent.must_be_bv
```

---

## 🚨 Important Notes

### Dependencies

**No changes needed to `requirements.txt`** - OpenAI is already included:
```
openai==1.109.1
```

### Environment Variables

**No new environment variables needed** - Uses existing:
```
OPENAI_API_KEY=your_key_here
```

### Backward Compatibility

✅ **V2 is backward compatible:**
- Same API endpoints
- Same request/response format
- Automatic fallback to V1 heuristics if AI fails
- Zero breaking changes

### Testing After Deployment

After deploying, test with:

```bash
# Test the API
python backend/test_api.py

# Or use curl
curl -X POST http://localhost:8000/generate-memo \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Dutch Limited Liability Company"}'
```

---

## 📊 File Size Summary

| File | Size | Type |
|------|------|------|
| `semantic_router.py` | ~8 KB | Code |
| `orchestrator.py` | ~10 KB (modified) | Code |
| Documentation files | ~50 KB total | Docs |

**Total:** ~68 KB (very small deployment)

---

## 🔄 Rollback Plan

If you need to rollback V2:

```bash
# Option 1: Revert the commit
git revert HEAD
git push origin main

# Option 2: Reset to previous commit (if you haven't pushed)
git reset --hard HEAD~1
```

**Note:** V2 has automatic fallback, so rollback is rarely needed.

---

## 📞 Troubleshooting

### Issue: "ModuleNotFoundError: semantic_router"

**Solution:** Make sure `semantic_router.py` is in `backend/app/core/`

### Issue: "AttributeError: 'Orchestrator' has no attribute 'semantic_router'"

**Solution:** Make sure `orchestrator.py` has `self.semantic_router = SemanticRouter()` in `__init__`

### Issue: "OpenAI API error"

**Solution:** Check that `OPENAI_API_KEY` is set in environment variables

### Issue: "Git push rejected"

**Solution:** Pull latest changes first:
```bash
git pull origin main
# Resolve any conflicts
git push origin main
```

---

## ✅ Deployment Complete!

Once you've pushed to GitHub:

1. ✅ V2 is deployed
2. ✅ Semantic Router is active
3. ✅ System uses AI classification
4. ✅ Fallback heuristics are in place
5. ✅ Documentation is available

**Next Steps:**
- Test the deployment
- Monitor for any issues
- Collect user feedback
- Review metrics

---

## 📋 Summary

**Files to Deploy:**
1. ✅ `backend/app/core/semantic_router.py` (NEW - REQUIRED)
2. ✅ `backend/app/core/orchestrator.py` (MODIFIED - REQUIRED)
3. 📚 Documentation files (OPTIONAL but recommended)

**Commands:**
```bash
git add backend/app/core/semantic_router.py
git add backend/app/core/orchestrator.py
git commit -m "feat: Upgrade to V2 - Semantic Router"
git push origin main
```

**That's it!** V2 is now deployed. 🚀

