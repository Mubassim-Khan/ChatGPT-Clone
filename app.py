from openai import OpenAI, OpenAIError
import streamlit as st

# UI Configurations & Modifications
st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="./assets/favicon.png",
)
st.title("ChatGPT :orange[Clone]")
st.header("", divider="rainbow")
st.markdown("This clone of ChatGPT is made by fetching an API Key from OpenAI.")
st.markdown("ChatGPT can make mistakes. Consider checking important information.")

# Error handling for OpenAI API key authentication
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except OpenAIError as e:
    st.error(f"Error during OpenAI initialization: {e}")
    st.stop()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Error handling for OpenAI API call
        try:
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
