import streamlit as st
import time

# 🎯 Streamed response generator (Echo模式)
def response_generator(user_input):
    for word in user_input.split():
        yield word + " "
        time.sleep(0.05)  # 模拟流式生成的延迟

# 🎯 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎯 Streamlit UI
st.set_page_config(page_title="Streaming Chatbot", page_icon="💬", layout="centered")

st.title("💬 Streaming Echo Chatbot")
st.write("Send a message and I'll respond word by word!")

# 🎯 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎯 用户输入
if prompt := st.chat_input("Type a message..."):
    # 1️⃣ 记录用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2️⃣ 显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3️⃣ 生成流式 AI 回复
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))  # Echo 逻辑（流式）

    # 4️⃣ 记录 AI 回复
    st.session_state.messages.append({"role": "assistant", "content": response})

# 🎯 Reset 按钮
if st.button("Reset Chat"):
    st.session_state.messages = []  # 清空聊天记录
    st.experimental_rerun()  # 重新运行，刷新 UI
