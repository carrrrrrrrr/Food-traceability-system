// 用户数据存储
let users = [];

// 获取所有用户
export const getUsers = () => {
  // 从 localStorage 获取用户数据
  const storedUsers = localStorage.getItem('users');
  if (storedUsers) {
    users = JSON.parse(storedUsers);
  }
  return users;
};

// 保存用户数据到 localStorage
export const saveUsers = () => {
  localStorage.setItem('users', JSON.stringify(users));
};

// 添加新用户
export const addUser = (user) => {
  // 先获取最新的用户列表
  getUsers();
  
  // 检查账号是否已存在
  const existingUser = users.find(u => u.account === user.account);
  if (existingUser) {
    return {
      status: 'error',
      message: '账号已存在'
    };
  }
  
  // 生成用户ID
  const userId = users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1;
  
  // 创建新用户对象
  const newUser = {
    id: userId,
    username: user.username,
    account: user.account,
    password: user.password,
    identity: user.identity,
    createTime: new Date().toISOString()
  };
  
  // 添加到用户列表
  users.push(newUser);
  
  // 保存到 localStorage
  saveUsers();
  
  return {
    status: 'success',
    message: '注册成功'
  };
};

// 用户登录验证
export const verifyUser = (account, password) => {
  // 获取最新的用户列表
  getUsers();
  
  // 查找用户
  const user = users.find(u => u.account === account);
  
  // 验证用户和密码
  if (user && user.password === password) {
    return {
      status: 'success',
      message: '登录成功',
      data: {
        id: user.id,
        username: user.username,
        identity: user.identity
      }
    };
  } else {
    return {
      status: 'error',
      message: '账号或密码错误'
    };
  }
};