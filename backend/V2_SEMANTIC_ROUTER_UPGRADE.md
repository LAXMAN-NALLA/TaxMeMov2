1# V2 Architecture Upgrade: Semantic Router Implementation

## 🚀 Overview

This document describes the V2 upgrade that replaces brittle regex/if-else logic with an AI-powered Semantic Router for intent classification.

## ✅ What Was Implemented

### 1. Semantic Router Module (`app/core/semantic_router.py`)

**New Component:** AI-powered intent classifier that understands natural language variations.

**Key Features:**
- Uses GPT-4o-mini for fast, cost-effective classification
- Handles synonyms ("Dutch Limited Liability Co" = BV)
- Resistant to typos and phrasing variations
- Fallback to heuristics if AI fails (backward compatibility)

**UserIntent Model:**
```python
class UserIntent(BaseModel):
    is_holding: bool
    must_be_bv: bool
    intent: str  # "SETUP", "ADVISORY", "COMPLIANCE"
    entity_type: Optional[str]  # "BV", "BRANCH", "HOLDING"
    urgency: str  # "HIGH", "MEDIUM", "LOW"
    industry_context: Optional[str]  # "TECH", "FINANCIAL", "GENERAL"
```

### 2. Orchestrator Upgrade (`app/core/orchestrator.py`)

**Before (V1):** Regex-based detection
```python
must_be_bv = (
    "b.v" in company_name or 
    "bv" in company_name or 
    "b.v." in company_name
)
```

**After (V2):** AI-powered classification
```python
intent = self.semantic_router.get_intent(request_dict)
must_be_bv = intent.must_be_bv
```

## 📊 Benefits

### 1. **Handles Synonyms**
- ✅ "Dutch Limited Liability Company" → correctly identifies as BV
- ✅ "Besloten Vennootschap" → correctly identifies as BV
- ✅ "I want a B.V. fast" → correctly identifies urgency + BV requirement

### 2. **Context-Aware**
- Understands that "holding company" + "participation exemption" = holding intent
- Distinguishes between generic "Corporation" (foreign) vs "Dutch BV" (explicit)

### 3. **Robust to Variations**
- Typos: "B.V" vs "BV" vs "B.V." → all work
- Phrasing: "I need a Dutch entity" vs "Set up a BV" → both understood

### 4. **Backward Compatible**
- Falls back to heuristics if AI classification fails
- Same task planning logic (no breaking changes)

## 🔄 How It Works

### Step 1: Request Processing
```python
# User sends request
request = TaxMemoRequest(
    company_name="Dutch Tech Solutions B.V.",
    industry="Software & Technology",
    timeline_preference="ASAP"
)
```

### Step 2: Semantic Router Classification
```python
# Orchestrator calls semantic router
intent = semantic_router.get_intent(request.model_dump())

# AI analyzes and returns:
# UserIntent(
#     is_holding=False,
#     must_be_bv=True,  # Detected "B.V." in name
#     entity_type="BV",
#     urgency="HIGH",  # Detected "ASAP"
#     industry_context="TECH"
# )
```

### Step 3: Task Planning
```python
# Orchestrator uses classified intent
if intent.must_be_bv:
    # Plan BV-specific tasks
elif intent.urgency == "HIGH":
    # Plan Branch Office tasks (fast setup)
```

## 🧪 Testing

### Test Case 1: Synonym Recognition
**Input:**
```json
{
  "company_name": "Dutch Limited Liability Co",
  "industry": "Technology"
}
```
**Expected:** `must_be_bv = True` (V1 would fail, V2 succeeds)

### Test Case 2: Context Understanding
**Input:**
```json
{
  "company_name": "Global Holdings Group",
  "company_type": "Holding Company",
  "tax_considerations": ["participation exemption"]
}
```
**Expected:** `is_holding = True`, `must_be_bv = True`

### Test Case 3: Urgency Detection
**Input:**
```json
{
  "company_name": "Speed Corp",
  "timeline_preference": "I need this ASAP, very urgent"
}
```
**Expected:** `urgency = "HIGH"`, `prioritizes_speed = True`

## 📝 API Compatibility

**No Breaking Changes:** The API endpoint `/generate-memo` works exactly the same. The upgrade is transparent to API consumers.

**Request Format:** Unchanged
```json
{
  "company_name": "Example Corp",
  "industry": "Software & Technology",
  "timeline_preference": "3 months"
}
```

**Response Format:** Unchanged (same memo structure)

## 🔧 Configuration

**Required Environment Variables:**
- `OPENAI_API_KEY` (already required for V1)

**Model Used:**
- `gpt-4o-mini` (fast, cheap, perfect for classification)
- Temperature: 0.1 (low for consistency)

## 🚦 Migration Status

- ✅ Semantic Router module created
- ✅ Orchestrator updated to use semantic router
- ✅ Fallback heuristics implemented
- ✅ Backward compatibility maintained
- ⏳ Testing in production (next step)

## 🎯 Next Steps (Future V2 Features)

1. **Multi-Agent System** (Researcher, Calculator, Writer agents)
2. **Compliance Watchdog** (automatic law change monitoring)
3. **Natural Language Chat Interface** (beyond structured JSON)

## 📚 Files Changed

1. `backend/app/core/semantic_router.py` (NEW)
2. `backend/app/core/orchestrator.py` (UPDATED)

## 💡 Example Usage

```python
from app.core.semantic_router import SemanticRouter
from app.models.request import TaxMemoRequest

# Create request
request = TaxMemoRequest(
    company_name="TechStart B.V.",
    industry="Software & Technology",
    timeline_preference="ASAP"
)

# Classify intent
router = SemanticRouter()
intent = router.get_intent(request.model_dump())

print(f"Must be BV: {intent.must_be_bv}")  # True
print(f"Urgency: {intent.urgency}")  # HIGH
print(f"Entity Type: {intent.entity_type}")  # BV
```

---

**Version:** 2.0.0  
**Date:** 2025  
**Status:** ✅ Implemented

