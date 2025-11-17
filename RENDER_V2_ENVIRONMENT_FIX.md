# 🔧 V2 Qdrant Fix - Environment Variables Not Migrated

## 🚨 Problem

**Error:** `Qdrant search error: [Errno -2] Name or service not known`

**Root Cause:** When deploying V2, the environment variables from V1 were not automatically copied. The `QDRANT_URL` is either:
- Not set in the new V2 deployment
- Set incorrectly
- Missing from Render environment variables

---

## ✅ Quick Fix (3 Steps)

### Step 1: Check Current Status

**Test the health endpoint:**
```bash
curl https://taxmemov2.onrender.com/health
```

**Look for:**
```json
{
  "qdrant": {
    "status": "not_configured",  // ← This means QDRANT_URL is missing
    "url_from_env": "NOT SET",    // ← This confirms it
    "diagnostic": "Go to Render Dashboard → Environment → Add QDRANT_URL"
  }
}
```

### Step 2: Get Your Qdrant URL from V1

**Option A: Check V1 Render Service**
1. Go to: https://dashboard.render.com
2. Find your **V1 service** (old deployment)
3. Click **"Environment"** tab
4. Copy the `QDRANT_URL` value
5. Copy the `QDRANT_API_KEY` value (if set)

**Option B: Check Qdrant Cloud Dashboard**
1. Go to: https://cloud.qdrant.io/
2. Sign in
3. Select your cluster
4. Copy the **Cluster URL** (e.g., `https://xxxxx-xxxxx.qdrant.io`)
5. Copy the **API Key**

### Step 3: Set Environment Variables in V2 Render Service

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Select your **V2 service**: `tax-memo-backend` (or your service name)

2. **Go to Environment Tab:**
   - Click **"Environment"** in the left sidebar
   - Scroll to **"Environment Variables"** section

3. **Add/Update Variables:**

   **QDRANT_URL** (Required)
   - Click **"Add Environment Variable"** (if not exists)
   - **Key:** `QDRANT_URL`
   - **Value:** Paste your Qdrant URL from Step 2
     - Format: `https://xxxxx-xxxxx.qdrant.io` (Qdrant Cloud)
     - Or: `http://your-server:6333` (Self-hosted)
   - Click **"Save"**

   **QDRANT_API_KEY** (If using Qdrant Cloud)
   - Click **"Add Environment Variable"** (if not exists)
   - **Key:** `QDRANT_API_KEY`
   - **Value:** Paste your Qdrant API key from Step 2
   - Click **"Save"**

4. **Verify OPENAI_API_KEY:**
   - Make sure `OPENAI_API_KEY` is also set
   - If missing, add it from your V1 service

5. **Save and Redeploy:**
   - Render will automatically redeploy after saving
   - Wait 2-3 minutes for deployment

---

## 🔍 Verify Fix

### Test Health Endpoint Again:
```bash
curl https://taxmemov2.onrender.com/health
```

### Expected Result:
```json
{
  "status": "healthy",
  "qdrant": {
    "status": "connected",           // ✅ Connected!
    "url_from_env": "https://xxx...", // ✅ URL is set
    "connected": true                 // ✅ Working!
  }
}
```

### Test Memo Generation:
- Generate a memo through the API
- Check logs - should see:
  ```
  ✅ Qdrant connection successful
  Found 5 search results  // Instead of "Found 0"
  ```

---

## 📋 Environment Variables Checklist

In Render Dashboard → Environment tab, verify all three are set:

- [ ] `OPENAI_API_KEY` = `sk-...` ✅
- [ ] `QDRANT_URL` = `https://...` or `http://...` ✅
- [ ] `QDRANT_API_KEY` = `...` (if using Qdrant Cloud) ✅

---

## 🎯 Common Issues

### Issue 1: "NOT SET" in health endpoint
**Solution:** QDRANT_URL is not set. Follow Step 3 above.

### Issue 2: "Name or service not known" still appears
**Possible causes:**
- URL format wrong (missing `https://` or `http://`)
- URL has trailing slash (remove it)
- URL is incorrect

**Fix:**
- Correct format: `https://abc123-def456.qdrant.io`
- Wrong: `abc123-def456.qdrant.io` (missing https://)
- Wrong: `https://abc123-def456.qdrant.io/` (trailing slash)

### Issue 3: Variables set but still not working
**Solution:**
1. Check Render logs for startup errors
2. Verify variables are saved (refresh Render page)
3. Try manual redeploy: "Manual Deploy" → "Deploy latest commit"

---

## 🔄 Copy from V1 to V2 (Quick Method)

If you have both V1 and V2 services in Render:

1. **V1 Service:**
   - Go to Environment tab
   - Note down: `QDRANT_URL`, `QDRANT_API_KEY`, `OPENAI_API_KEY`

2. **V2 Service:**
   - Go to Environment tab
   - Add each variable with the same values
   - Save

---

## ✅ Summary

**Problem:** V2 deployment doesn't have QDRANT_URL from V1  
**Solution:** Copy environment variables from V1 to V2 in Render Dashboard  
**Time:** 5 minutes  
**Result:** Qdrant connection restored, memos use knowledge base context

---

## 🚀 Next Steps

After fixing:
1. ✅ Test health endpoint: `curl https://taxmemov2.onrender.com/health`
2. ✅ Generate a test memo
3. ✅ Verify logs show "Found 5 search results"

**Status:** Ready to use! 🎉

