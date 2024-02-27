```bash
version: '3.7'  # 使用的docker-compose文件版本是3.7

services:  # 定义了要运行的服务

  consul-server1:  # 定义了一个名为consul-server1的服务
    image: hashicorp/consul:1.15.2  # 使用的镜像是hashicorp/consul，版本是1.15.2
    container_name: consul-server1  # 容器的名称将被设置为consul-server1
    restart: always  # 如果容器停止，总是尝试重启容器
    volumes:  # 挂载卷
     - ./config/server1.json:/consul/config/server1.json:ro  # 将主机上的./config/server1.json文件挂载到容器的/consul/config/server1.json，并设置为只读
     - ./certs/:/consul/config/certs/:ro  # 将主机上的./certs/目录挂载到容器的/consul/config/certs/目录，并设置为只读
    networks:  # 定义网络
      - consul  # 将服务连接到名为consul的网络
    ports:  # 端口映射
      - "8500:8500"  # 将容器的8500端口映射到主机的8500端口
      - "8600:8600/tcp"  # 将容器的8600端口映射到主机的8600端口，TCP协议
      - "8600:8600/udp"  # 将容器的8600端口映射到主机的8600端口，UDP协议
    command: "agent -bootstrap-expect=3"  # 容器启动时执行的命令，这里是启动Consul代理并设置期望的服务器节点数为3

```


```bash
docker run -d --name consul-server1 \
  --restart always \
  -v "$(pwd)/config/server1.json:/consul/config/server1.json:ro" \
  -v "$(pwd)/certs/:/consul/config/certs/:ro" \
  --network consul \
  -p 8500:8500 \
  -p 8600:8600/tcp \
  -p 8600:8600/udp \
  hashicorp/consul:1.15.2 \
  agent -bootstrap-expect=3

```