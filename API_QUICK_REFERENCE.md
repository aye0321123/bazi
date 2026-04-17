# 🚀 BaziAI API 快速参考

## 📌 基本信息

```
Base URL: https://www.bazi-ai.com
Session ID: 26a7d080-283c-43c9-a741-23d8dfcb8512
Cookie: 从 bazi_credentials.json 获取
```

---

## 🔑 API 端点

### 1️⃣ 获取消息列表

```http
GET /api/chat-session/{session_id}/messages
```

**Python 示例**:
```python
import requests
import json

with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']

url = "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages"
headers = {"Cookie": cookie, "Content-Type": "application/json"}

response = requests.get(url, headers=headers)
messages = response.json()
print(f"共有 {len(messages)} 条消息")
```

**cURL 示例**:
```bash
curl -X GET "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages" \
  -H "Cookie: YOUR_COOKIE_HERE" \
  -H "Content-Type: application/json"
```

---

### 2️⃣ 发送消息

```http
POST /api/chat-session/{session_id}/messages
```

**请求体**:
```json
{
  "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
  "role": "user",
  "content": "你的问题",
  "id": ""
}
```

**Python 示例**:
```python
import requests
import json

with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']

url = "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages"
headers = {"Cookie": cookie, "Content-Type": "application/json"}
data = {
    "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
    "role": "user",
    "content": "请帮我分析一下今天的运势",
    "id": ""
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(f"消息已发送，ID: {result['id']}")
```

**cURL 示例**:
```bash
curl -X POST "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages" \
  -H "Cookie: YOUR_COOKIE_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
    "role": "user",
    "content": "请帮我分析一下今天的运势",
    "id": ""
  }'
```

---

## 📦 完整的 Python 类

```python
import requests
import json

class BaziAPI:
    def __init__(self):
        with open('bazi_credentials.json', 'r') as f:
            self.cookie = json.load(f)['cookie']
        self.session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
        self.base_url = "https://www.bazi-ai.com"
        self.headers = {
            "Cookie": self.cookie,
            "Content-Type": "application/json"
        }
    
    def get_messages(self):
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def send(self, content):
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        data = {
            "session_id": self.session_id,
            "role": "user",
            "content": content,
            "id": ""
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

# 使用
api = BaziAPI()
messages = api.get_messages()
result = api.send("你好")
```

---

## 🎯 快速开始

### 1. 运行简单示例

```bash
python simple_api_example.py
```

### 2. 使用封装好的类

```bash
python bazi_simple.py
```

### 3. 交互式使用

```bash
python bazi_interactive.py
```

---

## 📝 响应格式

### 消息对象

```json
{
  "id": "消息唯一ID",
  "session_id": "会话ID",
  "role": "user 或 assistant",
  "content": "消息内容",
  "created_at": "创建时间 (ISO 8601)",
  "reasoning_content": null
}
```

---

## ⚠️ 注意事项

1. **Cookie 必须完整** - 确保复制了完整的 Cookie 字符串
2. **Cookie 会过期** - 约 30 天后需要重新获取
3. **请求间隔** - 建议每次请求间隔 1-2 秒
4. **错误处理** - 始终检查响应状态码

---

## 🔧 故障排除

### 401 错误
```bash
# Cookie 过期，重新获取
python get_cookie_v2.py
```

### SSL 错误
```bash
# 安装 brotli
pip install brotli
```

### 超时错误
```python
# 增加超时时间
response = requests.get(url, headers=headers, timeout=30)
```

---

## 📚 相关文件

- `API_DOCUMENTATION.md` - 完整 API 文档
- `simple_api_example.py` - 简单示例
- `bazi_api.py` - 完整的 API 客户端
- `bazi_credentials.json` - 您的凭证文件

---

**快速测试**:
```bash
python simple_api_example.py
```
