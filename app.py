import streamlit as st
from openai import OpenAI

st.title("PURER AI v1013")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# irister_key = st.secrets["IRISTER_API_KEY"]



# set lock chat state
if "lock_chat" not in st.session_state:
    st.session_state["lock_chat"] = False

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.lock_chat:
    st.chat_input("AI is responding...", disabled=True)  # **锁定输入**
else:
    user_input = st.chat_input("Type your message:", disabled=False)

# Accept user input
if user_input:

    ## lock chat after user send msg
    st.session_state["lock_chat"] = True
    ## rerun to refresh ui
    st.rerun()

    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # **5️⃣ 解锁输入**
    st.session_state.lock_chat = False
    st.rerun()