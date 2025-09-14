# Sales Page Quick-Answer & Lead Bot

A configurable Streamlit application that simulates a sales page bot capable of answering questions, proactively engaging visitors, and capturing leads. This implementation follows the comprehensive project plan for building an intelligent sales assistant.

## 🚀 Features

- **Q&A Engine**: Answers questions based on configurable knowledge pack with keyword matching
- **Proactive Nudges**: Triggers contextual messages based on visitor behavior patterns
- **Lead Capture**: Conversational form to collect visitor information naturally
- **Admin Panel**: Upload configuration files and preview bot behavior
- **Trace Logging**: See the bot's decision-making process in real-time
- **Situation Preview Tool**: Test different scenarios to see what the bot would say

## 🏗️ Architecture

The system is built around a **configurable framework** that separates logic from content:

1. **Configuration Files (JSON)**:
   - `knowledge_pack.json`: Q&A pairs with keywords and sources
   - `rules_engine.json`: Logic for proactive nudges and triggers
   - `lead_form.json`: Questions for the lead capture sequence

2. **Bot Engine (Python/Streamlit Backend)**:
   - State Manager: Tracks visitor context throughout interaction
   - Q&A Module: Searches knowledge pack for fast, correct answers
   - Rules Engine: Evaluates visitor state against triggers
   - Lead Capture Module: Conversational form collection
   - Persistence Layer: Saves captured leads to JSON

3. **Frontend (Streamlit UI)**:
   - Live Demo Pane: Chat interface simulating on-page widget
   - Admin/Control Panel: Configuration management and preview tool

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
streamlit run sales_bot.py
```

3. **Open your browser** to `http://localhost:8501`

## 📋 Configuration Files

### Knowledge Pack (`knowledge_pack.json`)
Contains Q&A pairs with keywords for matching:
```json
[
  {
    "id": "SEC-01",
    "keywords": ["soc 2", "soc2", "compliance", "security"],
    "question": "Do you have SOC 2?",
    "answer": "Yes, we are SOC 2 Type II compliant...",
    "source": "https://ourcompany.com/security"
  }
]
```

### Rules Engine (`rules_engine.json`)
Defines triggers for proactive nudges:
```json
[
  {
    "rule_name": "High Intent on Pricing/Security",
    "trigger": {
      "pages_visited": ["/pricing", "/security"],
      "questions_answered": 2
    },
    "action": {
      "type": "NUDGE",
      "message": "Looks like you're doing some serious research...",
      "follow_up_action": "INITIATE_LEAD_CAPTURE"
    }
  }
]
```

### Lead Form (`lead_form.json`)
Defines conversational lead capture questions:
```json
[
  {
    "field": "name",
    "prompt": "Great! What's your full name?",
    "required": true
  }
]
```

## 🎯 How to Use

### Live Demo Panel (Right Side)
- **Chat Interface**: Type questions to see the bot respond
- **Proactive Nudges**: Ask multiple questions to trigger contextual messages
- **Lead Capture**: Agree to nudges to start the conversational form

### Admin Panel (Left Side)
- **File Uploaders**: Update configuration files without code changes
- **Situation Preview Tool**: Test different scenarios to see bot responses
- **Trace Log**: View the bot's decision-making process in real-time
- **Captured Leads**: Review all collected lead information

## 🎭 Example Scenarios

### Scenario 1: Security-Focused Visitor
1. Ask: "Do you have SOC 2 compliance?"
2. Ask: "What about data residency in India?"
3. Bot triggers security-focused nudge
4. Agree to see security documentation

### Scenario 2: Integration Power User
1. Simulate visiting `/integrations` page
2. Ask: "Do you integrate with Salesforce?"
3. Ask: "What about custom webhooks?"
4. Bot triggers integration specialist call offer
5. Complete lead capture form

### Scenario 3: Pricing Page Visitor
1. Simulate visiting `/pricing` with 70% scroll
2. Bot triggers pricing assistance nudge
3. Ask about pricing plans

## 🔧 Admin Features

### Situation Preview Tool
Test different visitor scenarios:
- **Current Page**: Select from dropdown (home, pricing, security, integrations, support)
- **Scroll Depth**: Use slider to simulate scroll percentage
- **Questions Asked**: Set number of questions answered
- **Keywords Mentioned**: Select relevant keywords
- **Preview**: See what the bot would say in that situation

### Trace Logging
Monitor the bot's decision process:
- User questions and keyword detection
- Rule evaluation and triggering
- Lead capture progression
- Session state updates

## 📊 Project Structure

```
├── sales_bot.py           # Main Streamlit application
├── knowledge_pack.json    # Q&A configuration
├── rules_engine.json      # Rules for proactive nudges
├── lead_form.json         # Lead capture questions
├── leads.json            # Captured leads (auto-generated)
├── demo_scenarios.py     # Demo scenarios and examples
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎪 Demo Scenarios

Run the demo script to see example workflows:
```bash
python3 demo_scenarios.py
```

This shows:
- Admin preview tool functionality
- Different visitor scenarios
- Rule triggering logic
- Expected bot responses

## 🔄 Workflow Examples

### High-Intent Visitor Journey
1. **Engage**: Visitor lands on `/pricing` page, scrolls 80%
2. **Inform**: Asks "What are your pricing plans?" → Gets detailed answer
3. **Inform**: Asks "Do you have SOC 2?" → Gets compliance info
4. **Engage**: Bot detects high intent, triggers nudge
5. **Identify**: Visitor agrees, enters lead capture flow
6. **Convert**: Completes conversational form, lead saved

### Integration-Focused Journey
1. **Engage**: Visitor on `/integrations` page
2. **Inform**: Asks about Salesforce integration
3. **Inform**: Asks about custom webhooks
4. **Engage**: Bot detects integration focus, offers technical call
5. **Identify**: Visitor agrees, lead capture begins
6. **Convert**: Technical details collected, specialist follow-up scheduled

## 🎯 Key Benefits

- **Configurable**: Sales/Marketing teams can update content without code changes
- **Intelligent**: Proactive nudges based on visitor behavior patterns
- **Natural**: Conversational lead capture feels organic, not like a form
- **Traceable**: Full visibility into bot decision-making process
- **Testable**: Preview tool allows testing scenarios before deployment

## 🚀 Next Steps

1. **Customize Content**: Update the JSON files with your company's specific information
2. **Add More Rules**: Create additional trigger conditions for different visitor types
3. **Expand Knowledge**: Add more Q&A pairs to cover common questions
4. **Integrate**: Connect to your CRM or lead management system
5. **Deploy**: Host on your preferred platform (Heroku, AWS, etc.)

This implementation provides a solid foundation for a production-ready sales bot that can be easily customized and extended based on your specific business needs.