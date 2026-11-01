# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI
#配置环境变量DEEPSEEK_API_KEY
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)
#交互
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是个弱智，只会加和减"},
        {"role": "user", "content": "10-2*414，最后是多少"},
    ],
    stream=False

)
#输出
print(response.choices[0].message.content)