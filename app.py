import streamlit as st
from openai import OpenAI

st.title("PURER AI")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# irister_key = st.secrets["IRISTER_API_KEY"]

# 初始化 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lock_chat" not in st.session_state:
    st.session_state.lock_chat = False  # 默认解锁

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# **用户输入框（当 `lock_chat=True` 时禁用）**
if not st.session_state.lock_chat:
    user_input = st.chat_input("Type your message:")
else:
    st.chat_input("Waiting for AI response...", disabled=True)  # 禁用输入框

# 处理用户输入
if user_input:
    # **1️⃣ 立即锁定输入，防止重复**
    st.session_state.lock_chat = True

    # **2️⃣ 记录 & 显示用户输入**
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # **3️⃣ 显示 AI 回复（流式输出）**
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response_text = ""
        for chunk in stream:
            response_text += chunk  # 累计完整 AI 回复
            st.markdown(response_text)  # 逐步显示

    # **4️⃣ 记录 AI 回复**
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # **5️⃣ 解锁输入**
    st.session_state.lock_chat = False
