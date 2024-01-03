import requests
import streamlit as st
import json
from call_assistant import call_openai

if 'name' not in st.session_state:
    st.session_state['name'] = ''


image_name = ''
st.title("Mango Leaf Classifier")
image = st.image(image='Yotsuba_Nakano_FULL_BODY.webp',caption='uploaded image')
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    url = 'http://127.0.0.1:5555/get-predict'

    file_bytes = uploaded_file.getvalue()

    
    response = requests.post(
        url=url,
        files={'file':file_bytes}
    )
    image.image(uploaded_file.getvalue(),caption='uploaded image')
    image_name_json = json.loads(response.text)
    st.session_state.name = image_name_json
 


if st.session_state.name != "":
    st.write("diseases = ", st.session_state.name)


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

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