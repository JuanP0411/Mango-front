import requests
import streamlit as st
import json
from call_assistant import call_openai

if 'name' not in st.session_state:
    st.session_state['name'] = ''


image_name = ''
st.title("Mango Leaf Classifier")

image = st.image(image='mango.png',caption='uploaded image')
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    url = 'https://mango-classifier-api.onrender.com/get-predict'
    if uploaded_file.type == 'image/jpeg' :

        file_bytes = uploaded_file.getvalue()
        

        with st.spinner('Loading AI model'):
            response = requests.post(
            url=url,
            files={'file':file_bytes}
            )
    
        image.image(uploaded_file.getvalue(),caption='uploaded image')
        image_name_json = json.loads(response.text)
        st.session_state.name = image_name_json
    else : 
        st.warning(f"We do not support {uploaded_file.type}, currently we only suport .jpeg images")


if st.session_state.name != "" and st.session_state.name != "Healthy":
    st.write("Detected diseases: ", st.session_state.name)
elif st.session_state.name == "Healthy" :
    st.write("Your plant is healthy :)")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

if st.session_state.name != "" and st.session_state.name != "Healthy": 
    mango_disease = st.session_state.name
    temp_prompt = f"I have a mango crop with {mango_disease} how should I treat it, and what could be causing the diseases"
    st.session_state.messages.append({"role": "user", "content": temp_prompt})
    with st.chat_message("user"):
        st.write(temp_prompt)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)



if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_openai(st.session_state.name)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


st.caption('Created by Marco Fidel Vásquez, and Juan Pablo Herrera')