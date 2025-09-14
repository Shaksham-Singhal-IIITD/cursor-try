#!/usr/bin/env python3
"""
Demo scenarios for the Sales Page Quick-Answer & Lead Bot
This script demonstrates the key features and workflows of the bot.
"""

import json
from sales_bot import SalesBot

def demo_scenario_1_security_focused():
    """Demo: Security-focused visitor asking about compliance"""
    print("=" * 60)
    print("DEMO SCENARIO 1: Security-Focused Visitor")
    print("=" * 60)
    
    bot = SalesBot()
    
    # Simulate visitor asking about security
    print("\n1. Visitor asks: 'Do you have SOC 2 compliance?'")
    bot.process_user_input("Do you have SOC 2 compliance?")
    
    print("\n2. Visitor asks: 'What about data residency in India?'")
    bot.process_user_input("What about data residency in India?")
    
    print("\n3. Bot's proactive nudge (Security-Focused Visitor rule):")
    # Manually trigger the security rule
    st.session_state.keywords_mentioned = ['soc', 'compliance', 'security', 'data residency']
    st.session_state.questions_answered = 2
    triggered_rule = bot.evaluate_rules()
    if triggered_rule:
        print(f"   Bot: {triggered_rule['action']['message']}")
    
    print("\n4. Visitor agrees to see security info:")
    bot.process_user_input("Yes, I'd like to see the security documentation")
    
    print("\n--- End of Scenario 1 ---\n")

def demo_scenario_2_integration_power_user():
    """Demo: Integration-focused visitor triggering lead capture"""
    print("=" * 60)
    print("DEMO SCENARIO 2: Integration Power User")
    print("=" * 60)
    
    bot = SalesBot()
    
    # Reset session state
    st.session_state.pages_visited = ['/integrations']
    st.session_state.questions_answered = 0
    st.session_state.keywords_mentioned = []
    
    print("\n1. Visitor is on integrations page and asks: 'Do you integrate with Salesforce?'")
    bot.process_user_input("Do you integrate with Salesforce?")
    
    print("\n2. Visitor asks: 'What about custom webhooks?'")
    bot.process_user_input("What about custom webhooks?")
    
    print("\n3. Bot's proactive nudge (Integration Power User rule):")
    # Manually trigger the integration rule
    st.session_state.keywords_mentioned = ['integration', 'api', 'webhook', 'salesforce']
    triggered_rule = bot.evaluate_rules()
    if triggered_rule:
        print(f"   Bot: {triggered_rule['action']['message']}")
    
    print("\n4. Visitor agrees to schedule a call:")
    bot.process_user_input("Yes please")
    
    print("\n5. Lead capture sequence begins:")
    # Simulate lead capture
    st.session_state.lead_capture_mode = True
    st.session_state.current_lead_field = 0
    st.session_state.lead_capture_data = {}
    
    # Simulate filling out the form
    lead_responses = [
        "John Smith",
        "john.smith@company.com", 
        "TechCorp Inc",
        "51-200",
        "Customer data integration",
        "Within 1 month"
    ]
    
    for i, response in enumerate(lead_responses):
        field = bot.lead_form[i]
        print(f"   Bot: {field['prompt']}")
        print(f"   Visitor: {response}")
        st.session_state.lead_capture_data[field['field']] = response
        st.session_state.current_lead_field = i + 1
    
    # Complete lead capture
    bot.complete_lead_capture()
    
    print("\n--- End of Scenario 2 ---\n")

def demo_scenario_3_pricing_page_visitor():
    """Demo: Pricing page visitor with scroll behavior"""
    print("=" * 60)
    print("DEMO SCENARIO 3: Pricing Page Visitor")
    print("=" * 60)
    
    bot = SalesBot()
    
    # Reset session state
    st.session_state.pages_visited = ['/pricing']
    st.session_state.scroll_depth = 80
    st.session_state.questions_answered = 0
    st.session_state.keywords_mentioned = []
    
    print("\n1. Visitor is on pricing page, scrolled 80%")
    print("2. Bot's proactive nudge (Pricing Page Visitor rule):")
    
    triggered_rule = bot.evaluate_rules()
    if triggered_rule:
        print(f"   Bot: {triggered_rule['action']['message']}")
    
    print("\n3. Visitor asks: 'What are your pricing plans?'")
    bot.process_user_input("What are your pricing plans?")
    
    print("\n--- End of Scenario 3 ---\n")

def demo_preview_tool():
    """Demo: Admin preview tool functionality"""
    print("=" * 60)
    print("DEMO: Admin Preview Tool")
    print("=" * 60)
    
    bot = SalesBot()
    
    print("\nTesting different scenarios with the preview tool:")
    
    scenarios = [
        {
            "name": "High Intent on Pricing",
            "pages": ["/pricing"],
            "questions": 2,
            "keywords": ["pricing", "cost"],
            "scroll": 50
        },
        {
            "name": "Integration Power User",
            "pages": ["/integrations"],
            "questions": 2,
            "keywords": ["integration", "api", "webhook"],
            "scroll": 30
        },
        {
            "name": "Security-Focused",
            "pages": ["/security"],
            "questions": 1,
            "keywords": ["soc", "compliance"],
            "scroll": 40
        },
        {
            "name": "Low Intent",
            "pages": ["/home"],
            "questions": 0,
            "keywords": [],
            "scroll": 20
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print(f"  Pages: {scenario['pages']}")
        print(f"  Questions: {scenario['questions']}")
        print(f"  Keywords: {scenario['keywords']}")
        print(f"  Scroll: {scenario['scroll']}%")
        
        # Simulate the scenario
        temp_pages = scenario['pages']
        temp_questions = scenario['questions']
        temp_keywords = scenario['keywords']
        temp_scroll = scenario['scroll']
        
        # Find matching rule
        matching_rule = None
        for rule in bot.rules_engine:
            trigger = rule['trigger']
            match = True
            
            if 'pages_visited' in trigger:
                if not any(page in temp_pages for page in trigger['pages_visited']):
                    match = False
            
            if 'questions_answered' in trigger:
                if temp_questions < trigger['questions_answered']:
                    match = False
            
            if 'keywords_mentioned' in trigger:
                if not any(keyword in temp_keywords for keyword in trigger['keywords_mentioned']):
                    match = False
            
            if 'scroll_depth' in trigger:
                if temp_scroll < trigger['scroll_depth']:
                    match = False
            
            if match:
                matching_rule = rule
                break
        
        if matching_rule:
            print(f"  → Bot would say: {matching_rule['action']['message']}")
            print(f"  → Rule: {matching_rule['rule_name']}")
        else:
            print("  → No rules would trigger")

def main():
    """Run all demo scenarios"""
    print("🤖 Sales Page Quick-Answer & Lead Bot - Demo Scenarios")
    print("=" * 60)
    
    # Note: These demos won't work perfectly without Streamlit's session state
    # but they demonstrate the core logic and workflows
    
    print("\nNote: These are simplified demos showing the bot's logic.")
    print("For the full interactive experience, run: streamlit run sales_bot.py")
    print()
    
    # Demo the preview tool (this works without Streamlit)
    demo_preview_tool()
    
    print("\n" + "=" * 60)
    print("To see the full interactive demo:")
    print("1. Run: streamlit run sales_bot.py")
    print("2. Open: http://localhost:8501")
    print("3. Try the scenarios in the Live Demo panel")
    print("4. Use the Admin Panel to preview different situations")
    print("=" * 60)

if __name__ == "__main__":
    # We need to mock st.session_state for the demo
    class MockSessionState:
        def __init__(self):
            self.pages_visited = []
            self.questions_answered = 0
            self.keywords_mentioned = []
            self.scroll_depth = 0
            self.lead_capture_mode = False
            self.current_lead_field = 0
            self.lead_capture_data = {}
    
    import sys
    sys.modules['streamlit'] = type('MockStreamlit', (), {
        'session_state': MockSessionState()
    })()
    
    main()