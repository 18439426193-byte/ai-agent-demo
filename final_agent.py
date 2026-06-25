import json
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key-here"
)

def get_current_weather(location: str, unit: str = "摄氏度"):
    weather_db = {
        "北京": {"temp": 22, "condition": "晴朗"},
        "上海": {"temp": 26, "condition": "多云"},
        "深圳": {"temp": 30, "condition": "阵雨"},
        "杭州": {"temp": 18, "condition": "小雨"},
        "广州": {"temp": 28, "condition": "晴天"},
        "成都": {"temp": 20, "condition": "阴天"},
    }
    info = weather_db.get(location, {"temp": 25, "condition": "未知"})
    result = {"location": location, "temperature": info["temp"], "unit": unit, "condition": info["condition"]}
    return json.dumps(result, ensure_ascii=False)

tools = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"},
                "unit": {"type": "string", "enum": ["摄氏度", "华氏度"]}
            },
            "required": ["location"]
        }
    }
}]

# 存储对话历史
messages = []

print("🤖 AI Agent已启动（输入 exit 退出）\n")

while True:
    user_input = input("你：")
    if user_input == "exit":
        print("再见！")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    # 第一次请求
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        
        # 执行工具
        result = get_current_weather(**args)
        
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
        
        # 第二次请求
        final = client.chat.completions.create(
            model="qwen-plus",
            messages=messages
        )
        reply = final.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("AI：", reply)
    else:
        reply = message.content
        messages.append({"role": "assistant", "content": reply})
        print("AI：", reply)
