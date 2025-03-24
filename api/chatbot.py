import streamlit as st
import os
import google.generativeai as ggi

st.set_page_config(page_title="Tarry from Eat-O-Mate", page_icon="https://github.com/StellarStrivers/Eat-O-Mate/blob/main/static/chatbot.png?raw=true")
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("img.png")
    }
    }
    </style>
    """,
    unsafe_allow_html=True
)

ggi.configure(api_key = os.getenv('API_KEY'))

model = ggi.GenerativeModel("gemini-pro") 
chat = model.start_chat()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def LLM_Response(question):
    question= question+" answer me a bit emotionally but not poetic, just a bit supportive"
    response = chat.send_message(question,stream=True)
    return response

st.title("Talk with Tarry")
for role, message in st.session_state.chat_history:
    if role != "user":
        st.markdown(f""" 
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px;'>
                {message}
            </div>
            <img src='https://github.com/StellarStrivers/Eat-O-Mate/blob/main/static/chatbot.png?raw=true' style='border-radius: 50%; margin-left: 10px;' />
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <img src='https://github.com/Tasneem-I/Eat-O-Mate/blob/main/static/chatuser.png?raw=true' style='border-radius: 50%; margin-right: 10px;' />
            <div style='background-color: #dff0d8; padding: 10px; border-radius: 10px; margin-right: 10px;'>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)


user_quest = st.text_input("Hey there, do you have any questions or require guidance? Even if you just neeed someone to talk to, I'm here for you.")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.session_state.chat_history.append(("user", user_quest))
    bot_response = " ".join([word.text for word in result])
    st.session_state.chat_history.append(("bot", bot_response))
    st.experimental_rerun()
    