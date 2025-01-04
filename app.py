import streamlit as st
from chatbot.bot import HiringBot, ConversationStage
from utils.data_handler import DataHandler
from utils.ui_helper import apply_custom_styling, analyze_sentiment, display_candidate_info
from utils.language_handler import LanguageHandler

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = ConversationStage.GREETING.value
    if 'bot' not in st.session_state:
        st.session_state.bot = HiringBot()
    if 'data_handler' not in st.session_state:
        st.session_state.data_handler = DataHandler()
    if 'sentiment_history' not in st.session_state:
        st.session_state.sentiment_history = []
    if 'language_handler' not in st.session_state:
        st.session_state.language_handler = LanguageHandler()

def main():
    # Apply custom styling
    apply_custom_styling()
    
    # Create two columns: main chat and sidebar
    main_col, sidebar_col = st.columns([3, 1])
    
    with main_col:
        st.title("TalentScout Hiring Assistant")
        
        # Language selector
        languages = {'en': 'English', 'es': 'Español', 'fr': 'Français'}
        selected_language = st.selectbox('Select Language', list(languages.keys()), 
                                       format_func=lambda x: languages[x])
        
        # Initialize session state
        initialize_session_state()
        st.session_state.language_handler.set_language(selected_language)
        
        # Display chat messages with sentiment analysis
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message["role"] == "user":
                    sentiment = analyze_sentiment(message["content"])
                    st.session_state.sentiment_history.append(sentiment)
        
        # Initial greeting
        if not st.session_state.messages:
            bot_response = st.session_state.bot.get_response("", st.session_state.current_stage)
            st.session_state.messages.append({"role": "assistant", "content": bot_response["response"]})
            st.session_state.current_stage = bot_response["next_stage"]
            st.rerun()
        
        # Chat input
        if user_input := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get bot response
            bot_response = st.session_state.bot.get_response(user_input, st.session_state.current_stage)
            
            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response["response"]})
            
            # Update conversation stage
            st.session_state.current_stage = bot_response["next_stage"]
            
            # Save data if interview is complete
            if st.session_state.current_stage == ConversationStage.FAREWELL.value:
                success, file_path = st.session_state.data_handler.save_candidate_data(
                    st.session_state.bot.candidate_info
                )
                if success:
                    st.success("Interview data saved successfully!")
                else:
                    st.error(f"Error saving interview data: {file_path}")
            
            st.rerun()
    
    # Display candidate information in sidebar
    with sidebar_col:
        display_candidate_info(st.session_state.bot.candidate_info)
        
        # Display sentiment analysis summary
        if st.session_state.sentiment_history:
            st.sidebar.markdown("### Sentiment Analysis")
            positive = st.session_state.sentiment_history.count('positive')
            neutral = st.session_state.sentiment_history.count('neutral')
            negative = st.session_state.sentiment_history.count('negative')
            
            st.sidebar.write(f"Positive responses: {positive}")
            st.sidebar.write(f"Neutral responses: {neutral}")
            st.sidebar.write(f"Negative responses: {negative}")

if __name__ == "__main__":
    main()