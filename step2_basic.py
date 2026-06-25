from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.RYIHYXL.EEV9.MEUCIQCua9xM1UrwBGbYIpOzNT6aXYEoT0zMabqr9BBM8PJiEgIgVZECnFplU88Ddbkry8M2FviGz6IiSENJ0KIItS10dwY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 第一次对话
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "你是一个有用的AI助手。"},
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
)

print(response.choices[0].message.content)