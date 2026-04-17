# 🚀 快速开始指南

## 5分钟上手 BaziAI API

### 第一步：安装 Python 依赖

```bash
pip install requests
```

### 第二步：获取您的认证信息

#### 1. 获取 Session ID

打开 BaziAI 网站，从地址栏复制会话ID：

```
https://www.bazi-ai.com/zh/chat/26a7d080-283c-43c9-a741-23d8dfcb8512
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    这部分就是 Session ID
```

#### 2. 获取 Cookie

1. 在 BaziAI 网站上按 `F12` 打开开发者工具
2. 切换到 **Network（网络）** 标签
3. 点击 **Fetch/XHR** 过滤器
4. 在网站上发送一条测试消息
5. 点击出现的 `messages` 请求
6. 在右侧找到 **Headers** 标签
7. 向下滚动找到 **Request Headers** 部分
8. 复制 **Cookie** 的完整值

### 第三步：选择使用方式

#### 方式一：最简单 - 使用 `bazi_simple.py`

1. 打开 `bazi_simple.py`
2. 修改这两行：
   ```python
   SESSION_ID = "你的会话ID"
   COOKIE = """你的Cookie"""
   ```
3. 运行：
   ```bash
   python bazi_simple.py
   ```

#### 方式二：交互式 - 使用 `bazi_interactive.py`

1. 运行脚本：
   ```bash
   python bazi_interactive.py
   ```
2. 按提示输入 Session ID 和 Cookie
3. 使用命令与 BaziAI 交互

#### 方式三：编程使用 - 使用 `bazi_api.py`

```python
from bazi_api import BaziAI

# 创建客户端
client = BaziAI(
    session_id="你的会话ID",
    cookie="你的Cookie"
)

# 发送消息
client.send_message("请帮我分析运势")

# 获取聊天记录
messages = client.get_messages()

# 打印聊天记录
client.print_messages(messages)

# 保存到文件
client.save_messages_to_file(messages)
```

### 第四步：测试

运行任何一个脚本，如果看到类似输出，说明成功了：

```
✅ 消息发送成功！
消息ID: cedba3d8-7071-43b7-8f3b-61a63b754b1a
发送时间: 2026-04-16T13:20:42.402514+00:00
```

## 📝 常用示例

### 示例1：批量提问

```python
from bazi_api import BaziAI
import time

client = BaziAI(session_id="...", cookie="...")

questions = [
    "我今天的运势如何？",
    "我适合什么职业？",
    "我的财运怎么样？"
]

for q in questions:
    print(f"提问: {q}")
    client.send_message(q)
    time.sleep(3)  # 等待3秒避免请求过快
```

### 示例2：导出聊天记录

```python
from bazi_api import BaziAI

client = BaziAI(session_id="...", cookie="...")

# 获取所有消息
messages = client.get_messages()

# 保存为 JSON
client.save_messages_to_file(messages, "my_chat.json")

# 或者保存为文本格式
with open("my_chat.txt", "w", encoding="utf-8") as f:
    for msg in messages:
        role = "用户" if msg['role'] == 'user' else "AI"
        f.write(f"{role}: {msg['content']}\n\n")
```

### 示例3：监控新消息

```python
from bazi_api import BaziAI
import time

client = BaziAI(session_id="...", cookie="...")

last_count = 0

while True:
    messages = client.get_messages()
    current_count = len(messages)
    
    if current_count > last_count:
        # 有新消息
        new_messages = messages[last_count:]
        for msg in new_messages:
            print(f"新消息: {msg['content']}")
        last_count = current_count
    
    time.sleep(5)  # 每5秒检查一次
```

## ⚠️ 注意事项

1. **Cookie 会过期** - 如果出现认证错误，重新获取 Cookie
2. **请求限制** - 免费账户有使用次数限制
3. **请求频率** - 避免请求过快，建议间隔2-3秒
4. **隐私安全** - 不要分享您的 Cookie 和 Session ID

## 🆘 遇到问题？

### 问题1：`401 Unauthorized` 错误
**原因**：Cookie 过期或无效  
**解决**：重新登录网站，获取新的 Cookie

### 问题2：`404 Not Found` 错误
**原因**：Session ID 错误  
**解决**：检查 Session ID 是否正确

### 问题3：没有返回数据
**原因**：会话中没有消息  
**解决**：先在网站上发送一条消息

### 问题4：`ModuleNotFoundError: No module named 'requests'`
**原因**：未安装 requests 库  
**解决**：运行 `pip install requests`

## 📚 更多信息

查看 `README.md` 了解完整文档。

---

**祝您使用愉快！** 🎉
