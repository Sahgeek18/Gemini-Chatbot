import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="🧠",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 🎨 Add custom CSS styles
st.markdown("""
    <style>
        /* Center title */
        .st-emotion-cache-18ni7ap {
            text-align: center;
        }

        /* Chat bubbles */
        .stChatMessage.user {
            background-color: #f0f2f6;
            border-radius: 12px;
            padding: 12px;
            margin: 10px 0;
        }

        .stChatMessage.assistant {
            background-color: #e8f4fd;
            border-radius: 12px;
            padding: 12px;
            margin: 10px 0;
        }

        /* Chat input styling */
        section[tabindex="0"] textarea {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }

        /* Page background and content styling */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
            margin: auto;
        }

        /* Title styling */
        h1 {
            color: #0d47a1;
        }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title
st.title("🤖 Gemini - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field
user_prompt = st.chat_input("Ask Gemini...")
if user_prompt:
    # Show user's message
    st.chat_message("user").markdown(user_prompt)

    # Get response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Show model response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
