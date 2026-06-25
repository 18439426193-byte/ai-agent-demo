import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.RYIHYXL.EEV9.MEUCIQCua9xM1UrwBGbYIpOzNT6aXYEoT0zMabqr9BBM8PJiEgIgVZECnFplU88Ddbkry8M2FviGz6IiSENJ0KIItS10dwY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 天气函数（从第4步复制过来）
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

# 工具描述（告诉模型你有这个工具）
tools = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称，如：北京、上海、杭州、深圳"
                },
                "unit": {
                    "type": "string",
                    "enum": ["摄氏度", "华氏度"],
                    "description": "温度单位"
                }
            },
            "required": ["location"]
        }
    }
}]

# 问一个天气问题，看模型是否会触发工具调用
messages = [{"role": "user", "content": "杭州天气怎么样？"}]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# 检查模型是否要求调用工具
if message.tool_calls:
    tool_call = message.tool_calls[0]
    print("✅ 模型想调用工具：", tool_call.function.name)
    print("参数：", tool_call.function.arguments)
else:
    print("模型没有调用工具，直接回答：", message.content)