// ========================================
// 浏览器控制台 API 调用脚本
// ========================================
// 使用方法：
// 1. 打开 https://www.bazi-ai.com/zh/chat
// 2. 按 F12 打开开发者工具
// 3. 切换到 Console (控制台) 标签
// 4. 复制粘贴下面的代码并回车
// ========================================

// 配置
const BASE_URL = 'https://www.bazi-ai.com';

// ========================================
// 函数1: 创建新对话
// ========================================
async function createNewChat() {
    console.log('🆕 创建新对话...');
    
    try {
        const response = await fetch(`${BASE_URL}/api/chat-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*'
            },
            body: JSON.stringify({})
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            const sessionId = result.data.uuid;
            console.log('✅ 新对话创建成功！');
            console.log('会话 ID:', sessionId);
            console.log('创建时间:', result.data.created_at);
            return sessionId;
        } else {
            console.error('❌ 创建失败:', result.message);
            return null;
        }
    } catch (error) {
        console.error('❌ 请求失败:', error);
        return null;
    }
}

// ========================================
// 函数2: 发送消息
// ========================================
async function sendMessage(sessionId, message) {
    console.log('📤 发送消息...');
    console.log('会话 ID:', sessionId);
    console.log('消息内容:', message);
    
    try {
        const response = await fetch(`${BASE_URL}/api/chat-session/${sessionId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*'
            },
            body: JSON.stringify({
                session_id: sessionId,
                role: 'user',
                content: message,
                id: ''
            })
        });
        
        const result = await response.json();
        
        console.log('✅ 消息已发送');
        console.log('消息 ID:', result.id);
        console.log('发送时间:', result.created_at);
        
        return result;
    } catch (error) {
        console.error('❌ 发送失败:', error);
        return null;
    }
}

// ========================================
// 函数3: 获取消息列表
// ========================================
async function getMessages(sessionId) {
    console.log('📥 获取消息列表...');
    
    try {
        const response = await fetch(`${BASE_URL}/api/chat-session/${sessionId}/messages`, {
            method: 'GET',
            headers: {
                'Accept': '*/*'
            }
        });
        
        const messages = await response.json();
        
        console.log(`✅ 获取到 ${messages.length} 条消息`);
        
        // 格式化显示
        messages.forEach((msg, index) => {
            const role = msg.role === 'user' ? '👤 用户' : '🤖 AI';
            console.log(`\n${index + 1}. ${role} [${msg.created_at}]`);
            console.log(`   ${msg.content}`);
        });
        
        return messages;
    } catch (error) {
        console.error('❌ 获取失败:', error);
        return [];
    }
}

// ========================================
// 函数4: 完整流程 - 创建对话并发送消息
// ========================================
async function createAndSend(message) {
    console.log('='=50);
    console.log('🚀 开始完整流程');
    console.log('='=50);
    
    // 步骤1: 创建新对话
    const sessionId = await createNewChat();
    if (!sessionId) {
        console.error('❌ 流程终止：无法创建对话');
        return null;
    }
    
    console.log('\n');
    
    // 步骤2: 发送消息
    const result = await sendMessage(sessionId, message);
    if (!result) {
        console.error('❌ 流程终止：无法发送消息');
        return null;
    }
    
    console.log('\n');
    console.log('='=50);
    console.log('✅ 流程完成');
    console.log('='=50);
    console.log(`\n🌐 对话链接: ${BASE_URL}/zh/chat/${sessionId}`);
    console.log('\n💡 提示: 刷新页面或访问上面的链接查看 AI 回复');
    
    // 自动跳转到新对话
    setTimeout(() => {
        window.location.href = `${BASE_URL}/zh/chat/${sessionId}`;
    }, 2000);
    
    return { sessionId, result };
}

// ========================================
// 函数5: 在当前页面发送消息
// ========================================
async function sendToCurrentChat(message) {
    // 从当前 URL 获取 session_id
    const urlParts = window.location.pathname.split('/');
    const sessionId = urlParts[urlParts.length - 1];
    
    if (!sessionId || sessionId === 'chat') {
        console.error('❌ 无法获取当前会话 ID');
        console.log('💡 请先打开一个对话，或使用 createAndSend() 创建新对话');
        return null;
    }
    
    console.log('📍 当前会话 ID:', sessionId);
    return await sendMessage(sessionId, message);
}

// ========================================
// 使用示例
// ========================================
console.log(`
╔════════════════════════════════════════════════════════════╗
║          🔮 BaziAI 浏览器 API 调用工具                    ║
╚════════════════════════════════════════════════════════════╝

📚 可用函数:

1️⃣  createNewChat()
   创建新对话
   示例: await createNewChat()

2️⃣  sendMessage(sessionId, message)
   发送消息到指定会话
   示例: await sendMessage('会话ID', '你好')

3️⃣  getMessages(sessionId)
   获取指定会话的所有消息
   示例: await getMessages('会话ID')

4️⃣  createAndSend(message)
   创建新对话并发送消息（推荐）
   示例: await createAndSend('请帮我分析一下今天的运势')

5️⃣  sendToCurrentChat(message)
   在当前打开的对话中发送消息
   示例: await sendToCurrentChat('继续分析')

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 快速开始:

// 方式1: 创建新对话并发送消息（自动跳转）
await createAndSend('你好，请用一句话介绍你自己')

// 方式2: 在当前对话中发送消息
await sendToCurrentChat('请帮我分析一下今天的运势')

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示:
- 所有函数都是异步的，需要使用 await
- AI 回复会在页面上自动显示
- 发送消息后等待几秒钟即可看到 AI 回复

╚════════════════════════════════════════════════════════════╝
`);

// 自动检测当前页面
if (window.location.pathname.includes('/chat/')) {
    const urlParts = window.location.pathname.split('/');
    const currentSessionId = urlParts[urlParts.length - 1];
    console.log(`\n✅ 检测到当前会话: ${currentSessionId}`);
    console.log(`💡 可以直接使用: await sendToCurrentChat('你的消息')`);
}
