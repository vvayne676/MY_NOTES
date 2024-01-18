### protoc 3 buf
1. brew install buf
2. buf.work.yaml
```yaml
# 一般放下根目录下面 代表一个工作区， 通常一个项目也就一个该配置文件
version: v1
directories:
  - '.'
```
3. buf.gen.yaml
```yaml
# 一般放在buf.work.yaml的同级目录下面, 主要定义一些protoc生成的规则和插件配置
version: v1
managed:
  enabled: true
plugins:
  # generate go struct code
  - name: go
    out: api/
    opt: paths=source_relative
  # generate grpc service code
  - name: go-grpc
    out: gen/proto/go
    opt: paths=source_relative
  - name: validate
    out: api
    opt:
      - paths=source_relative
      - lang=go
```
4. buf mod init
5. buf generate(it will generate all corresponding proto pb files)