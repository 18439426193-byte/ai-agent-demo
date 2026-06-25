import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.RYIHYXL.EEV9.MEUCIQCua9xM1UrwBGbYIpOzNT6aXYEoT0zMabqr9BBM8PJiEgIgVZECnFplU88Ddbkry8M2FviGz6IiSENJ0KIItS10dwY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ===== 工具函数 =====
def get_current_weather(location: str, unit: str = "摄氏度"):
    weather_db = {
        "北京": {"temp": 22, "condition": "晴朗"},
        "上海": {"temp": 26, "condition": "多云"},
        "深圳": {"temp": 30, "condition": "阵雨"},
        "杭州": {"temp": 18, "condition": "小雨"},
    }
    info = weather_db.get(location, {"temp": 25, "condition": "未知"})
    result = {"location": location, "temperature": info["temp"], "unit": unit, "condition": info["condition"]}
    return json.dumps(result, ensure_ascii=False)

# ===== 工具描述 =====
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

# ===== 核心对话 =====
messages = [{"role": "user", "content": "杭州天气怎么样？"}]

# 第一次请求：让模型判断是否要调用工具
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
    
    print(f"🔧 调用工具：{tool_call.function.name}，参数：{args}")
    
    # 执行真正的工具函数
    result = get_current_weather(**args)
    print(f"📊 工具返回：{result}")
    
    # 把模型的请求追加到历史
    messages.append(message)
    # 把工具执行结果追加到历史
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })
    
    # 第二次请求：把工具结果发给模型，生成最终回答
    final = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    
    print("\n🤖 最终回答：", final.choices[0].message.content)
else:
    print("模型直接回答：", message.content)