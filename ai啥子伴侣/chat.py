from platform import system

import streamlit as st
import os
from openai import OpenAI

st.title("AI啥子伴侣")
system_chatInput=("你是一个 helpful的啥子,爱发表情")
chatInput=st.chat_input("说些什么")

#配置环境变量DEEPSEEK_API_KEY
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)


st.set_page_config(
    page_title="ai啥子伴侣",
    page_icon="🦊",
    #布局
    layout="wide",
    #侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={}
)

#初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
for message in st.session_state.messages:# 遍历会话状态中的消息
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("你:").write(message["content"])
    # else:
    #     st.chat_message("assistant:").write(message["content"])



#聊天输入框
if chatInput:#字符串自动转为布尔值：非空字符串为True
    # 保存用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": chatInput})

    # 交互
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_chatInput},
            {"role": "user", "content": chatInput},
        ],
        stream=False

    )

    print("返回结果为",response.choices[0].message.content)
    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    st.rerun()