## Project Code Structure
项目目录结构参考: https://github.com/golang-standards/project-layout/blob/master/README_zh.md

程序整体分两块:
1. 请求进来之前
    *  router 注册路径 并分配处理函数(处理函数由controller实现)
    *  controller结构体包含3个field 分别为 payin/payout/credit_card services. 每个services为一个 map, key是provider id or bank channel, value为对应service的对象. 每个service对象是一个接口定义了需要实现的方法. 在new controller的时候, 注册所有渠道到对应的map中. 
    *   注册的渠道对象通过new service实现, new service的时候也会new一个相应的client, client包含所有该渠道需要的一系列配置和参数.
    *   至此注册完成
2. 请求进来之后
    *   找到对应处理函数 函数中会根据provider id或者bank channel获取对应的服务, 因为该服务已实现了接口定义的所有方法, 所以可以放心调用相应方法. 
    *   相应方法均表示为一个business logic, 如果实现这个业务逻辑需要多个步骤, 则具体步骤写入 相应client并实现. 然后组装成 类似 client.step1 client.step2 client.step3 然后做出相应处理并返回
## Docker operation
```
docker build --platform linux/amd64 -t cc:amd .
docker build --platform linux/arm64 -t cc:arm .
// cc.tar is target name
// cc:latest is source name
docker save -o cc.tar cc:latest                                    
docker load -i cc.tar
```

## ENV
```
ENV=dev
PAYOUT_APP_ID=xxx
PAYOUT_APP_KEY=xxxx
LUCKY_KEY=1234567890123456
RDS_HOST=localhost
RDS_PASSWORD=xxxxxx
RDS_USERNAME=bankapi
REDIS_HOST=127.0.0.1

```

## Add a new Channel
1. Go to internal/common/in (or out ) to add your channel name
2. Go to internal/controller/transaction, follow the existing pattern to register your channel to corresponding service (you will see a lot of warnings from your IDE, just ignore them for now)
3. Go to internal/channels, create a new folder XXX, then 2 sub-folders: client and service. Service is responsible for processing business logic. Client is responsible for interacting with Channels' endpoints.
4. Under the service folder, usually you will have 3 files: 
    * payin: responsible for payin business logic
    * payout: responsible for payout business logic
    * service: responsible for some common definition and service initialization. You can implement NewPayinService and NewPayoutService here
5. Under the client folder, usually you will have 4 files:
    * payin: interact with channel endpoints about payin service
    * payout: interact with channel endpoints about payout service
    * channelname.go: this file will include some client level definitions and payin/payout client initialization (Attention: payin/payout client is a Singleton instance that stores all related config info like key, secret, api url etc. )
    * channlename.pb.go: protobuff generated file. it defines all the structs that you need when interact with channels' endpoints




## Key Points
查询时候 成功失败一定要映射specific status code, 不确定的 status code 可以找渠道确认, 非确定的可以PROCESSING 避免出错. Payin 尽量让PAID的范围足够小 Payout尽量让REJECTED的范围足够小 比如下面
```
if statusCode==0
{
    return "REJECTED"
}else if statusCode==1
{
    return "PAID"
}else if ...{
    ...
}else 
{
    return "PROCESSING"
}
```

PIX

一般都是两步 第一步查 pix key 第二步确认打款 不论名字怎么叫 其本质不变

第二步即便收到成功的返回 也只是说打款的请求成功收到了 最终transaction 状态要看回调或者查询的结果






pix
original_error - ref: fastcash

non-pix 
ref: paypal


### For loop do goroutine htp/grpc call example
```golang
 
// out trade no case
		// merchantIds := req.GetMerchantIds()
		// results := make(chan *ts_data.Payout, len(merchantIds))

		// var wg sync.WaitGroup

		// for _, merchantStringId := range merchantIds {

		// 	wg.Add(1)

		// 	go func(merchantId string) {

		// 		defer gr.RecoverPanic(ctx)
		// 		defer wg.Done()

		// 		merchantInt := service.MerchantId2Int(ctx, merchantId)

		// 		r, err = grpc.PayoutListAdb.FindPayoutListByReferenceId(ctx, &ts_data.CustomCode{
		// 			ReferenceId: req.GetOutTradeNo(),
		// 			MerchantId:  merchantInt})
		// 		if err != nil {
		// 			logs.CtxErrorf(ctx, "[TransactionQuery.PayoutListAdb.FindPayoutListByReferenceId] error: %v", err)
		// 			r = &ts_data.Payout{}
		// 		}

		// 		results <- r // Send result to channel
		// 	}(merchantStringId)
		// }

		// go func() {
		// 	wg.Wait()
		// 	close(results)
		// }()

		// // Process results from the channel
		// for result := range results {
		// 	if result.GetTransactionId() != "" {
		// 		res.TradeStatus = service.GetTradeStatus(ctx, r.GetTransactionStatus())
		// 		res.PaymentMethod = service.GetPaymentMethod(ctx, r.GetThirdpartyId())
		// 		res.RefusedReason = r.GetRemark()
		// 		res.TradeNo = r.GetTransactionId()
		// 		return res, nil
		// 	}
		// }
		// res.ErrMsg = fmt.Sprintf("Transaction %v does not exist", req.TradeNo)
		// return res, nil
```

### buf proto to swagger json
buf.yaml
```yml
version: v1
build:
  excludes:
    - ./vendor
deps:
  - buf.build/googleapis/googleapis
  - buf.build/bufbuild/protovalidate
  - buf.build/grpc-ecosystem/protoc-gen-swagger
  - buf.build/grpc-ecosystem/grpc-gateway
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
```
buf.gen.yaml
```yml
# 一般放在buf.work.yaml的同级目录下面, 主要定义一些protoc生成的规则和插件配置
version: v1
managed:
  enabled: true
plugins:
  # generate go struct code
  - name: go
    out: "."
    # opt: paths=source_relative
  # generate grpc service code
  - name: go-grpc
    out: "."
    # opt: paths=source_relative
  - name: validate
    out: "."
    opt:
      # - paths=source_relative
      - lang=go
  - plugin: buf.build/grpc-ecosystem/openapiv2
    out: "swagger-ui"
    opt:
      - json_names_for_fields=false # ref: https://github.com/grpc-ecosystem/grpc-gateway/issues/3394 https://github.com/grpc-ecosystem/grpc-gateway/blob/main/protoc-gen-openapiv2/main.go

```

```proto
syntax = "proto3";
package aml;
option go_package = "api/server/aml;aml";
import "buf/validate/validate.proto";
import "protoc-gen-openapiv2/options/annotations.proto";
import "google/api/annotations.proto";

// ************************  AML service ***********************

service Merchant {
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_tag) = {
    name: "AML Service Support"
    description: "AMLService description -- provide support for AML service!"

  };

  // Get all merchants
  //
  // This API get all merchants
  rpc GetMerchants(GetMerchantsRequest) returns (GetMerchantsReply) {
    option (google.api.http) = {
      post: "/api/aml/v1/merchants"
    };
  }

  // Get apps under merchant
  //
  // This API get apps under the selected merchant
  rpc GetMerchantApps(GetMerchantAppsRequest) returns (GetMerchantAppsReply) {
    option (google.api.http) = {
      post: "/api/aml/v1/merchant/apps"
    };
  }
}

// https://buf.build/bufbuild/protovalidate/docs/main:buf.validate#buf.validate.Int64Rules
message GetMerchantsRequest {
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_schema) = {
    json_schema: {
      title: "GetMerchantsMessage"
      description: "GetMerchantsMessage"
      required: [ "page_num", "page_size", "time" ]
    }
  };
  int64 page_num = 1 [(buf.validate.field).int64.gt = 0];
  int64 page_size = 2 [
    (buf.validate.field).int64.lte = 1000,
    (buf.validate.field).int64.gt = 0,

  ];
  int64 time = 3 [(buf.validate.field).int64.gt = 0];
}
message GetMerchantsReply {
  message Merchant {
    string merchant_no = 1;  // 32bit string
    string merchant_name = 2;
  }
  repeated Merchant merchant_list = 1;
  string err_msg = 99;
}

message GetMerchantAppsRequest {
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_schema) = {
    json_schema: {
      title: "GetMerchantAppsMessage"
      description: "GetMerchantAppsMessage"
      required: [ "page_num", "page_size", "merchant_no", "time" ]
    }
  };
  int64 page_num = 1 [(buf.validate.field).int64.gt = 0];
  int64 page_size = 2 [
    (buf.validate.field).int64.lte = 1000,
    (buf.validate.field).int64.gt = 0
  ];
  string merchant_no = 3;
  int64 time = 4 [(buf.validate.field).int64.gt = 0];
}
message GetMerchantAppsReply {
  message App {
    string app_no = 1;
    string app_name = 2;
  }
  repeated App app_list = 1;
  string err_msg = 99;
}


```