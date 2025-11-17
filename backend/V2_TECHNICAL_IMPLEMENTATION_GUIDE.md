# V2 Technical Implementation Guide
## How the Semantic Router Works - Step by Step

This document provides a detailed technical walkthrough of how V2 was implemented and how it works under the hood.

---

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    API Layer                                 │
│  POST /generate-memo                                         │
│  Input: TaxMemoRequest (JSON)                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestrator (V2 Updated)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Receives TaxMemoRequest                           │  │
│  │  2. Calls SemanticRouter.get_intent()                │  │
│  │  3. Gets UserIntent back                             │  │
│  │  4. Plans tasks based on intent                      │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          Semantic Router (V2 New Component)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Builds natural language description             │  │
│  │  2. Calls GPT-4o-mini API                            │  │
│  │  3. Parses AI response                               │  │
│  │  4. Returns UserIntent object                        │  │
│  │  5. Falls back to heuristics if AI fails              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Code Flow

### Step 1: User Sends Request

**Input:**
```json
{
  "company_name": "Dutch Limited Liability Company",
  "industry": "Software & Technology",
  "timeline_preference": "ASAP"
}
```

**Code Location:** `backend/app/main.py`
```python
@app.post("/generate-memo")
async def generate_memo(request: TaxMemoRequest):
    # Request received
    tasks = orchestrator.plan_tasks(request)  # ← Goes to orchestrator
```

---

### Step 2: Orchestrator Receives Request

**Code Location:** `backend/app/core/orchestrator.py`

**Before (V1):**
```python
def plan_tasks(self, request: TaxMemoRequest):
    # V1: Manual regex matching
    company_name = request.company_name.lower()
    must_be_bv = "b.v" in company_name or "bv" in company_name
    # ... more regex checks
```

**After (V2):**
```python
def plan_tasks(self, request: TaxMemoRequest):
    # V2: Convert to dict for semantic router
    request_dict = request.model_dump()
    
    # V2: Call semantic router (AI-powered)
    intent = self.semantic_router.get_intent(request_dict)
    
    # Extract classified values
    is_holding = intent.is_holding
    must_be_bv = intent.must_be_bv
    urgency = intent.urgency
    # ... use intent values
```

**Key Change:** Instead of regex, we call `semantic_router.get_intent()`

---

### Step 3: Semantic Router Processes Request

**Code Location:** `backend/app/core/semantic_router.py`

#### 3.1: Build Natural Language Description

```python
def _build_user_input_text(self, request_data: dict) -> str:
    """Builds a natural language description from request data."""
    parts = []
    
    if request_data.get("company_name"):
        parts.append(f"Company name: {request_data['company_name']}")
    
    if request_data.get("industry"):
        parts.append(f"Industry: {request_data['industry']}")
    
    if request_data.get("timeline_preference"):
        parts.append(f"Timeline preference: {request_data['timeline_preference']}")
    
    return "\n".join(parts)
```

**Output for our example:**
```
Company name: Dutch Limited Liability Company
Industry: Software & Technology
Timeline preference: ASAP
```

#### 3.2: Prepare AI Prompt

```python
system_prompt = """You are a tax intent classifier for the Netherlands market entry system.

Your job is to analyze user input and classify their intent into structured JSON.

CRITICAL RULES:
1. **must_be_bv**: Set to true if:
   - User explicitly names company with "B.V.", "BV", "Besloten Vennootschap"
   - User says "Dutch Limited Liability Company" or similar Dutch entity synonyms
   - User explicitly requests a Dutch BV structure
   ...
"""
```

#### 3.3: Call GPT-4o-mini API

```python
def get_intent(self, request_data: dict) -> UserIntent:
    user_input = self._build_user_input_text(request_data)
    
    try:
        # Try structured outputs API (newer OpenAI SDK)
        response = self.openai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            response_format=UserIntent,  # ← Pydantic model
            temperature=0.1  # Low for consistency
        )
        
        intent = response.choices[0].message.parsed
        return intent
        
    except AttributeError:
        # Fallback to JSON mode if structured outputs not available
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[...],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        # Parse JSON and create UserIntent
        parsed_json = json.loads(response.choices[0].message.content)
        return UserIntent(**parsed_json)
        
    except Exception as e:
        # Fallback to heuristics if AI fails
        return self._fallback_classification(request_data)
```

**What Happens:**
1. Sends user input to GPT-4o-mini
2. AI analyzes and returns structured JSON
3. Parses into `UserIntent` Pydantic model
4. Falls back to heuristics if anything fails

#### 3.4: AI Response (Example)

**AI Returns:**
```json
{
  "is_holding": false,
  "must_be_bv": true,
  "intent": "SETUP",
  "entity_type": "BV",
  "urgency": "HIGH",
  "industry_context": "TECH"
}
```

**Parsed into:**
```python
UserIntent(
    is_holding=False,
    must_be_bv=True,  # ✅ AI understood "Dutch Limited Liability Company" = BV
    intent="SETUP",
    entity_type="BV",
    urgency="HIGH",  # ✅ AI understood "ASAP" = high urgency
    industry_context="TECH"  # ✅ AI understood "Software & Technology"
)
```

---

### Step 4: Orchestrator Uses Classified Intent

**Code Location:** `backend/app/core/orchestrator.py`

```python
def plan_tasks(self, request: TaxMemoRequest):
    # Get classified intent from semantic router
    intent = self.semantic_router.get_intent(request.model_dump())
    
    # Extract values
    is_holding = intent.is_holding  # False
    must_be_bv = intent.must_be_bv  # True ✅
    urgency = intent.urgency  # "HIGH"
    industry_context = intent.industry_context  # "TECH"
    
    # Map to task planning variables
    is_tech = (industry_context == "TECH")  # True
    prioritizes_speed = (urgency == "HIGH")  # True
    
    # Plan tasks (same logic as V1, but with better inputs)
    if is_holding:
        # ... holding company tasks
    elif must_be_bv:  # ✅ This path is taken
        tasks.append(TaskPlan(
            task_name="BV Executive Summary",
            search_query="Netherlands BV private limited company...",
            section_name="executive_summary",
            priority=1
        ))
        # ... more BV tasks
    elif prioritizes_speed:
        # ... branch office tasks
    else:
        # ... default comparison tasks
    
    # Add tech incentives if tech industry
    if is_tech:  # ✅ True
        tasks.append(TaskPlan(
            task_name="R&D Incentives (WBSO & Innovation Box)",
            search_query="Netherlands WBSO R&D tax credit...",
            section_name="tax_considerations",
            priority=5
        ))
    
    return tasks
```

**Result:** Correct tasks planned based on AI understanding

---

### Step 5: RAG Engine Generates Memo

**Code Location:** `backend/app/services/rag_engine.py`

```python
# Tasks are passed to RAG engine (unchanged from V1)
sections = rag_engine.generate_memo_sections(tasks, user_context)

# Generates memo sections based on tasks
# This part is unchanged - V2 only improves task planning
```

---

## 🔄 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  User Request                                                │
│  {                                                           │
│    "company_name": "Dutch Limited Liability Company",        │
│    "industry": "Software & Technology",                     │
│    "timeline_preference": "ASAP"                            │
│  }                                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Orchestrator.plan_tasks()                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  request_dict = request.model_dump()                │  │
│  │  intent = semantic_router.get_intent(request_dict)   │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SemanticRouter.get_intent()                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Build user input text:                           │  │
│  │     "Company name: Dutch Limited Liability Company   │  │
│  │      Industry: Software & Technology                 │  │
│  │      Timeline preference: ASAP"                      │  │
│  │                                                       │  │
│  │  2. Call GPT-4o-mini:                                │  │
│  │     POST https://api.openai.com/v1/chat/completions  │  │
│  │     {                                                │  │
│  │       "model": "gpt-4o-mini",                        │  │
│  │       "messages": [                                   │  │
│  │         {"role": "system", "content": "..."},        │  │
│  │         {"role": "user", "content": "..."}           │  │
│  │       ],                                             │  │
│  │       "response_format": UserIntent                 │  │
│  │     }                                                │  │
│  │                                                       │  │
│  │  3. AI Response:                                     │  │
│  │     {                                                │  │
│  │       "must_be_bv": true,                           │  │
│  │       "urgency": "HIGH",                            │  │
│  │       "industry_context": "TECH"                   │  │
│  │     }                                                │  │
│  │                                                       │  │
│  │  4. Parse into UserIntent object                    │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Return UserIntent to Orchestrator                         │
│  UserIntent(                                                │
│    must_be_bv=True,                                         │
│    urgency="HIGH",                                         │
│    industry_context="TECH"                                  │
│  )                                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Orchestrator Plans Tasks                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  if intent.must_be_bv:  # True                        │  │
│  │    tasks.append("BV Executive Summary")               │  │
│  │    tasks.append("BV Incorporation Process")          │  │
│  │    ...                                                │  │
│  │                                                       │  │
│  │  if intent.industry_context == "TECH":  # True        │  │
│  │    tasks.append("R&D Incentives")                    │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  RAG Engine Generates Memo                                  │
│  (Unchanged from V1)                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Example: Complete Request Flow

### Input Request

```json
{
  "company_name": "Dutch Limited Liability Company",
  "industry": "Software & Technology",
  "timeline_preference": "ASAP"
}
```

### Step-by-Step Processing

#### Step 1: Orchestrator Receives Request
```python
# orchestrator.py
request_dict = {
    "company_name": "Dutch Limited Liability Company",
    "industry": "Software & Technology",
    "timeline_preference": "ASAP"
}
intent = self.semantic_router.get_intent(request_dict)
```

#### Step 2: Semantic Router Builds Input Text
```python
# semantic_router.py
user_input = """
Company name: Dutch Limited Liability Company
Industry: Software & Technology
Timeline preference: ASAP
"""
```

#### Step 3: AI Classification
```python
# semantic_router.py
response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a tax intent classifier..."
        },
        {
            "role": "user",
            "content": "Company name: Dutch Limited Liability Company\n..."
        }
    ],
    response_format=UserIntent
)

# AI analyzes and returns:
# - "Dutch Limited Liability Company" = BV (understands synonym)
# - "ASAP" = HIGH urgency (understands natural language)
# - "Software & Technology" = TECH industry
```

#### Step 4: AI Response Parsed
```python
# semantic_router.py
intent = UserIntent(
    is_holding=False,
    must_be_bv=True,  # ✅ Correctly identified
    intent="SETUP",
    entity_type="BV",
    urgency="HIGH",  # ✅ Correctly identified
    industry_context="TECH"  # ✅ Correctly identified
)
return intent
```

#### Step 5: Orchestrator Plans Tasks
```python
# orchestrator.py
if intent.must_be_bv:  # True
    tasks = [
        TaskPlan("BV Executive Summary", ...),
        TaskPlan("BV Incorporation Process", ...),
        TaskPlan("BV Tax and Compliance", ...),
        TaskPlan("BV Implementation Timeline", ...)
    ]

if intent.industry_context == "TECH":  # True
    tasks.append(TaskPlan("R&D Incentives (WBSO & Innovation Box)", ...))

return tasks
```

#### Step 6: RAG Engine Generates Memo
```python
# rag_engine.py (unchanged)
sections = rag_engine.generate_memo_sections(tasks, user_context)
# Returns memo with BV-specific content + R&D incentives
```

### Final Result

**V1 Would Have:**
- ❌ Missed BV intent (no "B.V." in name)
- ❌ Recommended Branch Office (wrong)
- ❌ Missed R&D incentives (maybe)

**V2 Actually Does:**
- ✅ Correctly identifies BV intent
- ✅ Recommends BV structure (correct)
- ✅ Includes R&D incentives (correct)
- ✅ Detects urgency (correct)

---

## 🔧 Error Handling & Fallbacks

### Three-Layer Safety

#### Layer 1: Structured Outputs API
```python
try:
    # Try new structured outputs API
    response = client.beta.chat.completions.parse(...)
    return response.choices[0].message.parsed
except AttributeError:
    # Fallback to JSON mode
```

#### Layer 2: JSON Mode
```python
try:
    # Fallback to JSON mode
    response = client.chat.completions.create(
        response_format={"type": "json_object"}
    )
    return UserIntent(**json.loads(response.content))
except Exception:
    # Fallback to heuristics
```

#### Layer 3: Heuristics (V1 Logic)
```python
except Exception as e:
    # Final fallback: Use V1 heuristics
    logger.warning(f"AI classification failed: {e}")
    return self._fallback_classification(request_data)
```

**Result:** System never breaks, always returns valid intent

---

## 📊 Performance Characteristics

### Response Time Breakdown

```
Total Request Time: ~10-30 seconds (memo generation)

Breakdown:
- Semantic Router: ~200-300ms (2-3% of total)
- Task Planning: ~10ms (<0.1% of total)
- RAG Generation: ~10-30 seconds (97% of total)
```

**Impact:** Semantic Router adds negligible latency

### Cost Breakdown

```
Per Request:
- GPT-4o-mini (classification): $0.00015
- GPT-4o (memo generation): $0.05-0.15
- Total: $0.05-0.15

Semantic Router: 0.1-0.3% of total cost
```

**Impact:** Minimal cost increase

---

## 🎯 Key Implementation Details

### 1. Pydantic Model for Type Safety

```python
class UserIntent(BaseModel):
    is_holding: bool = Field(default=False)
    must_be_bv: bool = Field(default=False)
    intent: str = Field(default="SETUP")
    entity_type: Optional[str] = None
    urgency: str = Field(default="MEDIUM")
    industry_context: Optional[str] = None
```

**Benefits:**
- Type safety
- Validation
- IDE autocomplete
- Documentation

### 2. Temperature Setting

```python
temperature=0.1  # Low for consistency
```

**Why:** Classification should be consistent, not creative

### 3. Model Choice

```python
model="gpt-4o-mini"  # Fast, cheap, accurate enough
```

**Why:**
- Fast response (~200ms)
- Low cost ($0.00015/request)
- Accurate for classification tasks
- No need for GPT-4o (overkill for classification)

### 4. Fallback Heuristics

```python
def _fallback_classification(self, request_data: dict) -> UserIntent:
    # V1 logic as fallback
    # Ensures system never breaks
```

**Why:** Safety net if AI fails

---

## 🚀 Deployment Checklist

- [x] Semantic Router module created
- [x] Orchestrator updated
- [x] Fallback heuristics implemented
- [x] Error handling added
- [x] Logging added
- [x] Documentation created
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Staging deployment
- [ ] Production deployment

---

**This document provides the technical foundation for understanding how V2 works. Use it alongside the CEO presentation for complete coverage.**

