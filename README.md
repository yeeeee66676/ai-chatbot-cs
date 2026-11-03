# AI 啥子伴侣

一个使用 Streamlit 和 DeepSeek 构建的中文聊天应用。

## 本地运行

1. 安装依赖：

   ```powershell
   pip install -r requirements.txt
   ```

2. 设置 API 密钥：

   ```powershell
   $env:DEEPSEEK_API_KEY = "你的 DeepSeek API 密钥"
   ```

3. 启动应用：

   ```powershell
   streamlit run streamlit_app.py
   ```

## Streamlit Community Cloud

部署时使用以下配置：

- Repository：`yeeeee66676/ai-chatbot-cs`
- Branch：`main`
- Main file path：`streamlit_app.py`

登录 Streamlit Community Cloud 后，可以直接使用
[部署入口](https://share.streamlit.io/deploy?repository=https%3A%2F%2Fgithub.com%2Feeeee66676%2Fai-chatbot-cs&branch=main&mainModule=streamlit_app.py)
创建应用。

在 Streamlit Community Cloud 的应用设置中添加 Secret：

```toml
DEEPSEEK_API_KEY = "你的 DeepSeek API 密钥"
```

聊天记录只保存在当前浏览器会话中。应用重启或服务器重启后不会保留聊天记录。
