### protoc 3 buf
1. brew install buf
2. buf.work.yaml (可以不用)
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
    out: '.'
    # opt: paths=source_relative
  # generate grpc service code
  - name: go-grpc
    out: '.'
    opt: paths=source_relative
  - name: validate
    out: '.'
    opt:
      # - paths=source_relative
      - lang=go
```
4. buf.yaml
```yaml
version: v1
deps:
  - buf.build/googleapis/googleapis
  - buf.build/bufbuild/protovalidate
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT

```
5. buf mod update
6. proto
```proto
syntax = "proto3";
package server;
option go_package = "api/server;server";
import "buf/validate/validate.proto";
// Payin transaction service
// ************************ Payin transaction service ***********************

message TxStatusQueryRequest {
  string merchant_id = 1;
  string trade_no = 2;
}
```
7. buf generate(it will generate all corresponding proto pb files)