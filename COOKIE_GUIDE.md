# 🍪 Cookie 自动提取指南

本指南介绍如何使用脚本自动获取 BaziAI 的 Cookie。

---

## 📋 方法选择

### 方法一：Selenium 自动化（推荐）✅
- **优点**: 最可靠，模拟真实浏览器
- **缺点**: 需要安装 ChromeDriver
- **文件**: `get_cookie.py`

### 方法二：简易版本
- **优点**: 无需浏览器，快速
- **缺点**: 可能不支持某些登录方式
- **文件**: `get_cookie_simple.py`

### 方法三：手动获取
- **优点**: 100% 可靠
- **缺点**: 需要手动操作
- **说明**: 见下文

---

## 🚀 方法一：使用 Selenium（推荐）

### 1. 安装依赖

```bash
pip install selenium
```

### 2. 安装 ChromeDriver

#### Windows:
1. 下载 ChromeDriver: https://chromedriver.chromium.org/downloads
2. 选择与您的 Chrome 版本匹配的版本
3. 解压到任意目录
4. 将目录添加到系统 PATH

#### 或使用自动安装:
```bash
pip install webdriver-manager
```

### 3. 运行脚本

```bash
python get_cookie.py
```

### 4. 按提示输入

```
📧 请输入邮箱: 您的邮箱
🔑 请输入密码: 您的密码
```

### 5. 等待完成

脚本会：
- 自动打开浏览器
- 访问 BaziAI 网站
- 自动登录
- 提取 Cookie
- 保存到 `bazi_credentials.json`

### 6. 查看结果

```bash
cat bazi_credentials.json
```

---

## ⚡ 方法二：简易版本

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行脚本

```bash
python get_cookie_simple.py
```

### 3. 输入凭证

按提示输入邮箱和密码

### 4. 查看结果

如果成功，Cookie 会保存到 `bazi_credentials_simple.json`

---

## 🖐️ 方法三：手动获取（最可靠）

### 步骤：

#### 1. 登录网站
访问: https://www.bazi-ai.com

#### 2. 打开开发者工具
按 **F12** 键

#### 3. 切换到 Network 标签
点击顶部的 **Network** 或 **网络**

#### 4. 过滤请求
点击 **Fetch/XHR** 过滤器

#### 5. 发送测试消息
在网站上发送任意消息

#### 6. 查看请求
- 点击 `messages` 请求
- 找到 **Headers** 标签
- 找到 **Request Headers** 部分
- 找到 **Cookie** 字段
- 复制完整的 Cookie 值

#### 7. 提取 Session ID
从浏览器地址栏复制：
```
https://www.bazi-ai.com/zh/chat/[这里是Session ID]
```

---

## 📝 使用提取的 Cookie

### 方式一：在 Web 界面使用

1. 打开: http://127.0.0.1:5000
2. 粘贴 Session ID
3. 粘贴 Cookie
4. 点击登录

### 方式二：在代码中使用

```python
import json

# 读取保存的凭证
with open('bazi_credentials.json', 'r') as f:
    creds = json.load(f)

session_id = creds['session_id']
cookie = creds['cookie']

# 使用凭证
from bazi_api import BaziAI

client = BaziAI(session_id, cookie)
messages = client.get_messages()
```

---

## 🔧 故障排除

### 问题1: ChromeDriver 版本不匹配

**错误信息**:
```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX
```

**解决方法**:
1. 检查 Chrome 版本: 打开 Chrome → 设置 → 关于 Chrome
2. 下载匹配的 ChromeDriver: https://chromedriver.chromium.org/downloads
3. 或使用 webdriver-manager:
   ```bash
   pip install webdriver-manager
   ```
   然后修改脚本:
   ```python
   from webdriver_manager.chrome import ChromeDriverManager
   driver = webdriver.Chrome(ChromeDriverManager().install())
   ```

### 问题2: 找不到 ChromeDriver

**错误信息**:
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```

**解决方法**:
1. 下载 ChromeDriver
2. 将其路径添加到系统 PATH
3. 或在代码中指定路径:
   ```python
   driver = webdriver.Chrome(executable_path='C:/path/to/chromedriver.exe')
   ```

### 问题3: 登录失败

**可能原因**:
- 邮箱或密码错误
- 需要验证码
- 网站结构变化

**解决方法**:
1. 检查邮箱密码
2. 查看错误截图 `error_*.png`
3. 使用手动方法获取 Cookie

### 问题4: Cookie 过期

**症状**:
- 登录失败
- 401 错误

**解决方法**:
- 重新运行脚本获取新的 Cookie
- Cookie 通常 1-2 周过期

---

## 🔒 安全提示

1. **不要分享 Cookie**
   - Cookie 相当于登录凭证
   - 不要上传到公共仓库

2. **定期更换密码**
   - 建议每月更换一次

3. **使用环境变量**
   ```bash
   export BAZI_EMAIL="your@email.com"
   export BAZI_PASSWORD="your_password"
   ```

4. **删除敏感文件**
   ```bash
   # 使用完后删除
   rm bazi_credentials.json
   rm bazi_credentials_simple.json
   ```

---

## 📊 文件说明

| 文件 | 说明 |
|------|------|
| `get_cookie.py` | Selenium 自动化脚本 |
| `get_cookie_simple.py` | 简易版本脚本 |
| `bazi_credentials.json` | 保存的凭证（Selenium） |
| `bazi_credentials_simple.json` | 保存的凭证（简易版） |
| `error_*.png` | 错误截图 |

---

## 💡 最佳实践

1. **首次使用**: 使用 Selenium 版本
2. **快速测试**: 使用简易版本
3. **生产环境**: 使用手动获取的 Cookie
4. **自动化**: 定期运行脚本更新 Cookie

---

## 🆘 需要帮助？

如果遇到问题：
1. 查看错误截图
2. 检查 Chrome 和 ChromeDriver 版本
3. 尝试手动获取 Cookie
4. 查看项目文档

---

**祝您使用愉快！** 🎉
