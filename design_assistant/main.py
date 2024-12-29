import os

from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# load enviorment variable
load_dotenv()

# streamlit page setting
st.set_page_config(
    page_title='Solve your query',
    layout='centered'
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# initialising chat session if not present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
st.title("Your assistant is ready to chat")

# display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_promt = st.chat_input("Enter your Query")
if user_promt:
    # add user msg to the chat and display it
    st.chat_message("user").markdown(user_promt)
    # generate response from gemini
    gemini_response = st.session_state.chat_session.send_message(user_promt)

    # display response
    with st.chat_message('assistant'):
        st.markdown(gemini_response.text)
