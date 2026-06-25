import json

def get_current_weather(location: str, unit: str = "摄氏度"):
    """获取指定城市的天气（模拟数据）"""
    # 模拟天气数据库
    weather_db = {
        "北京": {"temp": 22, "condition": "晴朗"},
        "上海": {"temp": 26, "condition": "多云"},
        "深圳": {"temp": 30, "condition": "阵雨"},
        "杭州": {"temp": 18, "condition": "小雨"},
        "广州": {"temp": 28, "condition": "晴天"},
        "成都": {"temp": 20, "condition": "阴天"},
    }
    
    info = weather_db.get(location)
    if info is None:
        info = {"temp": 25, "condition": "未知"}
    
    result = {
        "location": location,
        "temperature": info["temp"],
        "unit": unit,
        "condition": info["condition"]
    }
    return json.dumps(result, ensure_ascii=False)

# 测试函数是否正常工作
if __name__ == "__main__":
    print(get_current_weather("杭州"))
    # 输出：{"location": "杭州", "temperature": 18, "unit": "摄氏度", "condition": "小雨"}