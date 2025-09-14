import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# Page configuration
st.set_page_config(
    page_title="Sales Page Quick-Answer & Lead Bot",
    page_icon="🤖",
    layout="wide"
)

class SalesBot:
    def __init__(self):
        self.knowledge_pack = self.load_knowledge_pack()
        self.rules_engine = self.load_rules_engine()
        self.lead_form = self.load_lead_form()
        self.leads = self.load_leads()
        
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'pages_visited' not in st.session_state:
            st.session_state.pages_visited = []
        if 'questions_answered' not in st.session_state:
            st.session_state.questions_answered = 0
        if 'keywords_mentioned' not in st.session_state:
            st.session_state.keywords_mentioned = []
        if 'scroll_depth' not in st.session_state:
            st.session_state.scroll_depth = 0
        if 'lead_capture_mode' not in st.session_state:
            st.session_state.lead_capture_mode = False
        if 'lead_capture_data' not in st.session_state:
            st.session_state.lead_capture_data = {}
        if 'current_lead_field' not in st.session_state:
            st.session_state.current_lead_field = 0
        if 'trace_log' not in st.session_state:
            st.session_state.trace_log = []

    def load_knowledge_pack(self) -> List[Dict]:
        try:
            with open('knowledge_pack.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_rules_engine(self) -> List[Dict]:
        try:
            with open('rules_engine.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_lead_form(self) -> List[Dict]:
        try:
            with open('lead_form.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_leads(self) -> List[Dict]:
        try:
            with open('leads.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_leads(self):
        with open('leads.json', 'w') as f:
            json.dump(self.leads, f, indent=2)

    def add_trace(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.trace_log.append(f"[{timestamp}] {message}")

    def find_best_answer(self, question: str) -> Optional[Dict]:
        """Find the best matching answer based on keywords"""
        question_lower = question.lower()
        best_match = None
        best_score = 0
        
        for entry in self.knowledge_pack:
            score = 0
            for keyword in entry['keywords']:
                if keyword.lower() in question_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = entry
        
        return best_match if best_score > 0 else None

    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from user input"""
        text_lower = text.lower()
        keywords = []
        
        # Check against all keywords in knowledge pack
        for entry in self.knowledge_pack:
            for keyword in entry['keywords']:
                if keyword.lower() in text_lower and keyword not in keywords:
                    keywords.append(keyword)
        
        return keywords

    def evaluate_rules(self) -> Optional[Dict]:
        """Evaluate current session state against rules engine"""
        current_state = {
            'pages_visited': st.session_state.pages_visited,
            'questions_answered': st.session_state.questions_answered,
            'keywords_mentioned': st.session_state.keywords_mentioned,
            'scroll_depth': st.session_state.scroll_depth
        }
        
        for rule in self.rules_engine:
            trigger = rule['trigger']
            match = True
            
            # Check pages visited
            if 'pages_visited' in trigger:
                if not any(page in current_state['pages_visited'] for page in trigger['pages_visited']):
                    match = False
            
            # Check questions answered
            if 'questions_answered' in trigger:
                if current_state['questions_answered'] < trigger['questions_answered']:
                    match = False
            
            # Check keywords mentioned
            if 'keywords_mentioned' in trigger:
                if not any(keyword in current_state['keywords_mentioned'] for keyword in trigger['keywords_mentioned']):
                    match = False
            
            # Check scroll depth
            if 'scroll_depth' in trigger:
                if current_state['scroll_depth'] < trigger['scroll_depth']:
                    match = False
            
            if match:
                return rule
        
        return None

    def process_user_input(self, user_input: str):
        """Process user input and generate response"""
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Extract keywords and update session state
        keywords = self.extract_keywords(user_input)
        st.session_state.keywords_mentioned.extend(keywords)
        st.session_state.keywords_mentioned = list(set(st.session_state.keywords_mentioned))  # Remove duplicates
        
        # Add trace
        self.add_trace(f"User asked: '{user_input}'. Keywords detected: {keywords}")
        
        # Check if in lead capture mode
        if st.session_state.lead_capture_mode:
            self.handle_lead_capture_input(user_input)
            return
        
        # Find best answer
        best_match = self.find_best_answer(user_input)
        
        if best_match:
            # Update questions answered
            st.session_state.questions_answered += 1
            
            # Add bot response
            response = f"**Answer:** {best_match['answer']}\n\n*Source: {best_match['source']}*"
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Add trace
            self.add_trace(f"Matched rule {best_match['id']}. Questions answered: {st.session_state.questions_answered}")
        else:
            # No match found
            response = "I'm not sure I understand your question. Could you rephrase it or ask about our pricing, security, integrations, or support?"
            st.session_state.messages.append({"role": "assistant", "content": response})
            self.add_trace("No matching answer found for user question")
        
        # Evaluate rules for nudges
        triggered_rule = self.evaluate_rules()
        if triggered_rule:
            nudge_message = triggered_rule['action']['message']
            st.session_state.messages.append({"role": "assistant", "content": f"💡 **Proactive Nudge:** {nudge_message}"})
            self.add_trace(f"Rule '{triggered_rule['rule_name']}' triggered. Firing nudge.")
            
            # Check if we should initiate lead capture
            if triggered_rule['action'].get('follow_up_action') == 'INITIATE_LEAD_CAPTURE':
                st.session_state.lead_capture_mode = True
                st.session_state.current_lead_field = 0
                st.session_state.lead_capture_data = {}
                self.add_trace("Initiating lead capture sequence")

    def handle_lead_capture_input(self, user_input: str):
        """Handle input during lead capture mode"""
        if user_input.lower() in ['no', 'nope', 'not now', 'skip']:
            st.session_state.lead_capture_mode = False
            st.session_state.messages.append({"role": "assistant", "content": "No problem! Feel free to ask me anything else about our platform."})
            self.add_trace("User declined lead capture")
            return
        
        # Get current field
        current_field = self.lead_form[st.session_state.current_lead_field]
        field_name = current_field['field']
        
        # Store the response
        st.session_state.lead_capture_data[field_name] = user_input
        
        # Move to next field
        st.session_state.current_lead_field += 1
        
        if st.session_state.current_lead_field < len(self.lead_form):
            # Ask next question
            next_field = self.lead_form[st.session_state.current_lead_field]
            question = next_field['prompt']
            if 'options' in next_field:
                options = ', '.join(next_field['options'])
                question += f" (Options: {options})"
            st.session_state.messages.append({"role": "assistant", "content": question})
        else:
            # Lead capture complete
            self.complete_lead_capture()

    def complete_lead_capture(self):
        """Complete the lead capture process"""
        # Add timestamp
        st.session_state.lead_capture_data['timestamp'] = datetime.now().isoformat()
        st.session_state.lead_capture_data['session_id'] = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save lead
        self.leads.append(st.session_state.lead_capture_data.copy())
        self.save_leads()
        
        # Reset lead capture mode
        st.session_state.lead_capture_mode = False
        st.session_state.current_lead_field = 0
        st.session_state.lead_capture_data = {}
        
        # Thank user
        name = st.session_state.lead_capture_data.get('name', 'there')
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"Thank you, {name}! I've captured your information and someone from our team will reach out to you within 24 hours. Is there anything else I can help you with?"
        })
        
        self.add_trace("Lead capture completed successfully")

    def render_admin_panel(self):
        """Render the admin control panel"""
        st.header("🔧 Admin Control Panel")
        
        # File uploaders
        st.subheader("Configuration Files")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            knowledge_file = st.file_uploader("Knowledge Pack", type=['json'], key="knowledge_upload")
            if knowledge_file:
                try:
                    data = json.load(knowledge_file)
                    with open('knowledge_pack.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    st.success("Knowledge pack updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating knowledge pack: {e}")
        
        with col2:
            rules_file = st.file_uploader("Rules Engine", type=['json'], key="rules_upload")
            if rules_file:
                try:
                    data = json.load(rules_file)
                    with open('rules_engine.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    st.success("Rules engine updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating rules engine: {e}")
        
        with col3:
            lead_form_file = st.file_uploader("Lead Form", type=['json'], key="lead_form_upload")
            if lead_form_file:
                try:
                    data = json.load(lead_form_file)
                    with open('lead_form.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    st.success("Lead form updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating lead form: {e}")
        
        # Situation Preview Tool
        st.subheader("🎯 Situation → Bot Action Preview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Simulate User Situation:**")
            current_page = st.selectbox("Current Page", ["/home", "/pricing", "/security", "/integrations", "/support"])
            scroll_depth = st.slider("Scroll Depth %", 0, 100, 50)
            questions_asked = st.number_input("Questions Asked", 0, 10, 0)
            
            # Simulate keywords mentioned
            st.write("**Keywords Mentioned:**")
            keyword_options = []
            for entry in self.knowledge_pack:
                keyword_options.extend(entry['keywords'])
            keyword_options = list(set(keyword_options))
            
            selected_keywords = st.multiselect("Select keywords", keyword_options)
            
            if st.button("Preview Bot Action"):
                # Simulate session state
                temp_pages = [current_page] if current_page != "/home" else []
                temp_questions = questions_asked
                temp_keywords = selected_keywords
                temp_scroll = scroll_depth
                
                # Find matching rule
                matching_rule = None
                for rule in self.rules_engine:
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
                    st.success(f"**Bot would say:**\n\n{matching_rule['action']['message']}")
                    st.info(f"**Rule triggered:** {matching_rule['rule_name']}")
                else:
                    st.info("No rules would trigger in this situation.")
        
        with col2:
            st.write("**Current Session State:**")
            st.json({
                "pages_visited": st.session_state.pages_visited,
                "questions_answered": st.session_state.questions_answered,
                "keywords_mentioned": st.session_state.keywords_mentioned,
                "scroll_depth": st.session_state.scroll_depth,
                "lead_capture_mode": st.session_state.lead_capture_mode
            })
        
        # Trace Log
        st.subheader("📋 Trace Log")
        if st.session_state.trace_log:
            trace_text = "\n".join(st.session_state.trace_log[-20:])  # Show last 20 entries
            st.text_area("Recent Activity", trace_text, height=200, disabled=True)
        else:
            st.info("No trace entries yet. Start chatting to see the bot's decision process!")
        
        # Captured Leads
        st.subheader("📊 Captured Leads")
        if self.leads:
            leads_df = st.dataframe(self.leads, use_container_width=True)
        else:
            st.info("No leads captured yet.")

    def render_live_demo(self):
        """Render the live demo chat interface"""
        st.header("💬 Live Demo - Sales Bot")
        
        # Chat interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask me anything about our platform..."):
            self.process_user_input(prompt)
            st.rerun()

def main():
    st.title("🤖 Sales Page Quick-Answer & Lead Bot")
    st.markdown("---")
    
    # Initialize bot
    bot = SalesBot()
    
    # Create two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        bot.render_admin_panel()
    
    with col2:
        bot.render_live_demo()

if __name__ == "__main__":
    main()