"""Semantic Router: AI-powered intent classification for V2 architecture."""
from typing import Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from app.core.config import settings


class UserIntent(BaseModel):
    """
    Structured intent classification from user input.
    
    This replaces the brittle regex/if-else logic with AI understanding
    that can handle synonyms, typos, and context.
    """
    is_holding: bool = Field(
        default=False,
        description="True if the user wants to establish a holding company structure"
    )
    must_be_bv: bool = Field(
        default=False,
        description="True if the user explicitly wants a Dutch BV (Besloten Vennootschap). This includes synonyms like 'Dutch Limited Liability Co', 'B.V.', 'BV', etc."
    )
    intent: str = Field(
        default="SETUP",
        description="Primary intent: 'SETUP' (establish entity), 'ADVISORY' (tax advice), 'COMPLIANCE' (compliance check)"
    )
    entity_type: Optional[str] = Field(
        default=None,
        description="Detected entity type: 'BV', 'BRANCH', 'HOLDING', or None if unclear"
    )
    urgency: str = Field(
        default="MEDIUM",
        description="Urgency level: 'HIGH' (ASAP/urgent), 'MEDIUM' (normal), 'LOW' (flexible timeline)"
    )
    industry_context: Optional[str] = Field(
        default=None,
        description="Industry context: 'TECH' (software/tech/R&D), 'FINANCIAL' (financial services), 'GENERAL' (other)"
    )


class SemanticRouter:
    """
    V2 Semantic Router: Uses AI to classify user intent instead of regex.
    
    Benefits:
    - Understands synonyms ("Dutch Limited Liability Co" = BV)
    - Handles typos and variations
    - Context-aware classification
    - Impossible to "trick" with phrasing
    """
    
    def __init__(self):
        """Initialize semantic router with OpenAI client."""
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"  # Fast and cheap for classification
    
    def get_intent(self, request_data: dict) -> UserIntent:
        """
        Classify user intent from request data using AI.
        
        Args:
            request_data: Dictionary containing request fields (company_name, industry, 
                         company_type, entry_goals, tax_considerations, timeline_preference, etc.)
        
        Returns:
            UserIntent object with classified intent
        """
        # Build a natural language description of the user's request
        user_input = self._build_user_input_text(request_data)
        
        system_prompt = """You are a tax intent classifier for the Netherlands market entry system.

Your job is to analyze user input and classify their intent into structured JSON.

CRITICAL RULES:
1. **is_holding**: Set to true if:
   - User explicitly mentions "holding company" or "holding structure"
   - User mentions "participation exemption" or "deelnemingsvrijstelling"
   - User's goals include holding/managing subsidiaries
   - Company name contains "holding" or "group" (in holding context)

2. **must_be_bv**: Set to true if:
   - User explicitly names company with "B.V.", "BV", "Besloten Vennootschap"
   - User says "Dutch Limited Liability Company" or similar Dutch entity synonyms
   - User explicitly requests a Dutch BV structure
   - is_holding is true (holdings need BV for tax treaties)
   - NOTE: Generic terms like "LLC", "Corporation", "Limited Liability" do NOT mean BV unless explicitly Dutch context

3. **entity_type**: 
   - "BV" if must_be_bv is true
   - "BRANCH" if user prioritizes speed/urgency and must_be_bv is false
   - "HOLDING" if is_holding is true
   - None if unclear

4. **urgency**:
   - "HIGH" if timeline mentions: ASAP, urgent, fast, short-term, 1 month, immediate
   - "MEDIUM" if timeline is 3-6 months or normal
   - "LOW" if timeline is flexible or long-term

5. **industry_context**:
   - "TECH" if industry is software, technology, biotech, engineering, or goals mention R&D/research
   - "FINANCIAL" if industry is financial services, banking, insurance
   - "GENERAL" for other industries
   - None if unclear

6. **intent**:
   - "SETUP" if user wants to establish a new entity
   - "ADVISORY" if user wants tax advice/consultation
   - "COMPLIANCE" if user wants compliance check

Return ONLY valid JSON matching the UserIntent schema. Be precise and conservative - only set flags to true if you're confident."""
        
        try:
            # Try structured outputs API (available in OpenAI SDK 1.12+)
            try:
                response = self.openai_client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    response_format=UserIntent,
                    temperature=0.1  # Low temperature for consistent classification
                )
                intent = response.choices[0].message.parsed
                return intent
            except AttributeError:
                # Fallback to JSON mode if structured outputs not available
                import json
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt + "\n\nReturn ONLY valid JSON matching the UserIntent schema."},
                        {"role": "user", "content": user_input}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                content = response.choices[0].message.content
                # Parse JSON and create UserIntent
                parsed_json = json.loads(content)
                return UserIntent(**parsed_json)
            
        except Exception as e:
            # Fallback: If AI classification fails, use basic heuristics
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Semantic router AI classification failed: {e}. Using fallback heuristics.")
            return self._fallback_classification(request_data)
    
    def _build_user_input_text(self, request_data: dict) -> str:
        """Build a natural language description from request data."""
        parts = []
        
        if request_data.get("company_name"):
            parts.append(f"Company name: {request_data['company_name']}")
        
        if request_data.get("company_type"):
            parts.append(f"Company type: {request_data['company_type']}")
        
        if request_data.get("industry"):
            parts.append(f"Industry: {request_data['industry']}")
        
        if request_data.get("entry_goals"):
            goals = ", ".join(request_data["entry_goals"])
            parts.append(f"Entry goals: {goals}")
        
        if request_data.get("tax_considerations"):
            tax = ", ".join([str(tc) for tc in request_data["tax_considerations"]])
            parts.append(f"Tax considerations: {tax}")
        
        if request_data.get("timeline_preference"):
            parts.append(f"Timeline preference: {request_data['timeline_preference']}")
        
        if request_data.get("urgency_level"):
            parts.append(f"Urgency level: {request_data['urgency_level']}")
        
        if request_data.get("preferred_structure"):
            parts.append(f"Preferred structure: {request_data['preferred_structure']}")
        
        if request_data.get("additional_context"):
            parts.append(f"Additional context: {request_data['additional_context']}")
        
        return "\n".join(parts) if parts else "User request for Netherlands market entry."
    
    def _fallback_classification(self, request_data: dict) -> UserIntent:
        """
        Fallback classification using basic heuristics if AI fails.
        This maintains backward compatibility.
        """
        company_name = (request_data.get("company_name") or "").lower()
        company_type = (request_data.get("company_type") or "").lower()
        industry = (request_data.get("industry") or "").lower()
        goals = [g.lower() for g in (request_data.get("entry_goals") or [])]
        tax_considerations = [str(tc).lower() for tc in (request_data.get("tax_considerations") or [])]
        timeline = (request_data.get("timeline_preference") or "").lower()
        additional_context = (request_data.get("additional_context") or "").lower()
        
        all_tax_text = " ".join(tax_considerations) + " " + additional_context
        
        # Basic heuristics (similar to V1 but simplified)
        is_holding = (
            "holding" in company_type or
            "holding" in company_name or
            "participation exemption" in all_tax_text or
            "deelnemingsvrijstelling" in all_tax_text
        )
        
        must_be_bv = (
            "b.v" in company_name or
            "bv" in company_name or
            "b.v." in company_name or
            "besloten vennootschap" in company_type or
            is_holding
        )
        
        urgency = "MEDIUM"
        if any(word in timeline for word in ["asap", "urgent", "fast", "short", "1 month"]):
            urgency = "HIGH"
        elif any(word in timeline for word in ["flexible", "long", "12 months"]):
            urgency = "LOW"
        
        industry_context = None
        if ("software" in industry or "technology" in industry or "biotech" in industry or 
            "engineering" in industry or "r&d" in " ".join(goals)):
            industry_context = "TECH"
        elif "financial" in industry:
            industry_context = "FINANCIAL"
        
        entity_type = None
        if must_be_bv:
            entity_type = "BV"
        elif is_holding:
            entity_type = "HOLDING"
        elif urgency == "HIGH" and not must_be_bv:
            entity_type = "BRANCH"
        
        return UserIntent(
            is_holding=is_holding,
            must_be_bv=must_be_bv,
            intent="SETUP",
            entity_type=entity_type,
            urgency=urgency,
            industry_context=industry_context
        )

