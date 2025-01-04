import streamlit as st
from textblob import TextBlob

def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
        <style>
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        
        .stMarkdown {
            line-height: 1.5;
        }
        
        .css-1aumxhk {
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def analyze_sentiment(text):
    """Analyze the sentiment of user messages"""
    analysis = TextBlob(text)
    
    # Get polarity score (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    # Determine sentiment category
    if polarity > 0.3:
        return 'positive'
    elif polarity < -0.3:
        return 'negative'
    else:
        return 'neutral'

def display_candidate_info(candidate_info):
    """Display candidate information in a formatted way"""
    st.sidebar.title("Candidate Information")
    
    if candidate_info:
        st.sidebar.markdown("### Profile Summary")
        for key, value in candidate_info.items():
            if key != 'technical_answers':
                st.sidebar.write(f"**{key.replace('_', ' ').title()}:** {value}")