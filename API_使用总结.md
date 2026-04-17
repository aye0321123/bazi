# 🎉 BaziAI API 使用总结

## ✅ 已完成的工作

### 1. Cookie 自动提取
- ✅ 成功提取 Cookie
- ✅ 保存到 `bazi_credentials.json`
- ✅ Cookie 有效期约 30 天

### 2. API 测试
- ✅ 获取消息列表 - 成功获取 10 条消息
- ✅ 发送消息 - 成功发送测试消息
- ✅ 所有 API 端点正常工作

### 3. 文档和示例
- ✅ 完整 API 文档 (`API_DOCUMENTATION.md`)
- ✅ 快速参考 (`API_QUICK_REFERENCE.md`)
- ✅ 简单示例 (`simple_api_example.py`)
- ✅ 完整客户端 (`bazi_api.py`)

---

## 🔑 您的 API 信息

### 基础配置

```python
BASE_URL = "https://www.bazi-ai.com"
SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"
COOKIE = "从 bazi_credentials.json 读取"
```

### API 端点

1. **获取消息**: `GET /api/chat-session/{session_id}/messages`
2. **发送消息**: `POST /api/chat-session/{session_id}/messages`

---

## 🚀 快速开始

### 方式 1: 使用简单示例（推荐新手）

```bash
python simple_api_example.py
```

这个脚本演示了：
- 如何获取消息列表
- 如何发送消息
- 基本的错误处理

### 方式 2: 使用封装好的类（推荐）

```python
from bazi_api import BaziAI
import json

# 读取凭证
with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']

# 创建客户端
client = BaziAI("26a7d080-283c-43c9-a741-23d8dfcb8512", cookie)

# 使用
messages = client.get_messages()
client.send_message("你好")
```

### 方式 3: 直接调用 API

```python
import requests
import json

# 读取 Cookie
with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']

# 获取消息
url = "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages"
headers = {"Cookie": cookie, "Content-Type": "application/json"}
response = requests.get(url, headers=headers)
messages = response.json()

# 发送消息
data = {
    "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
    "role": "user",
    "content": "你好",
    "id": ""
}
response = requests.post(url, headers=headers, json=data)
result = response.json()
```

---

## 📚 文档说明

### 1. API_DOCUMENTATION.md
**完整的 API 文档**，包含：
- API 概述和认证方式
- 所有 API 端点详细说明
- Python、JavaScript、PHP 代码示例
- 错误处理和故障排除
- 完整的 API 封装类

### 2. API_QUICK_REFERENCE.md
**快速参考卡片**，包含：
- 基本信息和配置
- API 端点快速查询
- 常用代码片段
- 快速故障排除

### 3. simple_api_example.py
**简单示例脚本**，演示：
- 基本的 API 调用
- 获取和发送消息
- 简单的错误处理

### 4. bazi_api.py
**完整的 Python 客户端**，提供：
- 封装好的 API 调用方法
- 自动错误处理
- 消息格式化和导出
- 易于使用的接口

---

## 💡 使用场景

### 1. 简单查询
```python
from bazi_api import BaziAI
import json

with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']

client = BaziAI("26a7d080-283c-43c9-a741-23d8dfcb8512", cookie)
client.send_message("请帮我分析一下今天的运势")
messages = client.get_messages()
print(messages[-1]['content'])  # 打印最新回复
```

### 2. 批量处理
```python
questions = [
    "今天的运势如何？",
    "本周的财运怎么样？",
    "感情方面有什么建议？"
]

for q in questions:
    client.send_message(q)
    time.sleep(2)  # 等待 2 秒

messages = client.get_messages()
# 处理所有回复
```

### 3. 自动化脚本
```python
import schedule
import time

def daily_fortune():
    client.send_message("请分析今天的运势")
    messages = client.get_messages()
    # 发送到邮件或其他通知渠道

# 每天早上 8 点运行
schedule.every().day.at("08:00").do(daily_fortune)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 4. Web 服务集成
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
client = BaziAI("26a7d080-283c-43c9-a741-23d8dfcb8512", cookie)

@app.route('/api/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    result = client.send_message(question)
    return jsonify(result)

app.run(port=8000)
```

---

## 🔧 常见问题

### Q1: Cookie 在哪里？
**A**: 在 `bazi_credentials.json` 文件中，使用以下代码读取：
```python
import json
with open('bazi_credentials.json', 'r') as f:
    cookie = json.load(f)['cookie']
```

### Q2: Cookie 过期了怎么办？
**A**: 重新运行提取脚本：
```bash
python get_cookie_v2.py
```

### Q3: 如何知道 Cookie 是否有效？
**A**: 运行测试脚本：
```bash
python test_api_detailed.py
```

### Q4: 可以在其他语言中使用吗？
**A**: 可以！查看 `API_DOCUMENTATION.md` 中的 JavaScript 和 PHP 示例。

### Q5: 如何处理错误？
**A**: 使用 try-except 捕获异常：
```python
try:
    messages = client.get_messages()
except Exception as e:
    print(f"错误: {e}")
```

---

## 📊 测试结果

### 最新测试（2026-04-17）

```
✅ 获取消息列表 - 成功获取 10 条消息
✅ 发送消息 - 消息 ID: 62ee8b59-5c64-4b08-96d0-a61dcae1c8ec
✅ 响应时间 - 平均 1-2 秒
✅ 所有功能正常
```

---

## 🎯 下一步

### 1. 立即测试
```bash
python simple_api_example.py
```

### 2. 阅读文档
- 查看 `API_DOCUMENTATION.md` 了解详细信息
- 查看 `API_QUICK_REFERENCE.md` 快速查询

### 3. 开始开发
- 使用 `bazi_api.py` 作为基础
- 根据需求修改和扩展

### 4. 集成到项目
- 将 API 调用集成到您的应用中
- 参考使用场景部分的示例

---

## 📁 文件清单

### API 相关
- ✅ `API_DOCUMENTATION.md` - 完整 API 文档
- ✅ `API_QUICK_REFERENCE.md` - 快速参考
- ✅ `simple_api_example.py` - 简单示例
- ✅ `bazi_api.py` - Python 客户端

### 凭证和配置
- ✅ `bazi_credentials.json` - 您的 Cookie
- ✅ `get_cookie_v2.py` - Cookie 提取脚本

### 测试工具
- ✅ `test_api_detailed.py` - 详细 API 测试
- ✅ `test_full_workflow.py` - 完整工作流程测试
- ✅ `test_login_api.py` - 登录测试

### Web 应用
- ✅ `app.py` - Flask Web 服务器
- ✅ `templates/index.html` - Web 界面

### 文档
- ✅ `README.md` - 项目说明
- ✅ `QUICKSTART.md` - 快速开始
- ✅ `USER_GUIDE.md` - 用户指南
- ✅ `完成总结.md` - 完成总结

---

## 🌟 总结

您现在拥有：

1. **✅ 有效的 API 凭证** - Cookie 和 Session ID
2. **✅ 完整的 API 文档** - 详细说明和示例
3. **✅ 可用的代码示例** - Python、JavaScript、PHP
4. **✅ 测试通过的功能** - 所有 API 端点正常
5. **✅ Web 界面** - 可视化操作界面

**您可以立即开始使用 BaziAI API 了！** 🚀

---

**最后更新**: 2026-04-17  
**状态**: ✅ 完成  
**测试**: ✅ 通过
