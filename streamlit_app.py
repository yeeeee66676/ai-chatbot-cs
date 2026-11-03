"""AI 啥子伴侣：一个可部署到 Streamlit Community Cloud 的聊天应用。"""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime
import logging
import os

import streamlit as st
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    PermissionDeniedError,
    RateLimitError,
)


logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="AI 啥子伴侣",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _get_secret(name: str) -> str | None:
    """Read a Cloud secret first, then fall back to an environment variable."""
    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        # Apps remain usable locally before .streamlit/secrets.toml is created.
        pass
    environment_value = os.getenv(name)
    return environment_value.strip() if environment_value else None


@st.cache_resource(show_spinner=False)
def _create_client(api_key: str) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=30.0,
        max_retries=1,
    )


def _new_session_id() -> str:
    base = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    candidate = base
    suffix = 2
    while candidate in st.session_state.saved_sessions:
        candidate = f"{base} ({suffix})"
        suffix += 1
    return candidate


def _reset_current_session() -> None:
    st.session_state.messages = []
    st.session_state.nick_name = ""
    st.session_state.character = ""
    st.session_state.session_id = _new_session_id()
    st.session_state.widget_epoch += 1


def _save_current_session() -> None:
    if not st.session_state.messages:
        return

    st.session_state.saved_sessions[st.session_state.session_id] = {
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "messages": [message.copy() for message in st.session_state.messages],
    }


def _start_new_session() -> None:
    _save_current_session()
    _reset_current_session()


def _load_session(session_id: str) -> None:
    if session_id == st.session_state.session_id:
        return

    _save_current_session()
    session = st.session_state.saved_sessions[session_id]
    st.session_state.messages = [message.copy() for message in session["messages"]]
    st.session_state.nick_name = session["nick_name"]
    st.session_state.character = session["character"]
    st.session_state.session_id = session_id
    st.session_state.widget_epoch += 1


def _delete_session(session_id: str) -> None:
    st.session_state.saved_sessions.pop(session_id, None)
    if session_id == st.session_state.session_id:
        _reset_current_session()


def _build_system_prompt() -> str:
    nickname = st.session_state.nick_name.strip() or "啥子"
    character = (
        st.session_state.character.strip()
        or "温暖、自然、可靠，擅长倾听并给出具体建议"
    )
    return (
        f"你叫{nickname}，是用户的 AI 伴侣。"
        f"你的性格和角色设定是：{character}。"
        "请使用自然、简洁的中文交流，根据上下文持续对话。"
    )


def _stream_reply(client: OpenAI) -> Generator[str, None, None]:
    messages = [
        {"role": "system", "content": _build_system_prompt()},
        *st.session_state.messages,
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
    )
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def _request_error_message(error: Exception) -> str:
    if isinstance(error, AuthenticationError):
        return "DeepSeek API 密钥无效或已失效，请重新生成密钥并更新云端 Secret。"
    if isinstance(error, PermissionDeniedError):
        return "DeepSeek 拒绝了该密钥的访问权限，请检查密钥权限。"
    if isinstance(error, RateLimitError):
        return "DeepSeek 请求过于频繁，请稍后再试。"
    if isinstance(error, APITimeoutError):
        return "连接 DeepSeek 超时，请稍后再试。"
    if isinstance(error, APIConnectionError):
        return "无法连接 DeepSeek，请稍后再试。"
    if isinstance(error, APIStatusError):
        return f"DeepSeek 请求失败（HTTP {error.status_code}），请稍后再试。"
    return "AI 服务暂时不可用，请稍后再试。"


st.session_state.setdefault("messages", [])
st.session_state.setdefault("nick_name", "")
st.session_state.setdefault("character", "")
st.session_state.setdefault("saved_sessions", {})
st.session_state.setdefault("widget_epoch", 0)
st.session_state.setdefault("session_id", _new_session_id())

api_key = _get_secret("DEEPSEEK_API_KEY")
client = _create_client(api_key) if api_key else None


with st.sidebar:
    st.subheader("聊天控制")
    if st.button(
        "新建会话",
        icon=":material/add_comment:",
        width="stretch",
    ):
        _start_new_session()
        st.rerun()

    st.caption("会话只保存在当前浏览器访问期间，不会与其他用户共享。")
    st.divider()
    st.subheader("会话历史")

    session_ids = sorted(
        st.session_state.saved_sessions,
        reverse=True,
    )
    if st.session_state.session_id not in session_ids and st.session_state.messages:
        session_ids.insert(0, st.session_state.session_id)

    if not session_ids:
        st.caption("还没有已保存的会话。")

    for session_id in session_ids:
        name_col, delete_col = st.columns([5, 1])
        with name_col:
            if st.button(
                session_id,
                key=f"load_{session_id}",
                icon=":material/chat_bubble:",
                width="stretch",
                type=(
                    "primary"
                    if session_id == st.session_state.session_id
                    else "secondary"
                ),
            ):
                _load_session(session_id)
                st.rerun()
        with delete_col:
            if st.button(
                "删除",
                key=f"delete_{session_id}",
                icon=":material/delete:",
            ):
                _delete_session(session_id)
                st.rerun()

    st.divider()
    st.subheader("伴侣设定")
    profile_key = f"{st.session_state.session_id}_{st.session_state.widget_epoch}"
    nickname = st.text_input(
        "昵称",
        value=st.session_state.nick_name,
        placeholder="例如：小狐狸",
        key=f"nickname_{profile_key}",
    )
    character = st.text_area(
        "角色设定",
        value=st.session_state.character,
        placeholder="例如：温柔、幽默，喜欢分享生活灵感",
        key=f"character_{profile_key}",
    )
    st.session_state.nick_name = nickname
    st.session_state.character = character

    if client is None:
        st.warning(
            "云端尚未配置 DeepSeek API 密钥，请先添加 `DEEPSEEK_API_KEY`。",
            icon=":material/key_off:",
        )


st.title("AI 啥子伴侣")
st.caption(f"当前会话：{st.session_state.session_id}")

if not st.session_state.messages:
    st.info(
        "先设置伴侣昵称和角色，然后开始聊天。"
        "云端不会保存聊天记录，请勿发送敏感信息。",
        icon=":material/waving_hand:",
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "说些什么",
    disabled=client is None,
    submit_mode="disable",
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(_stream_reply(client))
        except Exception as error:
            logger.exception("DeepSeek chat request failed")
            st.error(
                _request_error_message(error),
                icon=":material/error:",
            )
            _save_current_session()
        else:
            if reply:
                st.session_state.messages.append(
                    {"role": "assistant", "content": str(reply)}
                )
                _save_current_session()
