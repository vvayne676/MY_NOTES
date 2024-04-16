1. rune: unicode code point
2. check if map has key:
```go
var mapp map[int]string
if _, ok := mapp[10]; ok{

}else{

}
```
3. default para and optional para are not supported in golang but can use ellipsis (...)
```go 
// 这个函数可以传入任意数量的 []int 
// []int is slice [1]int is array
func mergeSlices(slices ...[]int) []int {}
```
4. defer 执行顺序: 倒序
5. 指明返回值和不指明
```go
// 返回i为0
func test() int {
	i := 0
	defer func() {
		i += 1
		fmt.Println("defer")
	}()
	return i
}
// 返回i为1
func testi() (i int) {
	i = 0
	defer func() {
		i += 1
		fmt.Println("defer2")
	}()
	return i
}
```
test()不是有名返回, return执行后Go会创建一个临时变量保存返回值, 直到所有defer运行完然后返回. 如果是有名返回 testi() 执行return时并不会再创建临时变量保存,  因此 defer 修改了 i 就会对 返回值产生影响. 从函数体就能看出 test() i:=0, 而testi() i=0
6. Go语言的tag用处: json 序列化和db 映射字段名字, 总的来说就是结构体到目标样式字段的映射关系
7. 






设计一个支付系统

假设每天日活 1m 一天平均消费5次 保存近5年的消费记录

分流？load balance？ rate limiter?
DB 和 cache scaling？数据一致性
CDN？
stateful or stateless
服务拆分？降低耦合？
Logging? Metrics? Automation?

Optimization: 
multi data center for latency
Monitoring (like rate limiting, check if the rule works well)


Write path
Read path


Golang基础 

1. For loop on “hello你好“
2. Channel会panic吗 可以recover吗？ 关一个 已经关闭的 关一个nil 和 往关闭的 发数据
3. Channel主要使用场景？同步协程 限制并发 数据传递
4. 了解程度怎么样 如果说熟悉 就问底层 实现 hcha结构体+调度器
5. context使用场景 context终止的底层是什么？channel
6. protobuf package 冲突



package utils

import (
    "context"
    "errors"
    "runtime"
    "sync"

    "gitlab.pagsmile.com/gopkg/logs"
)

var (
    PanicError = errors.New("Panic")
)

func PanicRecoverDecorator(f func() error, caller, callee string, ctx context.Context) (err1 error) {
    defer func() {
        if err := recover(); err != nil {
            LogEndReportPanic(ctx, err, caller, callee)
            err1 = PanicError
        }
    }()
    return f()
}

func LogEndReportPanic(ctx context.Context, err interface{}, caller string, callee string) {
    buf := make([]byte, 1<<16)
    stackSize := runtime.Stack(buf, false)
    logs.CtxErrorf(ctx, "", "action=RecoverPanic||panic error||err=%v||caller=%v||callee=%v||msg=%v",
        err, caller, callee, string(buf[0:stackSize]))
    // add metrics
}

func test(ctx context.Context) {
    waitGroup := sync.WaitGroup{}
    waitGroup.Add(2)
    go func() {
        defer waitGroup.Done()
        err := PanicRecoverDecorator(func() (err error) {
            // 额外信息
            // your logic code
            // result，DataErr = logic
            return
        }, "caller", "caller", ctx)
        if err != nil {
        }
        // some  logs
    }()

    go func() {
        defer waitGroup.Done()
        err := PanicRecoverDecorator(func() (err error) {
            // your logic code
            return
        }, "caller", "callee", ctx)

        if err != nil {
         
        }
        // some  logs
    }()
    waitGroup.Wait()
}


从并发 -> goroutine -> 到锁 -> 到MQ -> 到单核 -> 到多核 -> 到MESI和transaction-bus

