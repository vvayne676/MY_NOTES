docker run -d -p 5672:5672 --name some-rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3.13-rc-management

```yaml
version: '3.3'
services:
  rabbit:
    image: heidiks/rabbitmq-delayed-message-exchange:latest
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=password
    ports:
      - "5672:5672"
      - "15672:15672"
```
docker run -d -p 5672:5672 -p 15672:15672 --name some-rabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=password heidiks/rabbitmq-delayed-message-exchange:3.8.27-management


下载 rabbitmq_delayed_message_exchange-3.12.0.ez

docker run -d -p 5672:5672 -p 15672:15672 --hostname my-rabbit --name some-rabbit rabbitmq:3.13-rc-management

docker cp rabbitmq_delayed_message_exchange-3.12.0.ez container_id:/opt/rabbitmq/plugins

docker commit  container_id new_image_name



docker run -d -p 5672:5672 -p 15672:15672 --hostname my-rabbit --name some-rabbit rabbitmy




rabbitmq-plugins enable rabbitmq_delayed_message_exchange


