# 🔮 BaziAI API 完整文档

## 📋 目录

1. [API 概述](#api-概述)
2. [认证方式](#认证方式)
3. [API 端点](#api-端点)
4. [代码示例](#代码示例)
5. [错误处理](#错误处理)

---

## API 概述

### 基础信息

- **Base URL**: `https://www.bazi-ai.com`
- **认证方式**: Cookie 认证
- **数据格式**: JSON
- **编码**: UTF-8

### 您的凭证

```json
{
  "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
  "cookie": "从 bazi_credentials.json 获取"
}
```

---

## 认证方式

所有 API 请求都需要在 HTTP 请求头中包含以下信息：

```http
Cookie: __Secure-authjs.session-token=eyJhbGci...; _ga=GA1.1...; NEXT_LOCALE=zh; ...
Content-Type: application/json
Accept: */*
Origin: https://www.bazi-ai.com
Referer: https://www.bazi-ai.com/zh/chat/{session_id}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

---

## API 端点

### 1. 获取消息列表

**获取当前会话的所有消息**

```http
GET /api/chat-session/{session_id}/messages
```

#### 请求示例

```bash
curl -X GET "https://www.bazi-ai.com/api/chat-session/26a7d080-283c-43c9-a741-23d8dfcb8512/messages" \
  -H "Cookie: YOUR_COOKIE_HERE" \
  -H "Content-Type: application/json"
```

#### 响应示例

```json
[
  {
    "id": "cedba3d8-7071-43b7-8f3b-61a63b754b1a",
    "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
    "role": "user",
    "content": "我今天运势怎么样",
    "created_at": "2026-04-16T13:20:42.402514+00:00",
    "reasoning_content": null
  },
  {
    "id": "f8a2c3d4-...",
    "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
    "role": "assistant",
    "content": "根据您的八字...",
    "created_at": "2026-04-16T13:20:45.123456+00:00",
    "reasoning_content": null
  }
]
```

---

### 2. 发送消息

**向 AI 发送新消息**

```http
POST /api/chat-session/{session_id}/messages
```

#### 请求体

```json
{
  "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
  "role": "user",
  "content": "请帮我分析一下今天的运势",
  "id": ""
}
```

#### 请求示例

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

#### 响应示例

```json
{
  "id": "bc5b41aa-2f10-429b-b158-e29b8d955d4e",
  "session_id": "26a7d080-283c-43c9-a741-23d8dfcb8512",
  "role": "user",
  "content": "请帮我分析一下今天的运势",
  "created_at": "2026-04-17T04:04:55.913987+00:00",
  "reasoning_content": null
}
```

---

## 代码示例

### Python 示例

#### 方式 1: 使用 requests 库

```python
import requests
import json

# 配置
BASE_URL = "https://www.bazi-ai.com"
SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"

# 从文件读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    COOKIE = creds['cookie']

# 设置请求头
headers = {
    "Cookie": COOKIE,
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/zh/chat/{SESSION_ID}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 1. 获取消息列表
def get_messages():
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    response = requests.get(url, headers=headers)
    return response.json()

# 2. 发送消息
def send_message(content):
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    payload = {
        "session_id": SESSION_ID,
        "role": "user",
        "content": content,
        "id": ""
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 获取历史消息
    messages = get_messages()
    print(f"共有 {len(messages)} 条消息")
    
    # 发送新消息
    result = send_message("请帮我分析一下今天的运势")
    print(f"消息已发送，ID: {result['id']}")
```

#### 方式 2: 使用封装好的 BaziAI 类

```python
from bazi_api import BaziAI
import json

# 读取凭证
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)

# 创建客户端
client = BaziAI(
    session_id="26a7d080-283c-43c9-a741-23d8dfcb8512",
    cookie=creds['cookie']
)

# 获取消息
messages = client.get_messages()
print(f"共有 {len(messages)} 条消息")

# 发送消息
response = client.send_message("请帮我分析一下今天的运势")
print(f"消息已发送")

# 打印消息
client.print_messages(messages)

# 保存到文件
client.save_messages_to_file(messages)
```

---

### JavaScript/Node.js 示例

```javascript
const axios = require('axios');
const fs = require('fs');

// 配置
const BASE_URL = 'https://www.bazi-ai.com';
const SESSION_ID = '26a7d080-283c-43c9-a741-23d8dfcb8512';

// 读取 Cookie
const creds = JSON.parse(fs.readFileSync('bazi_credentials.json', 'utf8'));
const COOKIE = creds.cookie;

// 设置请求头
const headers = {
  'Cookie': COOKIE,
  'Content-Type': 'application/json',
  'Accept': '*/*',
  'Origin': BASE_URL,
  'Referer': `${BASE_URL}/zh/chat/${SESSION_ID}`,
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
};

// 1. 获取消息列表
async function getMessages() {
  const url = `${BASE_URL}/api/chat-session/${SESSION_ID}/messages`;
  const response = await axios.get(url, { headers });
  return response.data;
}

// 2. 发送消息
async function sendMessage(content) {
  const url = `${BASE_URL}/api/chat-session/${SESSION_ID}/messages`;
  const payload = {
    session_id: SESSION_ID,
    role: 'user',
    content: content,
    id: ''
  };
  const response = await axios.post(url, payload, { headers });
  return response.data;
}

// 使用示例
(async () => {
  try {
    // 获取历史消息
    const messages = await getMessages();
    console.log(`共有 ${messages.length} 条消息`);
    
    // 发送新消息
    const result = await sendMessage('请帮我分析一下今天的运势');
    console.log(`消息已发送，ID: ${result.id}`);
  } catch (error) {
    console.error('错误:', error.message);
  }
})();
```

---

### PHP 示例

```php
<?php

// 配置
$BASE_URL = 'https://www.bazi-ai.com';
$SESSION_ID = '26a7d080-283c-43c9-a741-23d8dfcb8512';

// 读取 Cookie
$creds = json_decode(file_get_contents('bazi_credentials.json'), true);
$COOKIE = $creds['cookie'];

// 设置请求头
$headers = [
    'Cookie: ' . $COOKIE,
    'Content-Type: application/json',
    'Accept: */*',
    'Origin: ' . $BASE_URL,
    'Referer: ' . $BASE_URL . '/zh/chat/' . $SESSION_ID,
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
];

// 1. 获取消息列表
function getMessages($BASE_URL, $SESSION_ID, $headers) {
    $url = $BASE_URL . '/api/chat-session/' . $SESSION_ID . '/messages';
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

// 2. 发送消息
function sendMessage($BASE_URL, $SESSION_ID, $headers, $content) {
    $url = $BASE_URL . '/api/chat-session/' . $SESSION_ID . '/messages';
    
    $payload = json_encode([
        'session_id' => $SESSION_ID,
        'role' => 'user',
        'content' => $content,
        'id' => ''
    ]);
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

// 使用示例
$messages = getMessages($BASE_URL, $SESSION_ID, $headers);
echo "共有 " . count($messages) . " 条消息\n";

$result = sendMessage($BASE_URL, $SESSION_ID, $headers, '请帮我分析一下今天的运势');
echo "消息已发送，ID: " . $result['id'] . "\n";

?>
```

---

## 错误处理

### 常见错误

#### 1. 401 Unauthorized

**原因**: Cookie 过期或无效

**解决方法**:
```bash
# 重新获取 Cookie
python get_cookie_v2.py
```

#### 2. 404 Not Found

**原因**: Session ID 错误或不存在

**解决方法**: 检查 Session ID 是否正确

#### 3. SSL Error

**原因**: SSL 连接问题

**解决方法**:
```python
# Python 中安装 brotli
pip install brotli

# 或禁用 SSL 验证（不推荐）
response = requests.get(url, headers=headers, verify=False)
```

#### 4. Timeout

**原因**: 网络超时

**解决方法**:
```python
# 增加超时时间
response = requests.get(url, headers=headers, timeout=30)
```

---

## 完整的 Python API 调用类

```python
import requests
import json
from datetime import datetime

class BaziAIAPI:
    """BaziAI API 封装类"""
    
    def __init__(self, session_id, cookie):
        self.base_url = "https://www.bazi-ai.com"
        self.session_id = session_id
        self.session = requests.Session()
        self.headers = {
            "Cookie": cookie,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/zh/chat/{session_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_messages(self):
        """获取消息列表"""
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        try:
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取消息失败: {e}")
            return []
    
    def send_message(self, content):
        """发送消息"""
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        payload = {
            "session_id": self.session_id,
            "role": "user",
            "content": content,
            "id": ""
        }
        try:
            response = self.session.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"发送消息失败: {e}")
            return None
    
    def get_latest_message(self):
        """获取最新消息"""
        messages = self.get_messages()
        return messages[-1] if messages else None
    
    def get_user_messages(self):
        """获取用户消息"""
        messages = self.get_messages()
        return [msg for msg in messages if msg.get('role') == 'user']
    
    def get_ai_messages(self):
        """获取 AI 回复"""
        messages = self.get_messages()
        return [msg for msg in messages if msg.get('role') == 'assistant']
    
    def export_to_json(self, filename=None):
        """导出消息到 JSON 文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bazi_chat_{timestamp}.json"
        
        messages = self.get_messages()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        print(f"已导出到: {filename}")
        return filename


# 使用示例
if __name__ == "__main__":
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    # 创建 API 实例
    api = BaziAIAPI(
        session_id="26a7d080-283c-43c9-a741-23d8dfcb8512",
        cookie=creds['cookie']
    )
    
    # 获取所有消息
    messages = api.get_messages()
    print(f"共有 {len(messages)} 条消息")
    
    # 发送消息
    result = api.send_message("请帮我分析一下今天的运势")
    if result:
        print(f"消息已发送，ID: {result['id']}")
    
    # 获取最新消息
    latest = api.get_latest_message()
    if latest:
        print(f"最新消息: {latest['content'][:50]}...")
    
    # 导出到文件
    api.export_to_json()
```

---

## 快速开始

### 1. 准备工作

```bash
# 安装依赖
pip install requests brotli

# 获取 Cookie
python get_cookie_v2.py
```

### 2. 使用 API

```python
from bazi_api import BaziAI
import json

# 读取凭证
with open('bazi_credentials.json', 'r') as f:
    creds = json.load(f)

# 创建客户端
client = BaziAI("26a7d080-283c-43c9-a741-23d8dfcb8512", creds['cookie'])

# 发送消息
client.send_message("你好")

# 获取消息
messages = client.get_messages()
```

---

## 注意事项

1. **Cookie 安全**
   - 不要分享您的 Cookie
   - 不要上传到公共代码仓库
   - 定期更新 Cookie

2. **请求频率**
   - 建议每次请求间隔 1-2 秒
   - 避免频繁请求导致封禁

3. **错误重试**
   - 遇到错误时自动重试 2-3 次
   - 使用指数退避策略

4. **Cookie 过期**
   - Cookie 通常 30 天过期
   - 过期后需要重新获取

---

## 相关文件

- `bazi_api.py` - Python API 客户端
- `bazi_credentials.json` - 您的凭证文件
- `get_cookie_v2.py` - Cookie 提取脚本
- `test_full_workflow.py` - 完整测试脚本

---

**最后更新**: 2026-04-17

**版本**: 1.0.0
