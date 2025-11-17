# Render Qdrant Connection Fix

## 🚨 Problem

**Error:** `Qdrant search error: [Errno -2] Name or service not known`

This means the Qdrant URL cannot be resolved (DNS/network issue).

---

## ✅ Solution: Set QDRANT_URL in Render

### Step 1: Get Your Qdrant URL

**If using Qdrant Cloud:**
- Go to your Qdrant Cloud dashboard
- Copy your cluster URL (e.g., `https://xxxxx-xxxxx.qdrant.io`)

**If using self-hosted Qdrant:**
- Use your Qdrant server URL (e.g., `http://your-qdrant-server.com:6333`)

### Step 2: Set Environment Variables in Render

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Select your service: `tax-memo-backend`

2. **Go to Environment Tab:**
   - Click "Environment" in the sidebar
   - Scroll to "Environment Variables"

3. **Add/Update Qdrant Variables:**
   - **QDRANT_URL:** Your Qdrant URL
     - Example: `https://xxxxx-xxxxx.qdrant.io`
     - Or: `http://your-qdrant-server.com:6333`
   
   - **QDRANT_API_KEY:** Your Qdrant API key (if using Qdrant Cloud)
     - Get from Qdrant Cloud dashboard
     - Leave empty if using self-hosted without auth

4. **Save Changes:**
   - Click "Save Changes"
   - Render will automatically redeploy

---

## 🔍 Verify Configuration

### Check Environment Variables

In Render Dashboard → Environment tab, verify:

```
✅ OPENAI_API_KEY = your_openai_key
✅ QDRANT_URL = https://your-qdrant-url.qdrant.io
✅ QDRANT_API_KEY = your_qdrant_api_key (if using Qdrant Cloud)
```

### Test Connection

After redeploy, check logs:
- Should see: "Qdrant connection successful" (or no errors)
- Should NOT see: "Name or service not known"

---

## 🛠️ Alternative: Check Qdrant Service Status

### If Using Qdrant Cloud:
1. Check Qdrant Cloud dashboard
2. Verify cluster is running
3. Verify URL is correct

### If Using Self-Hosted:
1. Check if Qdrant server is running
2. Verify URL is accessible from Render
3. Check firewall/network settings

---

## 📝 Current Behavior

**With Qdrant Error:**
- System continues without Qdrant context
- Uses LLM knowledge only (still works, but less accurate)
- Memos still generate successfully

**After Fix:**
- System uses Qdrant for context retrieval
- More accurate and context-aware memos
- Better recommendations

---

## 🔧 Quick Fix Commands

If you have access to Render shell:

```bash
# Check environment variables
echo $QDRANT_URL
echo $QDRANT_API_KEY

# Test Qdrant connection
curl $QDRANT_URL/collections
```

---

## ✅ Expected Result After Fix

**Before:**
```
Qdrant search error: [Errno -2] Name or service not known
Found 0 search results
```

**After:**
```
Searching Qdrant with query: ...
Found 5 search results
```

---

## 🎯 Summary

**Problem:** QDRANT_URL not set or incorrect in Render  
**Solution:** Set QDRANT_URL and QDRANT_API_KEY in Render Environment Variables  
**Status:** System works without Qdrant, but better with it

---

**Next Step:** Set QDRANT_URL in Render Dashboard → Environment tab

