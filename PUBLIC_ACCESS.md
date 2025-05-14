# 在公网上运行签名墙网站

我们提供了两种方法在公网上运行此签名墙网站：使用Django开发服务器或使用Gunicorn生产服务器。

## 方法一：使用Django开发服务器（推荐用于测试）

这种方法简单快捷，适合临时测试：

1. 确保您已安装所有依赖：
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. 运行我们提供的脚本：
```bash
./start_public_server.sh
```

3. 脚本将显示您的本地IP地址，您和同一局域网内的其他设备可以通过这个地址访问网站。

## 方法二：使用Gunicorn生产服务器（更接近生产环境）

这种方法更接近生产环境配置：

1. 确保安装了所有依赖：
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. 运行我们提供的生产模式脚本：
```bash
./start_production_server.sh
```

3. 同样，脚本会显示访问地址。

## 注意事项

1. 目前配置允许所有主机访问，这仅适用于测试环境。在实际生产环境中，应该限制允许访问的主机列表。

2. 默认使用的是SQLite数据库，适合小规模使用。如果需要处理更大的流量，建议切换到MySQL：

   - 在.env文件中设置：
   ```
   USE_SQLITE=False
   DB_NAME=signature_wall_db
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   ```

3. 为了真正的公网访问（而不仅仅是局域网），您需要：
   
   - 配置您的路由器进行端口转发（将外部端口转发到运行服务器的电脑）
   - 或使用内网穿透工具如ngrok、frp等
   - 或将网站部署到云服务器上
   
## macOS特有的端口开放设置

macOS用户需要注意以下事项来确保端口能正常开放：

1. 使用提供的macOS端口设置向导：
```bash
./macos_port_setup.sh
```

2. macOS防火墙基于应用程序而不是端口进行管理，需要在系统设置中允许Python应用接收传入连接：
   - 打开系统设置 → 网络 → 防火墙 → 防火墙选项
   - 找到Python应用并设置为"允许传入连接"

3. 如需高级配置，可以使用pf防火墙（需要管理员权限）：
```bash
# 加载防火墙规则
sudo pfctl -f macos_pf_rules.conf
# 启用pf防火墙
sudo pfctl -e
```

4. 端口占用问题：如果8000端口已被占用，可以使用以下命令查看和释放：
```bash
# 查看占用端口的进程
lsof -i :8000
# 终止占用端口的进程
lsof -ti :8000 | xargs kill -9
```

4. 在正式生产环境中，建议使用Nginx或Apache作为前端代理服务器，结合Gunicorn运行Django应用。
