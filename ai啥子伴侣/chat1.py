from platform import system

import streamlit as st
import os
from openai import OpenAI

from datetime import datetime

import json




def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果要删除的是当前会话，则需要生成新的会话信息
            if session_name ==st.session_state.session_id:
                st.session_state.messages=[]

                st.session_state.session_id=generate_session_name()
    except Exception :
        st.error("删除会话失败！！！")


#记载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            #读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)

                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.character = session_data["character"]
                st.session_state.session_id=session_name
    except Exception :
        st.error("加载会话失败！！！")


#加载所有会话
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list=os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list


#生成会话标识
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
#昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = ""
#性格
if 'character' not in st.session_state:
    st.session_state.character = ""

#会话标识
if 'session_id' not in st.session_state:
    st.session_state.session_id = generate_session_name()
#页面配置项
st.set_page_config(
    page_title="ai啥子伴侣",
    page_icon="🦊",
    #布局
    layout="wide",
    #侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={}
)


#保存会话信息的函数
def save_session():

    # 保存会话
    if st.session_state.session_id:
        #构建新会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "character": st.session_state.character,
            "session_id": st.session_state.session_id,
            "messages": st.session_state.messages
        }
        #   存入或创建文件夹
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 存储会话
        with open(f"sessions/{st.session_state.session_id}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)


# 侧边栏
# st.sidebar.subheader("## 侧边栏标题")
# nick_name=st.sidebar.text_input("## 输入框标题", "默认文本")

with st.sidebar:
    #会话信息
    st.subheader("AI控制面板")
    #新建会话信息
    if st.button("新建会话", width="stretch", icon="🔄"):
        # 保存当前会话
        save_session()

        #创建新会话
        if st.session_state.messages:
            st.session_state.messages = []#如果聊天信息非空：true，否则：false
            st.session_state.session_id = generate_session_name()
            save_session()
            st.rerun()#重新运行当前页面

    #会话历史
    st.text("会话历史")

    session_list=load_sessions()
    for session in session_list:
        col1,col2=st.columns([5,1])
        with col1:#加载会话信息
            #
            if st.button(session,width="stretch",icon="😚",key=f"load_{session}",type="primary" if session==st.session_state.session_id else "secondary"):
                load_session(session)
                st.rerun()
        with col2:#删除会话信息
            if st.button("",width="stretch",icon="☠️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


    #分割线
    st.divider()


    st.subheader("伴侣信息")
    nick_name=st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    character=st.text_area("画像",placeholder="请输入角色性格",value=st.session_state.character)
    if character:
        st.session_state.character = character




st.title("AI啥子伴侣")
system_chatInput="""你是一个 helpful的助手,你的名字是%s,你的角色是%s"""
chatInput=st.chat_input("说些什么")

#配置环境变量DEEPSEEK_API_KEY
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)


#展示聊天信息
st.text(f"聊天记录:{st.session_state.session_id}")
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
    st.chat_message("user").write(chatInput)
    # 交互
    print([
            {"role": "system", "content": system_chatInput},
            *st.session_state.messages
        ])
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_chatInput%(st.session_state.nick_name,st.session_state.character)},
            *st.session_state.messages
        ],
        stream=True

    )
#非流式  （
    # print("返回结果为",response.choices[0].message.content)
    # #保存大模型返回的结果
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    # st.rerun()  ）
#流式
    response_message=st.empty()
    full_response=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            full_response+=content
            response_message.chat_message("assistant").write(full_response)

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #等待大模型返回结果后立即保存会话
    save_session()