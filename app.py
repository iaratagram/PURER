import streamlit as st
from openai import OpenAI

st.title("PURER AI v1013")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🔹 初始化 `lock_chat` 状态
if "lock_chat" not in st.session_state:
    st.session_state["lock_chat"] = False

# 🔹 设置默认 AI 模型
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# 🔹 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🔹 **锁定输入框（防止用户重复输入）**
if st.session_state.lock_chat:
    st.chat_input("AI is responding...", disabled=True)
    st.stop()  # **阻止用户继续输入**
else:
    user_input = st.chat_input("Type your message:")

# 🔹 **处理用户输入**
if user_input:
    # **1️⃣ 立即锁定输入**
    st.session_state.lock_chat = True
    st.rerun()  # **立即刷新 UI 让输入框禁用**

# **2️⃣ 记录 & 显示用户输入**
st.session_state.messages.append({"role": "user", "content": user_input})
with st.chat_message("user"):
    st.markdown(user_input)

# **3️⃣ 生成 AI 回复（流式输出）**
with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )
    
    response_text = ""  # **用于存储完整 AI 回复**
    response_placeholder = st.empty()  # **逐步显示回复**
    
    for chunk in stream:
        response_text += chunk
        response_placeholder.markdown(response_text)

# **4️⃣ 存储 AI 回复**
st.session_state.messages.append({"role": "assistant", "content": response_text})

# **5️⃣ 解除锁定**
st.session_state.lock_chat = False
st.rerun()  # **解锁输入并刷新 UI**
