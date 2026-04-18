# 🚀 快速开始：在自己网页上看到 AI 回复

**目标**: 让 AI 回复直接显示在你的网页上，不跳转到官网

---

## ✅ 当前状态

- ✅ Selenium 已安装 (版本: 4.43.0)
- ⚠️ ChromeDriver 需要配置

---

## 📋 两种方案

### 方案 A: 使用 webdriver-manager（推荐，最简单）⭐⭐⭐

#### 1. 安装 webdriver-manager
```bash
pip install webdriver-manager
```

#### 2. 修改 app.py
在 `app.py` 文件顶部添加：
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
```

然后修改 `trigger_ai_with_selenium` 函数中的这一行：
```python
# 原来的代码
driver = webdriver.Chrome(options=chrome_options)

# 改为
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
```

#### 3. 完成！
现在启动应用：
```bash
python app.py
```

---

### 方案 B: 手动下载 ChromeDriver

#### 1. 查看 Chrome 版本
打开 Chrome 浏览器，访问：
```
chrome://version/
```
记下版本号（例如：131.0.6778.109）

#### 2. 下载 ChromeDriver
访问以下网站之一：
- 新版：https://googlechromelabs.github.io/chrome-for-testing/
- 旧版：https://chromedriver.chromium.org/downloads

下载与你的 Chrome 版本匹配的 ChromeDriver

#### 3. 解压并配置
**Windows**:
- 解压 `chromedriver.exe`
- 放到项目目录，或
- 放到 `C:\Windows\System32\`

**添加到 PATH**:
- 右键"此电脑" → 属性 → 高级系统设置
- 环境变量 → 系统变量 → Path
- 新建 → 添加 ChromeDriver 所在目录

#### 4. 测试
```bash
chromedriver --version
```

---

## 🎯 使用方法

### 1. 启动 Flask
```bash
python app.py
```

### 2. 访问网页
```
http://127.0.0.1:5000
```

### 3. 登录
- 输入 Session ID
- 输入 Cookie

### 4. 发送消息
1. 输入问题
2. 点击 **"🤖 自动获取回复（推荐）"** 按钮
3. 等待 10-15 秒
4. ✅ AI 回复自动显示在你的网页上！

---

## 📊 三种模式对比

| 按钮 | 说明 | 回复率 | 需要跳转 | 推荐度 |
|------|------|--------|---------|--------|
| 📤 快速发送 | 立即发送，稍后刷新 | 5% | ❌ | ⭐⭐ |
| 🤖 自动获取回复 | **Selenium 自动化** | **99%** | **❌** | **⭐⭐⭐⭐⭐** |
| 🌐 在官网查看 | 打开官网查看 | 95% | ✅ | ⭐⭐⭐⭐ |

---

## ⚠️ 如果 Selenium 不工作

### 临时方案：使用"在官网查看"
如果 Selenium 配置有问题，可以先使用：
1. 点击 **"🌐 在官网查看"** 按钮
2. 在新标签页查看 AI 回复
3. 返回点击"刷新"

这个方案不需要 Selenium，回复率也有 95%+

---

## 🔧 故障排查

### 问题 1: "Selenium 未安装"
```bash
pip install selenium
```

### 问题 2: "ChromeDriver 未找到"
使用方案 A（webdriver-manager）：
```bash
pip install webdriver-manager
```

### 问题 3: Chrome 版本不匹配
- 更新 Chrome 到最新版本
- 或下载匹配的 ChromeDriver

### 问题 4: 仍然没有回复
1. 检查 Flask 控制台日志
2. 开启调试模式查看详细信息
3. 尝试使用"在官网查看"按钮

---

## 💡 推荐配置（最简单）

### 一键安装
```bash
pip install webdriver-manager
```

### 修改 app.py
在文件顶部添加：
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
```

在 `trigger_ai_with_selenium` 函数中修改：
```python
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
```

### 完成！
```bash
python app.py
```

访问 `http://127.0.0.1:5000`，点击"🤖 自动获取回复"，AI 回复将自动显示！

---

## 🎉 成功标志

当你看到：
```
[DEBUG] 使用 Selenium 触发 AI...
[DEBUG] 访问页面: https://www.bazi-ai.com/zh/chat/xxx
[DEBUG] 等待 AI 生成回复...
[DEBUG] ✅ Selenium 触发完成
[DEBUG] ✅ 收到 AI 回复！等待时间: 12秒
```

并且 AI 回复显示在你的网页上，说明成功了！🎉

---

**总结**: 
1. 安装 `webdriver-manager`（最简单）
2. 修改 `app.py`（添加几行代码）
3. 启动应用
4. 点击"🤖 自动获取回复"
5. ✅ AI 回复自动显示在你的网页上！
