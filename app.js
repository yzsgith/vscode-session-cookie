const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('express-session');

// 导入我们的内存会话存储
const MemoryStore = require('./memory-store')(session);

const app = express();

// 中间件：解析Cookie
app.use(cookieParser());

// 中间件：会话管理
app.use(session({
  name: 'sessionId', // 可选的，自定义Cookie名称，默认是 'connect.sid'
  secret: 'your-secret-key', // 必填，用于签名会话ID Cookie的密钥
  resave: false, // 避免每次请求都重新保存会话，除非有修改
  saveUninitialized: false, // 避免保存未初始化的空会话
  store: new MemoryStore(), // 使用内存存储进行持久化
  cookie: {
    httpOnly: true, // 防止客户端JS读取Cookie，增强安全性
    maxAge: 1000 * 60 * 60 * 24 // Cookie过期时间（例如24小时）
  }
}));

// 示例路由：设置会话
app.get('/set-session', (req, res) => {
  req.session.userId = 'user_' + Math.floor(Math.random() * 1000);
  req.session.views = (req.session.views || 0) + 1;
  res.send(`Session set! UserId: ${req.session.userId}, Views: ${req.session.views}`);
});

// 示例路由：获取会话
app.get('/get-session', (req, res) => {
  const sessionData = {
    userId: req.session.userId,
    views: req.session.views
  };
  res.json(sessionData);
});

// 示例路由：销毁会话（登出）
app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).send('Could not log out.');
    }
    res.send('Logged out successfully.');
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = app; // 导出供测试使用