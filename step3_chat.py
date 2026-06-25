from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.RYIHYXL.EEV9.MEUCIQCua9xM1UrwBGbYIpOzNT6aXYEoT0zMabqr9BBM8PJiEgIgVZECnFplU88Ddbkry8M2FviGz6IiSENJ0KIItS10dwY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = []# 这个列表会存储所有对话历史

print("智能问答系统启动（输入 exit 退出）\n")

while True:
    user_input = input("你：")
    if user_input == "exit":
        print("再见！")
        break
    
    # 把用户的话加入历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用API
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    
    # 获取模型的回答
    reply = response.choices[0].message.content
    
    # 把模型的回答也加入历史（这样它才能记住上下文）
    messages.append({"role": "assistant", "content": reply})
    
    print("AI：", reply)