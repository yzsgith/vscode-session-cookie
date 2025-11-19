const request = require('supertest');
const app = require('../app');

describe('Session Management API', () => {
  let agent; // Supertest agent 用于保持Cookie跨请求

  beforeEach(() => {
    agent = request.agent(app); // 创建一个代理，自动管理Cookie
  });

  afterEach(async () => {
    // 清理：在每次测试后登出
    await agent.get('/logout');
  });

  it('should set session data and retrieve it in subsequent requests', async () => {
    // 第一个请求：设置会话
    const setResponse = await agent.get('/set-session');
    expect(setResponse.status).toBe(200);
    expect(setResponse.text).toMatch(/Session set!/);
    

    // 第二个请求：获取会话，应该能拿到之前设置的数据
    const getResponse = await agent.get('/get-session');
    expect(getResponse.status).toBe(200);

    const sessionData = getResponse.body;
    expect(sessionData.userId).toBeDefined();
    expect(sessionData.views).toBe(1); // 第一次访问/set-session后，views应为1

    // 第三个请求：再次访问/set-session，views应该增加
    await agent.get('/set-session');
    const finalGetResponse = await agent.get('/get-session');
    expect(finalGetResponse.body.views).toBe(2);
  });

  it('should destroy session on logout', async () => {
    // 先设置会话
    await agent.get('/set-session');
    const initialGetResponse = await agent.get('/get-session');
    expect(initialGetResponse.body.userId).toBeDefined();

    // 然后登出
    const logoutResponse = await agent.get('/logout');
    expect(logoutResponse.status).toBe(200);
    expect(logoutResponse.text).toBe('Logged out successfully.');

    // 登出后，会话数据应该为空或销毁
    const finalGetResponse = await agent.get('/get-session');
    // 根据我们的实现，登出后req.session.userId是undefined
    expect(finalGetResponse.body.userId).toBeUndefined();
    expect(finalGetResponse.body.views).toBeUndefined();
  });

  it('should not share sessions between different clients', async () => {
    const agent1 = request.agent(app);
    const agent2 = request.agent(app);

    // 客户端1设置会话
    await agent1.get('/set-session');
    const data1 = await agent1.get('/get-session').then(res => res.body);

    // 客户端2获取会话 (应该是空的)
    const data2 = await agent2.get('/get-session').then(res => res.body);

    expect(data1.userId).toBeDefined();
    expect(data2.userId).toBeUndefined(); // 客户端2不应该看到客户端1的会话

    await agent1.get('/logout');
    await agent2.get('/logout');
  });
});