# ✅ Cookie 提取成功！

## 🎉 恭喜！

您的 BaziAI Cookie 已成功提取并测试通过！

---

## 📊 提取结果

### ✅ Cookie 信息
- **状态**: 已成功提取
- **长度**: 1225 字符
- **Cookie 数量**: 7 个
- **提取时间**: 2026-04-17 10:19:36
- **有效期**: 约 30 天

### ✅ API 测试结果
- **GET 请求**: ✅ 成功 (状态码 200)
- **POST 请求**: ✅ 成功 (状态码 200)
- **消息获取**: ✅ 成功 (获取到 3 条消息)
- **消息发送**: ✅ 成功

---

## 🎯 如何使用

### 方法 1: Web 界面（推荐）

1. **打开浏览器访问**: http://127.0.0.1:5000

2. **输入凭证**:
   - **Session ID**: `26a7d080-283c-43c9-a741-23d8dfcb8512`
   - **Cookie**: 从 `bazi_credentials.json` 文件中复制完整的 Cookie

3. **点击登录**

4. **开始使用**:
   - 发送消息
   - 查看历史记录
   - 导出聊天记录
   - 使用调试模式查看 API 调用详情

### 方法 2: Python 代码

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

# 发送消息
response = client.send_message("请帮我分析一下今天的运势")
print(response)

# 获取历史消息
messages = client.get_messages()
client.print_messages(messages)
```

---

## 📁 重要文件

| 文件 | 说明 |
|------|------|
| `bazi_credentials.json` | 🔑 **您的凭证文件**（包含 Cookie） |
| `get_cookie_v2.py` | 🤖 Cookie 自动提取脚本 |
| `test_api_detailed.py` | 🧪 API 测试脚本 |
| `app.py` | 🌐 Web 服务器 |
| `bazi_api.py` | 📡 API 客户端库 |
| `QUICK_COOKIE_GUIDE.md` | 📖 手动获取 Cookie 指南 |

---

## 📸 截图文件

提取过程中保存了以下截图，可用于调试：

- `step1_homepage.png` - 首页
- `step2_after_login_click.png` - 点击登录后
- `step3_email_option.png` - 选择邮箱登录
- `step4_email_entered.png` - 输入邮箱后
- `step5_password_entered.png` - 输入密码后
- `step6_after_submit.png` - 提交登录后
- `step7_final_page.png` - 最终页面

---

## 🔒 安全提示

### ⚠️ 重要！

1. **Cookie 是敏感信息**
   - 相当于您的登录凭证
   - 不要分享给他人
   - 不要上传到公共代码仓库

2. **保护您的凭证文件**
   ```bash
   # 将凭证文件添加到 .gitignore
   echo "bazi_credentials.json" >> .gitignore
   echo "config.py" >> .gitignore
   ```

3. **Cookie 会过期**
   - 通常 30 天后需要重新获取
   - 如果出现 401 错误，说明 Cookie 已过期
   - 重新运行 `python get_cookie_v2.py` 即可

4. **建议定期更换密码**
   - 每月更换一次密码
   - 更换后需要重新提取 Cookie

---

## 🚀 快速开始

### 启动 Web 服务器

```bash
python app.py
```

服务器将在 http://127.0.0.1:5000 启动

### 使用 Web 界面

1. 打开浏览器访问 http://127.0.0.1:5000
2. 粘贴 Session ID 和 Cookie
3. 点击登录
4. 开始使用！

### 使用 Python API

```bash
# 测试 API
python test_api_detailed.py

# 运行示例
python bazi_simple.py

# 交互式使用
python bazi_interactive.py
```

---

## 🔧 故障排除

### 问题 1: Cookie 不工作

**症状**: 401 错误或登录失败

**解决方法**:
1. 检查 Cookie 是否完整复制
2. 检查 Cookie 是否过期
3. 重新运行 `python get_cookie_v2.py` 获取新 Cookie

### 问题 2: Web 服务器无法访问

**症状**: 无法打开 http://127.0.0.1:5000

**解决方法**:
1. 检查服务器是否运行: `python app.py`
2. 检查端口是否被占用
3. 尝试使用其他端口: `python app.py --port 5001`

### 问题 3: 需要重新提取 Cookie

**解决方法**:
```bash
# 运行自动提取脚本
python get_cookie_v2.py

# 或使用手动方法（参考 QUICK_COOKIE_GUIDE.md）
```

---

## 📚 相关文档

- **快速开始**: `QUICKSTART.md`
- **用户指南**: `USER_GUIDE.md`
- **Cookie 指南**: `QUICK_COOKIE_GUIDE.md`
- **项目概览**: `PROJECT_OVERVIEW.md`
- **文件说明**: `FILES_OVERVIEW.md`

---

## 🎯 下一步

### 1. 测试 Web 界面
- 打开 http://127.0.0.1:5000
- 使用提取的 Cookie 登录
- 发送测试消息

### 2. 探索功能
- 查看历史消息
- 导出聊天记录
- 使用调试模式

### 3. 集成到您的项目
- 使用 `bazi_api.py` 作为库
- 参考 `bazi_simple.py` 示例
- 阅读 API 文档

---

## 💡 提示

1. **首次使用**: 建议先在 Web 界面测试
2. **开发调试**: 使用调试模式查看 API 调用
3. **自动化**: 使用 Python API 进行批量操作
4. **定期维护**: 每月更新一次 Cookie

---

## 📞 需要帮助？

如果遇到问题：
1. 查看相关文档
2. 检查错误截图
3. 运行测试脚本
4. 查看日志输出

---

## 🎉 成功！

您现在可以：
- ✅ 使用 Web 界面与 BaziAI 交互
- ✅ 使用 Python API 进行自动化
- ✅ 导出和分析聊天记录
- ✅ 集成到您的项目中

**祝您使用愉快！** 🚀

---

**最后更新**: 2026-04-17 10:19:36
