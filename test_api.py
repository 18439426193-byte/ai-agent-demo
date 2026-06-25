from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.RYIHYXL.EEV9.MEUCIQCua9xM1UrwBGbYIpOzNT6aXYEoT0zMabqr9BBM8PJiEgIgVZECnFplU88Ddbkry8M2FviGz6IiSENJ0KIItS10dwY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "请用一句话介绍你自己"}]
    )
    print("✅ API连接成功！")
    print("回答：", response.choices[0].message.content)
except Exception as e:
    print("❌ 出错了：", e)