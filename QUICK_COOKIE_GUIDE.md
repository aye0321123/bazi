# 🍪 快速获取 Cookie 指南

由于自动化脚本可能遇到网站结构变化或验证码问题，这里提供最可靠的**手动获取方法**。

---

## 📋 手动获取 Cookie（5分钟完成）

### 步骤 1: 登录网站
1. 打开浏览器访问: https://www.bazi-ai.com/zh
2. 使用您的账号登录
   - 邮箱: 291568499@qq.com
   - 密码: hzy020618

### 步骤 2: 打开开发者工具
按键盘上的 **F12** 键（或右键点击页面 → 检查）

### 步骤 3: 切换到 Network 标签
在开发者工具顶部找到 **Network**（网络）标签并点击

### 步骤 4: 过滤请求
点击 **Fetch/XHR** 按钮（过滤器）

### 步骤 5: 发送测试消息
在网站的聊天框中输入任意消息（例如："你好"）并发送

### 步骤 6: 查看请求
1. 在 Network 标签中会出现新的请求
2. 找到名为 `messages` 或 `send` 的请求
3. 点击这个请求

### 步骤 7: 复制 Cookie
1. 在右侧面板找到 **Headers**（标头）标签
2. 向下滚动找到 **Request Headers**（请求标头）部分
3. 找到 **Cookie:** 这一行
4. 复制整行 Cookie 的值（很长的一串文本）

### 步骤 8: 获取 Session ID
从浏览器地址栏复制 Session ID：
```
https://www.bazi-ai.com/zh/chat/[这里就是您的Session ID]
```

例如您的 Session ID 是: `26a7d080-283c-43c9-a741-23d8dfcb8512`

---

## 🎯 使用提取的 Cookie

### 方法 1: 在 Web 界面使用

1. 打开: http://127.0.0.1:5000
2. 在 "Session ID" 框中粘贴: `26a7d080-283c-43c9-a741-23d8dfcb8512`
3. 在 "Cookie" 框中粘贴您复制的完整 Cookie
4. 点击 "登录" 按钮
5. 现在可以开始使用了！

### 方法 2: 保存到配置文件

创建 `config.py` 文件：

```python
# BaziAI 配置
SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"
COOKIE = "您复制的完整Cookie内容"
```

然后在代码中使用：

```python
from bazi_api import BaziAI
import config

client = BaziAI(config.SESSION_ID, config.COOKIE)
messages = client.get_messages()
print(messages)
```

---

## 📸 图解说明

### Cookie 在哪里？
```
开发者工具 (F12)
  └─ Network (网络)
      └─ Fetch/XHR
          └─ messages 请求
              └─ Headers (标头)
                  └─ Request Headers (请求标头)
                      └─ Cookie: [这里就是您要复制的内容]
```

### Cookie 长什么样？
```
Cookie: _ga=GA1.1.123456789.1234567890; _ga_ABC123=GS1.1.1234567890.1.1.1234567890.0.0.0; session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**注意**: Cookie 通常很长（几百到几千字符），要完整复制！

---

## ⚠️ 重要提示

1. **Cookie 是敏感信息**
   - 相当于您的登录凭证
   - 不要分享给他人
   - 不要上传到公共代码仓库

2. **Cookie 会过期**
   - 通常 1-2 周后需要重新获取
   - 如果出现 401 错误，说明 Cookie 已过期

3. **安全建议**
   - 使用完后建议修改密码
   - 定期更换 Cookie
   - 不要在公共电脑上操作

---

## 🔧 故障排除

### 问题 1: 找不到 Cookie
**解决**: 
- 确保已经登录
- 确保发送了消息（触发网络请求）
- 刷新页面重试

### 问题 2: Cookie 不工作
**解决**:
- 检查是否完整复制（没有遗漏）
- 检查 Session ID 是否正确
- 重新获取新的 Cookie

### 问题 3: 401 错误
**解决**:
- Cookie 已过期，需要重新获取

---

## 💡 小技巧

1. **快速测试**: 获取 Cookie 后，先在 Web 界面测试是否可用
2. **保存备份**: 将 Cookie 保存到文本文件，方便下次使用
3. **定期更新**: 建议每周更新一次 Cookie

---

## 📞 需要帮助？

如果遇到问题：
1. 检查是否已登录网站
2. 确认 F12 开发者工具已打开
3. 确保发送了消息（触发网络请求）
4. 查看 Network 标签中是否有请求

---

**预计完成时间**: 5 分钟 ⏱️

**成功率**: 100% ✅

祝您使用愉快！🎉
