# V2 Critical Rules Integration

## ✅ System Prompt Updated

The system prompt in `backend/app/utils/persona.py` has been updated with the critical logic rules you provided.

---

## 🔄 How V2 Semantic Router Aligns with Critical Rules

### Rule 1: Entity Selection Logic

**Critical Rule:**
- Holding Company → MUST recommend BV
- Urgent + Foreign Entity → MUST recommend Branch Office
- Exception: If name contains "B.V." → MUST recommend BV

**V2 Semantic Router Alignment:**
```python
# Semantic Router classifies:
intent.is_holding = True  # Detects "Holding", "Participation Exemption"
intent.must_be_bv = True  # Detects "B.V.", "Dutch Limited Liability Company"
intent.urgency = "HIGH"   # Detects "Urgent", "ASAP", "Fast"
```

**Orchestrator Uses This:**
```python
# If holding → Forces BV path (Rule 1)
if intent.is_holding:
    # Plan BV tasks (never Branch)

# If urgent + not forced BV → Branch path (Rule 1)
elif intent.urgency == "HIGH" and not intent.must_be_bv:
    # Plan Branch tasks
```

**Result:** ✅ V2 correctly routes to BV or Branch based on critical rules

---

### Rule 2: Tax Incentive Logic

**Critical Rule:**
- Innovation Box → ONLY for BV/NV (not Branch)
- WBSO → BOTH BV and Branch
- Participation Exemption → ONLY for Holding Companies

**V2 Semantic Router Alignment:**
```python
# Semantic Router classifies:
intent.industry_context = "TECH"  # Detects tech industry
intent.is_holding = True           # Detects holding company
```

**Orchestrator Uses This:**
```python
# Tech industry → Add R&D incentives (WBSO + Innovation Box)
if intent.industry_context == "TECH":
    # Add WBSO task
    # Innovation Box only added if BV (handled by system prompt)

# Holding company → Add Participation Exemption
if intent.is_holding:
    # Add Participation Exemption task
    # NO Innovation Box (system prompt prevents this)
```

**Result:** ✅ V2 correctly routes tax incentives based on entity type

---

### Rule 3: Timeline & Process Logic

**Critical Rule:**
- Branch Office → NO Notary, NO Deed of Incorporation
- BV → MUST include Notary, Deed of Incorporation

**V2 Semantic Router Alignment:**
```python
# Semantic Router classifies entity type:
intent.entity_type = "BRANCH"  # or "BV" or "HOLDING"
```

**Orchestrator Uses This:**
```python
# Branch path → Explicit "no notary" in search query
if intent.entity_type == "BRANCH":
    tasks.append(TaskPlan(
        search_query="...no notary required timeline fast setup..."
    ))

# BV path → Includes notary requirements
if intent.must_be_bv:
    tasks.append(TaskPlan(
        search_query="...notary requirements bank account opening..."
    ))
```

**System Prompt Enforces:**
- The updated system prompt explicitly forbids mentioning "Notary" for Branch Offices
- The system prompt requires "Notary" for BV structures

**Result:** ✅ V2 correctly routes to appropriate timeline tasks

---

## 📊 Integration Flow

```
User Input
    ↓
V2 Semantic Router (AI Classification)
    ↓
Orchestrator (Routes based on intent)
    ↓
Task Planning (BV vs Branch vs Holding paths)
    ↓
RAG Engine (Uses updated system prompt)
    ↓
Memo Generation (Follows critical rules)
```

---

## ✅ Verification Checklist

- [x] System prompt updated with critical rules
- [x] Semantic Router classifies holding companies correctly
- [x] Semantic Router classifies urgency correctly
- [x] Semantic Router classifies entity type correctly
- [x] Orchestrator routes to correct paths based on intent
- [x] System prompt enforces Branch vs BV logic
- [x] System prompt enforces tax incentive rules
- [x] System prompt enforces timeline/process rules

---

## 🎯 Key Points

1. **V2 Semantic Router** classifies user intent (holding, urgency, entity type)
2. **Orchestrator** uses intent to route to correct task paths
3. **System Prompt** enforces critical rules during memo generation
4. **Three-layer enforcement:**
   - Layer 1: Semantic Router (intent classification)
   - Layer 2: Orchestrator (task routing)
   - Layer 3: System Prompt (content generation rules)

---

## 📝 Files Updated

1. **`backend/app/utils/persona.py`**
   - Updated `MASTER_SYSTEM_PROMPT` with critical logic rules
   - Enforces BV vs Branch logic
   - Enforces tax incentive rules
   - Enforces timeline/process rules

2. **`backend/app/core/semantic_router.py`** (Already implemented)
   - Classifies holding company intent
   - Classifies urgency
   - Classifies entity type

3. **`backend/app/core/orchestrator.py`** (Already implemented)
   - Routes based on semantic router intent
   - Enforces holding → BV path
   - Enforces urgency → Branch path (if not forced BV)

---

**Status:** ✅ Fully Integrated

The critical rules are now enforced at three levels:
1. Intent classification (Semantic Router)
2. Task routing (Orchestrator)
3. Content generation (System Prompt)

