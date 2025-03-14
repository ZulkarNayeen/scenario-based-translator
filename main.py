import streamlit as st
import time

def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

st.title("জুলকার বট - RAG খাইয়া বট হইলাম")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("আপনি কি বলতে চান?")
if prompt:
    with st.chat_message("user"):
       st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = f"আমি বুঝতে পারছি না 🥴🥴, আমি তো ছোটভাই বট 😭😭😭 {prompt}"
    
    with st.chat_message("assistant"):
        st.write_stream(stream_data(response))
    
    st.session_state.messages.append({"role": "assistant", "content": response})
