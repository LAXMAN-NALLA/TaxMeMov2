"""
Streamlit UI for Tax Memo Generator - V2
AI-Powered Semantic Router - Professional Multi-Step Interface
"""
import streamlit as st
import requests
import json
from typing import Dict, Any, List
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Tax Memo Generator - V2",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# V2 Banner
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Version 2.0")
st.sidebar.markdown("*AI-Powered Semantic Router*")
st.sidebar.markdown("**✨ New Features:**")
st.sidebar.markdown("- Understands synonyms")
st.sidebar.markdown("- Natural language")
st.sidebar.markdown("- Context-aware")
st.sidebar.markdown("---")

# API Configuration
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://taxmemov2.onrender.com",
    help="Enter your backend API URL (default: production server)"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Step definitions
TOTAL_STEPS = 5
STEP_NAMES = {
    1: "Company Information",
    2: "Goals & Timeline",
    3: "Tax Considerations",
    4: "Additional Context",
    5: "Review & Generate"
}

# Industry options
INDUSTRIES = [
    "Software & Technology",
    "E-commerce & Retail",
    "Manufacturing",
    "Professional Services",
    "Financial Services",
    "Healthcare",
    "Education",
    "Media & Entertainment",
    "Other"
]

# Company size options
COMPANY_SIZES = [
    "Startup (1-10 employees)",
    "Small (11-50 employees)",
    "Medium (51-250 employees)",
    "Large (251+ employees)"
]

# Entry goals options
ENTRY_GOALS = [
    "Sell products/services",
    "Hire employees",
    "Establish physical presence",
    "Access new customer segments",
    "Tax optimization",
    "Regulatory compliance",
    "EU funding opportunities"
]

# Company types
COMPANY_TYPES = [
    "",
    "Holding Company",
    "Corporation",
    "LLC",
    "BV",
    "Besloten Vennootschap"
]

# Tax queries
TAX_QUERIES = [
    "Corporate income tax implications",
    "Value-added tax (VAT) registration and compliance",
    "Withholding tax on dividends, interest, and royalties",
    "Transfer pricing requirements",
    "Permanent establishment risks",
    "Tax treaty benefits and limitations",
    "Substance requirements",
    "Payroll tax obligations",
    "Double taxation prevention",
    "Participation exemption",
    "R&D tax credits (WBSO)",
    "Innovation Box regime"
]

def step_1_company_info():
    """Step 1: Company Information"""
    st.header("📊 Company Information")
    st.markdown("Tell us about your company")
    
    # V2 Feature Highlight
    st.info("💡 **V2 Feature:** You can use natural language like 'Dutch Limited Liability Company' and V2 will understand it means BV!")
    
    # Company Name (Required)
    business_name = st.text_input(
        "Company Name *",
        value=st.session_state.form_data.get("businessName", ""),
        help="💡 V2 understands synonyms! Try: 'Dutch Limited Liability Company' or 'TechStart B.V.'",
        placeholder="e.g., Tech Solutions Inc or Dutch Limited Liability Company"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Industry - Fixed selection issue
        industry_options = [""] + INDUSTRIES
        saved_industry = st.session_state.form_data.get("industry", "")
        industry_index = industry_options.index(saved_industry) if saved_industry in industry_options else 0
        
        industry = st.selectbox(
            "Industry",
            options=industry_options,
            index=industry_index,
            key="industry_select",
            help="Select your primary industry"
        )
        
        # Company Size - Fixed selection issue
        size_options = [""] + COMPANY_SIZES
        saved_size = st.session_state.form_data.get("companySize", "")
        size_index = size_options.index(saved_size) if saved_size in size_options else 0
        
        company_size = st.selectbox(
            "Company Size",
            options=size_options,
            index=size_index,
            key="company_size_select",
            help="Select your company size"
        )
    
    with col2:
        # Company Type - Fixed selection issue
        saved_type = st.session_state.form_data.get("companyType", "")
        type_index = COMPANY_TYPES.index(saved_type) if saved_type in COMPANY_TYPES else 0
        
        company_type = st.selectbox(
            "Company Type",
            options=COMPANY_TYPES,
            index=type_index,
            key="company_type_select",
            help="💡 V2 understands: 'BV', 'Besloten Vennootschap', 'Dutch Limited Liability Company'"
        )
        
        # Revenue (Optional)
        current_revenue = st.number_input(
            "Current Annual Revenue (€)",
            min_value=0.0,
            value=float(st.session_state.form_data.get("currentRevenue", 0)) if st.session_state.form_data.get("currentRevenue") else 0.0,
            step=10000.0,
            key="current_revenue_input",
            help="Your current annual revenue (optional)"
        )
    
    # Save to session state
    st.session_state.form_data["businessName"] = business_name
    st.session_state.form_data["industry"] = industry
    st.session_state.form_data["companySize"] = company_size
    st.session_state.form_data["companyType"] = company_type
    st.session_state.form_data["currentRevenue"] = current_revenue if current_revenue > 0 else None

def step_2_goals_timeline():
    """Step 2: Goals & Timeline"""
    st.header("🎯 Goals & Timeline")
    st.markdown("What are your goals and timeline?")
    
    # V2 Feature Highlight
    st.info("💡 **V2 Feature:** Express urgency in natural language! Try: 'I need this ASAP' or 'very urgently'")
    
    # Entry Goals - Fixed selection issue
    # Initialize widget state from form_data only if key doesn't exist (first time)
    if "entry_goals_select" not in st.session_state:
        st.session_state.entry_goals_select = st.session_state.form_data.get("entryGoals", [])
    
    # Use the widget's key to manage state - Streamlit handles this automatically
    # The widget will use st.session_state.entry_goals_select if it exists
    entry_goals = st.multiselect(
        "Entry Goals",
        options=ENTRY_GOALS,
        key="entry_goals_select",
        help="Select all that apply"
    )
    
    # Always sync widget value to form_data for persistence across steps
    st.session_state.form_data["entryGoals"] = entry_goals
    
    # Timeline - V2: Text input for natural language
    st.subheader("Timeline Preference")
    timeline = st.text_input(
        "When do you plan to enter the market?",
        value=st.session_state.form_data.get("timeline", ""),
        key="timeline_input",
        help="💡 V2 understands natural language! Examples: 'ASAP', 'I need this urgently', 'within 1 month', '3-6 months'",
        placeholder="e.g., ASAP, 3 months, I need this urgently"
    )
    
    # Primary Jurisdiction - Fixed selection issue
    st.subheader("Target Jurisdiction")
    jurisdiction_options = ["", "Netherlands"]
    saved_jurisdiction = st.session_state.form_data.get("primaryJurisdiction", "")
    jurisdiction_index = jurisdiction_options.index(saved_jurisdiction) if saved_jurisdiction in jurisdiction_options else 0
    
    primary_jurisdiction = st.selectbox(
        "Primary Jurisdiction",
        options=jurisdiction_options,
        index=jurisdiction_index,
        key="jurisdiction_select",
        help="Currently supports Netherlands"
    )
    
    # Save to session state (entryGoals already saved above)
    st.session_state.form_data["timeline"] = timeline
    st.session_state.form_data["primaryJurisdiction"] = primary_jurisdiction or "Netherlands"

def step_3_tax_considerations():
    """Step 3: Tax Considerations"""
    st.header("💰 Tax Considerations")
    st.markdown("Tell us about your tax concerns")
    
    # V2 Feature Highlight
    st.info("💡 **V2 Feature:** V2 understands context! Mention 'participation exemption' and it knows you want a holding company structure.")
    
    # Tax Queries - Fixed selection issue
    # Initialize widget state from form_data only if key doesn't exist (first time)
    if "tax_queries_select" not in st.session_state:
        st.session_state.tax_queries_select = st.session_state.form_data.get("taxQueries", [])
    
    # Use the widget's key to manage state - Streamlit handles this automatically
    tax_queries = st.multiselect(
        "Tax Queries",
        options=TAX_QUERIES,
        key="tax_queries_select",
        help="Select all relevant tax queries"
    )
    
    # Always sync widget value to form_data for persistence across steps
    st.session_state.form_data["taxQueries"] = tax_queries
    
    # Custom tax query
    custom_tax_query = st.text_input(
        "Custom Tax Query (optional)",
        value=st.session_state.form_data.get("customTaxQuery", ""),
        key="custom_tax_query_input",
        help="Add a custom tax query if needed"
    )
    
    if custom_tax_query:
        if tax_queries is None:
            tax_queries = []
        tax_queries.append(f"Custom: {custom_tax_query}")
        st.session_state.form_data["taxQueries"] = tax_queries
    
    # Save custom tax query to session state
    st.session_state.form_data["customTaxQuery"] = custom_tax_query

def step_4_additional_context():
    """Step 4: Additional Context"""
    st.header("📝 Additional Context")
    st.markdown("Any additional information or specific questions?")
    
    # V2 Feature Highlight
    st.success("✨ **V2 Power:** This is where V2 shines! Write in natural language and V2 will extract all relevant information.")
    
    additional_context = st.text_area(
        "Additional Context or Questions",
        value=st.session_state.form_data.get("additionalContext", ""),
        key="additional_context_input",
        help="💡 V2 can extract information from natural language! Example: 'I want a Dutch BV structure for my tech startup. I need to hire employees and this is urgent.'",
        height=200,
        placeholder="e.g., I want to establish a Dutch limited liability company quickly. I'm in the software industry and need to hire employees. This is urgent - I need to start operations within a month."
    )
    
    # Legal Topics (Optional)
    st.subheader("Legal Topics (Optional)")
    legal_topics_options = {
        "corporate-law": "Corporate Law",
        "employment-law": "Employment Law",
        "contract-law": "Contract Law",
        "intellectual-property": "Intellectual Property",
        "data-protection": "Data Protection"
    }
    
    # Legal Topics - Fixed selection issue
    # Initialize widget state from form_data only if key doesn't exist (first time)
    if "legal_topics_select" not in st.session_state:
        st.session_state.legal_topics_select = st.session_state.form_data.get("selectedLegalTopics", [])
    
    # Use the widget's key to manage state - Streamlit handles this automatically
    selected_topics = st.multiselect(
        "Legal Topics",
        options=list(legal_topics_options.keys()),
        format_func=lambda x: legal_topics_options[x],
        key="legal_topics_select",
        help="Select relevant legal topics"
    )
    
    # Always sync widget value to form_data for persistence across steps
    st.session_state.form_data["selectedLegalTopics"] = selected_topics
    
    # Save to session state
    st.session_state.form_data["additionalContext"] = additional_context

def step_5_review_and_generate():
    """Step 5: Review & Generate"""
    st.header("📋 Review & Generate")
    st.markdown("Review your inputs and generate your tax memo")
    
    # Validation
    if not st.session_state.form_data.get("businessName"):
        st.error("❌ Company Name is required. Please go back to Step 1.")
        return
    
    # Show summary
    st.subheader("📝 Input Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Company Information**")
        st.write(f"- **Name:** {st.session_state.form_data.get('businessName', 'N/A')}")
        st.write(f"- **Industry:** {st.session_state.form_data.get('industry', 'Not specified')}")
        st.write(f"- **Size:** {st.session_state.form_data.get('companySize', 'Not specified')}")
        st.write(f"- **Type:** {st.session_state.form_data.get('companyType', 'Not specified')}")
        
        if st.session_state.form_data.get('currentRevenue'):
            st.write(f"- **Current Revenue:** €{st.session_state.form_data.get('currentRevenue'):,.0f}")
    
    with col2:
        st.markdown("**Goals & Timeline**")
        entry_goals = st.session_state.form_data.get('entryGoals', [])
        if entry_goals:
            for goal in entry_goals:
                st.write(f"- {goal}")
        else:
            st.write("- No goals specified")
        st.write(f"- **Timeline:** {st.session_state.form_data.get('timeline', 'Not specified')}")
        st.write(f"- **Jurisdiction:** {st.session_state.form_data.get('primaryJurisdiction', 'Not specified')}")
        
        st.markdown("**Tax Considerations**")
        tax_queries = st.session_state.form_data.get('taxQueries', [])
        if tax_queries:
            st.write(f"- {len(tax_queries)} tax query/queries selected")
        else:
            st.write("- No tax queries specified")
    
    # V2 Classification Preview
    st.markdown("---")
    st.markdown("### 🎯 V2 Semantic Router Preview")
    
    preview_info = []
    
    # Check for BV indicators
    company_name = st.session_state.form_data.get('businessName', '').lower()
    company_type = st.session_state.form_data.get('companyType', '').lower()
    additional_context = st.session_state.form_data.get('additionalContext', '').lower()
    
    if any(x in company_name for x in ['b.v', 'bv', 'besloten', 'dutch limited liability']):
        preview_info.append("✅ **Entity Type:** BV detected (V2 understands synonyms!)")
    elif company_type in ['bv', 'besloten vennootschap']:
        preview_info.append("✅ **Entity Type:** BV detected")
    
    # Check for urgency
    timeline = st.session_state.form_data.get('timeline', '').lower()
    if any(x in timeline for x in ['asap', 'urgent', 'urgently', 'hurry', 'fast']):
        preview_info.append("✅ **Urgency:** HIGH detected (V2 understands natural language!)")
    
    # Check for holding company
    tax_queries_str = ' '.join(st.session_state.form_data.get('taxQueries', [])).lower()
    if 'participation exemption' in tax_queries_str or 'holding' in company_type:
        preview_info.append("✅ **Company Type:** Holding company detected (V2 understands context!)")
    
    # Check for tech industry
    industry = st.session_state.form_data.get('industry', '').lower()
    if 'software' in industry or 'technology' in industry:
        preview_info.append("✅ **Industry:** Tech detected - R&D incentives will be included")
    
    if preview_info:
        for info in preview_info:
            st.success(info)
    else:
        st.info("ℹ️ V2 will analyze your input and classify intent automatically.")
    
    # Special features indicator
    st.markdown("---")
    st.markdown("### ✨ Special Features Activated")
    
    special_features = []
    if st.session_state.form_data.get('industry') == "Software & Technology":
        special_features.append("🔬 **WBSO & Innovation Box Research** - Automatic research for R&D tax credits")
    if "Hire employees" in st.session_state.form_data.get('entryGoals', []):
        special_features.append("👥 **Employment Law Research** - Automatic research for payroll tax and employment contracts")
    if st.session_state.form_data.get('companyType') == "Holding Company" or any("participation exemption" in str(q).lower() for q in st.session_state.form_data.get('taxQueries', [])):
        special_features.append("🏢 **Holding Company Path** - Specialized research for participation exemption and BV structure")
    
    if special_features:
        for feature in special_features:
            st.success(feature)
    else:
        st.info("ℹ️ Standard research path will be used. V2 will automatically detect specialized needs from your input.")
    
    # Generate button
    st.markdown("---")
    if st.button("🚀 Generate Memo with V2", type="primary", use_container_width=True):
        generate_memo()

def map_frontend_to_backend(frontend_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map frontend field names to backend field names"""
    backend_data = {}
    
    # Required field
    if frontend_data.get("businessName"):
        backend_data["companyName"] = frontend_data["businessName"]
    
    # Direct mappings
    if frontend_data.get("entryGoals"):
        backend_data["entryGoals"] = frontend_data["entryGoals"]
    
    if frontend_data.get("primaryJurisdiction"):
        backend_data["primaryJurisdiction"] = frontend_data["primaryJurisdiction"]
    
    if frontend_data.get("taxQueries"):
        backend_data["taxConsiderations"] = frontend_data["taxQueries"]
    
    if frontend_data.get("selectedLegalTopics"):
        backend_data["selectedLegalTopics"] = frontend_data["selectedLegalTopics"]
    
    # Handle companySize -> employeeCount conversion
    if frontend_data.get("companySize"):
        size_map = {
            "Startup (1-10 employees)": 5,
            "Small (11-50 employees)": 25,
            "Medium (51-250 employees)": 100,
            "Large (251+ employees)": 500
        }
        if frontend_data["companySize"] in size_map:
            backend_data["employeeCount"] = size_map[frontend_data["companySize"]]
    
    # Handle industry
    if frontend_data.get("industry"):
        backend_data["industry"] = frontend_data["industry"]
    
    # Handle companyType
    if frontend_data.get("companyType"):
        backend_data["companyType"] = frontend_data["companyType"]
    
    # Handle timeline (V2: natural language)
    if frontend_data.get("timeline"):
        backend_data["timelinePreference"] = frontend_data["timeline"]
    
    # Handle additional context (V2: extracts info from natural language)
    if frontend_data.get("additionalContext"):
        backend_data["additionalContext"] = frontend_data["additionalContext"]
    
    # Handle revenue
    if frontend_data.get("currentRevenue"):
        backend_data["currentRevenue"] = frontend_data["currentRevenue"]
    
    return backend_data

def generate_memo():
    """Generate memo by calling backend API"""
    # Map frontend data to backend format
    backend_request = map_frontend_to_backend(st.session_state.form_data)
    
    # Show request being sent
    with st.spinner("🔄 Generating your memo with V2 Semantic Router... This may take 30-60 seconds."):
        try:
            response = requests.post(
                f"{API_URL}/generate-memo",
                json=backend_request,
                timeout=180
            )
            
            if response.status_code == 200:
                memo = response.json()
                st.session_state.memo_result = memo
                st.success("✅ Memo generated successfully with V2!")
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ Error: {response.status_code}")
                try:
                    error_detail = response.json()
                    st.json(error_detail)
                except:
                    st.write(response.text)
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Could not connect to API at {API_URL}")
            st.info("💡 The backend server might be starting up. Please try again in a few moments.")
            st.info(f"🔗 Backend URL: {API_URL}")
            st.info("💡 If the issue persists, check the backend status at: https://taxmemov2.onrender.com/health")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The memo generation is taking longer than expected.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def display_memo():
    """Display the generated memo in a clear, readable format"""
    if "memo_result" not in st.session_state:
        return
    
    memo = st.session_state.memo_result
    
    st.header("📄 Your Generated Tax Memo (V2)")
    st.markdown("---")
    
    # V2 Classification Results
    st.subheader("🎯 V2 Classification Results")
    st.success("""
    **What V2 Understood:**
    - ✅ Analyzed company name for entity type detection
    - ✅ Detected urgency from natural language timeline
    - ✅ Identified industry context for specialized recommendations
    - ✅ Extracted tax considerations for holding company detection
    """)
    st.markdown("---")
    
    # Executive Summary
    if memo.get("executiveSummary"):
        st.subheader("📊 Executive Summary")
        exec_sum = memo["executiveSummary"]
        
        if exec_sum.get("overview"):
            st.write(exec_sum["overview"])
        
        if exec_sum.get("keyRecommendations"):
            st.markdown("**✅ Key Recommendations:**")
            for rec in exec_sum["keyRecommendations"]:
                st.markdown(f"• {rec}")
        
        if exec_sum.get("criticalConsiderations"):
            st.markdown("**⚠️ Critical Considerations:**")
            for cons in exec_sum["criticalConsiderations"]:
                st.markdown(f"• {cons}")
        
        st.markdown("---")
    
    # Tax Considerations
    if memo.get("taxConsiderations"):
        st.subheader("💰 Tax Considerations")
        tax = memo["taxConsiderations"]
        
        if tax.get("corporateTaxRate"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Corporate Tax Rate", tax["corporateTaxRate"])
        
        if tax.get("taxObligations"):
            st.markdown("**📋 Tax Obligations:**")
            for obl in tax["taxObligations"]:
                st.markdown(f"• {obl}")
        
        if tax.get("taxOptimizationStrategies"):
            st.markdown("**💡 Tax Optimization Strategies:**")
            for strat in tax["taxOptimizationStrategies"]:
                st.markdown(f"• {strat}")
        
        if tax.get("specialRegimes"):
            st.markdown("**🎯 Special Tax Regimes:**")
            for regime in tax["specialRegimes"]:
                st.markdown(f"• {regime}")
        
        st.markdown("---")
    
    # Market Entry Options
    if memo.get("marketEntryOptions"):
        st.subheader("🚪 Market Entry Options")
        entry = memo["marketEntryOptions"]
        
        if entry.get("recommendedOption"):
            st.success(f"**Recommended:** {entry['recommendedOption']}")
        
        if entry.get("optionComparison"):
            st.markdown("**Options Comparison:**")
            for i, opt in enumerate(entry["optionComparison"], 1):
                with st.expander(f"Option {i}: {opt.get('option', 'Option')}", expanded=(i == 1)):
                    st.write(opt.get("description", ""))
        
        st.markdown("---")
    
    # Implementation Timeline
    if memo.get("implementationTimeline"):
        st.subheader("📅 Implementation Timeline")
        timeline = memo["implementationTimeline"]
        
        if timeline.get("estimatedDuration"):
            st.metric("Estimated Duration", timeline["estimatedDuration"])
        
        if timeline.get("phases"):
            st.markdown("**Phases:**")
            for i, phase in enumerate(timeline["phases"], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Phase {i}: {phase.get('phase', 'Phase')}**")
                    if phase.get("description"):
                        st.write(phase["description"])
                    elif phase.get("details"):
                        st.write(phase["details"])
                with col2:
                    st.markdown(f"**Duration:** {phase.get('duration', 'N/A')}")
        
        if timeline.get("milestones"):
            st.markdown("**🎯 Key Milestones:**")
            for milestone in timeline["milestones"]:
                st.markdown(f"• {milestone}")
        
        st.markdown("---")
    
    # Business Structure
    if memo.get("businessStructure"):
        st.subheader("🏢 Business Structure")
        struct = memo["businessStructure"]
        if struct.get("recommendedStructure"):
            st.write(f"**Recommended Structure:** {struct['recommendedStructure']}")
        if struct.get("structureRationale"):
            st.write(f"**Rationale:** {struct['structureRationale']}")
        st.markdown("---")
    
    # Legal Deep Dive
    if memo.get("legalDeepDive"):
        st.subheader("⚖️ Legal Deep Dive")
        legal = memo["legalDeepDive"]
        if legal.get("detailedAnalysis"):
            st.write(legal["detailedAnalysis"])
        st.markdown("---")
    
    # Download and Full JSON
    col1, col2 = st.columns(2)
    with col1:
        json_str = json.dumps(memo, indent=2)
        st.download_button(
            label="📥 Download Memo (JSON)",
            data=json_str,
            file_name=f"tax_memo_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    with col2:
        with st.expander("🔍 View Full JSON Response"):
            st.json(memo)

def main():
    """Main application"""
    st.title("📋 Tax Memo Generator")
    st.markdown("### Version 2.0 - AI-Powered Semantic Router")
    st.markdown("*Generate comprehensive tax and legal memos with intelligent intent classification*")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Step navigation
    for step_num in range(1, TOTAL_STEPS + 1):
        step_name = STEP_NAMES[step_num]
        if st.sidebar.button(f"Step {step_num}: {step_name}", key=f"nav_{step_num}", use_container_width=True):
            st.session_state.current_step = step_num
            st.rerun()
    
    st.sidebar.divider()
    
    # Progress indicator
    progress = st.session_state.current_step / TOTAL_STEPS
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Step {st.session_state.current_step} of {TOTAL_STEPS}")
    
    # V2 Features in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✨ V2 Features")
    st.sidebar.markdown("**Understands:**")
    st.sidebar.markdown("- Synonyms")
    st.sidebar.markdown("- Natural language")
    st.sidebar.markdown("- Context")
    st.sidebar.markdown("- Typos & variations")
    
    # Main content area
    if st.session_state.current_step == 1:
        step_1_company_info()
    elif st.session_state.current_step == 2:
        step_2_goals_timeline()
    elif st.session_state.current_step == 3:
        step_3_tax_considerations()
    elif st.session_state.current_step == 4:
        step_4_additional_context()
    elif st.session_state.current_step == 5:
        step_5_review_and_generate()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.current_step > 1:
            if st.button("◀ Previous", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_step < TOTAL_STEPS:
            if st.button("Next ▶", use_container_width=True, type="primary"):
                st.session_state.current_step += 1
                st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.form_data = {}
            st.session_state.current_step = 1
            if "memo_result" in st.session_state:
                del st.session_state.memo_result
            st.rerun()
    
    # Display memo if generated
    if "memo_result" in st.session_state:
        st.divider()
        display_memo()

if __name__ == "__main__":
    main()
