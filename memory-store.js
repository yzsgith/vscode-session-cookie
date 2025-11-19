module.exports = function (session) {
  const store = new session.MemoryStore(); // 实际上express-session自带了一个MemoryStore，这里我们直接用它
  // 但为了演示如何自定义一个存储，我们可以包装它或添加日志。
  // 这里我们直接返回原生的 MemoryStore 构造函数。
  return session.MemoryStore;
};