# Render Environment Variables Setup

## 🚨 Current Issue

**Error:** `Qdrant search error: [Errno -2] Name or service not known`

**Cause:** QDRANT_URL environment variable is not set or incorrect in Render.

---

## ✅ Quick Fix (5 Minutes)

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Select your service: `tax-memo-backend` (or your service name)

### Step 2: Set Environment Variables
1. Click **"Environment"** tab (left sidebar)
2. Scroll to **"Environment Variables"** section
3. Add/Update these variables:

#### Required Variables:

**1. QDRANT_URL**
- **Key:** `QDRANT_URL`
- **Value:** Your Qdrant URL
  - Qdrant Cloud: `https://xxxxx-xxxxx.qdrant.io`
  - Self-hosted: `http://your-server.com:6333`
- **Example:** `https://abc123-def456.qdrant.io`

**2. QDRANT_API_KEY** (if using Qdrant Cloud)
- **Key:** `QDRANT_API_KEY`
- **Value:** Your Qdrant API key
- **Get it from:** Qdrant Cloud dashboard
- **Note:** Leave empty if using self-hosted without auth

**3. OPENAI_API_KEY** (should already be set)
- **Key:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key
- **Verify:** Make sure this is set correctly

### Step 3: Save and Redeploy
1. Click **"Save Changes"**
2. Render will automatically redeploy
3. Wait 2-3 minutes for deployment

---

## 🔍 Verify Fix

### Check Logs After Redeploy:

**Before Fix:**
```
Qdrant search error: [Errno -2] Name or service not known
Found 0 search results
```

**After Fix:**
```
Searching Qdrant with query: ...
Found 5 search results
```

### Test API:
```bash
curl https://taxmemov2.onrender.com/health
```

---

## 📋 Environment Variables Checklist

In Render Dashboard → Environment tab, verify:

- [ ] `OPENAI_API_KEY` = `sk-...` (your OpenAI key)
- [ ] `QDRANT_URL` = `https://...` or `http://...` (your Qdrant URL)
- [ ] `QDRANT_API_KEY` = `...` (if using Qdrant Cloud, otherwise leave empty)

---

## 🎯 Where to Get Qdrant URL

### If Using Qdrant Cloud:
1. Go to: https://cloud.qdrant.io/
2. Sign in to your account
3. Select your cluster
4. Copy the **Cluster URL** (e.g., `https://xxxxx-xxxxx.qdrant.io`)
5. Copy the **API Key** from the same page

### If Using Self-Hosted Qdrant:
- Use your Qdrant server URL
- Format: `http://your-server-ip:6333` or `https://your-domain.com`

---

## 🛠️ Troubleshooting

### Still Getting "Name or service not known"?

1. **Check URL Format:**
   - ✅ Correct: `https://abc123-def456.qdrant.io`
   - ❌ Wrong: `abc123-def456.qdrant.io` (missing https://)
   - ❌ Wrong: `http://abc123-def456.qdrant.io` (should be https for cloud)

2. **Check Qdrant Service:**
   - Verify Qdrant cluster is running (Qdrant Cloud dashboard)
   - Test URL in browser: `https://your-qdrant-url.qdrant.io/collections`

3. **Check Render Logs:**
   - Go to Render Dashboard → Logs
   - Look for Qdrant connection errors
   - Check if environment variables are loaded

4. **Redeploy:**
   - Sometimes a fresh deploy helps
   - Click "Manual Deploy" → "Deploy latest commit"

---

## ✅ Expected Result

After setting QDRANT_URL correctly:

- ✅ No more "Name or service not known" errors
- ✅ "Found 5 search results" instead of "Found 0"
- ✅ Memos include context from knowledge base
- ✅ Better accuracy and recommendations

---

## 📝 Summary

**Problem:** QDRANT_URL not set in Render  
**Solution:** Set QDRANT_URL (and QDRANT_API_KEY if needed) in Render Environment Variables  
**Time:** 5 minutes  
**Impact:** System works without Qdrant, but much better with it

---

**Next Step:** Go to Render Dashboard → Environment → Add QDRANT_URL

