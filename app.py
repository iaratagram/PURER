import streamlit as st
from openai import OpenAI

st.title("PURER AI v1013")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 初始化 lock_chat 状态
if "lock_chat" not in st.session_state:
    st.session_state["lock_chat"] = False

# 设置默认模型
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 根据 lock_chat 状态显示不同的输入框，并确保 user_input 始终被定义
if st.session_state.lock_chat:
    user_input = None  # 这里给 user_input 赋一个默认值
    st.chat_input("AI is responding...", disabled=True)
    st.stop()  # 阻止后续代码执行
else:
    user_input = st.chat_input("Type your message:")

# 如果用户有输入，则处理输入
if user_input:
    # 锁定输入，防止重复输入
    st.session_state["lock_chat"] = True
    

    # 记录并显示用户输入
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # rerun to refresh ui
    st.rerun()

    # 生成 AI 回复（流式输出）
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

    # 记录 AI 回复
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 解锁输入
    st.session_state.lock_chat = False

    # 强制刷新 UI
    st.rerun()
