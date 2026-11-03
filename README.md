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

在 Streamlit Community Cloud 的应用设置中添加 Secret：

```toml
DEEPSEEK_API_KEY = "你的 DeepSeek API 密钥"
```

聊天记录只保存在当前浏览器会话中。应用重启或服务器重启后不会保留聊天记录。
