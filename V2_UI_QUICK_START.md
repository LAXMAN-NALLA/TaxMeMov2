# V2 UI Quick Start Guide

## 🚀 Simple Test UI for V2

I've created a simple Streamlit UI specifically for testing V2 features.

---

## 📋 Files

- **`streamlit_app_v2.py`** - Simple V2 test UI (NEW)
- **`streamlit_app.py`** - Original V1 UI (still works)

---

## 🏃 Quick Start

### Step 1: Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Start the FastAPI server
uvicorn app.main:app --reload
```

The server will run at: `http://localhost:8000`

### Step 2: Start Streamlit UI

```bash
# In a new terminal, from project root
streamlit run streamlit_app_v2.py
```

The UI will open in your browser at: `http://localhost:8501`

---

## 🧪 How to Test V2

### Option 1: Use Pre-built Test Cases

1. Open the UI
2. Select a test case from the dropdown:
   - **Test 1:** Synonym Recognition ("Dutch Limited Liability Company")
   - **Test 2:** Natural Language Urgency ("I need this ASAP")
   - **Test 3:** Holding Company Context
   - **Test 4:** Tech Industry Detection
   - **Test 5:** Complex Natural Language

3. Click **"🚀 Generate Memo with V2"**

### Option 2: Custom Input

1. Fill in the form:
   - **Company Name:** Try "Dutch Limited Liability Company" (tests synonym recognition)
   - **Timeline:** Try "I need this very urgently" (tests natural language)
   - **Additional Context:** Add natural language description

2. Click **"🚀 Generate Memo with V2"**

---

## ✨ What to Test

### Test 1: Synonym Recognition
**Input:**
```
Company Name: "Dutch Limited Liability Company"
Industry: "Software & Technology"
```

**Expected:** V2 should recognize this as BV intent (V1 would fail)

### Test 2: Natural Language Urgency
**Input:**
```
Company Name: "Speed Corp"
Timeline: "I need this done very urgently, ASAP"
```

**Expected:** V2 should detect HIGH urgency

### Test 3: Context Understanding
**Input:**
```
Company Name: "Global Holdings"
Tax Considerations: ["participation exemption"]
```

**Expected:** V2 should detect holding company intent

---

## 📊 What You'll See

1. **Request Preview** - See what's being sent to the API
2. **V2 Classification Info** - Shows what V2 understood
3. **Generated Memo** - Full memo with recommendations
4. **Download Option** - Download as JSON

---

## 🔍 Key Differences from V1 UI

| Feature | V1 UI | V2 UI |
|---------|-------|-------|
| **Focus** | Full form (5 steps) | Simple test interface |
| **Test Cases** | None | 5 pre-built test cases |
| **V2 Features** | Not highlighted | Clearly shown |
| **Complexity** | More fields | Minimal fields |
| **Purpose** | Production use | Testing V2 |

---

## 💡 Tips

1. **Start with Test Cases:** Use the pre-built test cases first
2. **Try Synonyms:** Test "Dutch Limited Liability Company" vs "B.V."
3. **Natural Language:** Try different ways of expressing urgency
4. **Check Results:** Look at the "V2 Classification Results" section

---

## 🐛 Troubleshooting

### "Could not connect to API"
- Make sure backend is running: `uvicorn app.main:app --reload`
- Check API URL in sidebar (should be `http://localhost:8000`)

### "Request timed out"
- Memo generation takes 30-60 seconds
- This is normal - wait for it to complete

### "ModuleNotFoundError: streamlit"
- Install streamlit: `pip install streamlit`

---

## 🎯 Quick Test Checklist

- [ ] Backend server running
- [ ] Streamlit UI running
- [ ] Test Case 1: Synonym recognition works
- [ ] Test Case 2: Natural language urgency works
- [ ] Custom input: Can enter own data
- [ ] Results: Memo displays correctly

---

## 📝 Example Test

**Try this:**

1. Select **"Test 1: Synonym Recognition"**
2. Click **"🚀 Generate Memo with V2"**
3. Wait 30-60 seconds
4. Check the memo - it should recommend BV structure
5. Compare: V1 would have failed on "Dutch Limited Liability Company"

**Success!** V2 is working! 🎉

---

**That's it!** The V2 UI is simple and focused on testing the new features.

