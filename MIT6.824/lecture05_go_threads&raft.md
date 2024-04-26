
## Lock
```go
func CondLock() {

	count := 0
	finished := 0

	var mu sync.Mutex
	cond := sync.NewCond(&mu) // 创建了一个 sync.Cond 类型的变量 cond，它与 mu 互斥锁相关联。cond 用于在条件满足时通知等待的协程

	for i := 0; i < 10; i++ {
		go func() {
			vote := requestVote()
			mu.Lock()
			defer mu.Unlock()
			if vote {
				count++
			}
			finished++
			cond.Broadcast() // cond.Broadcast() 通知所有等待 cond 条件的协程
		}()
	}
	mu.Lock() // 在主协程中,我们首先获取 mu 锁。
	// 进入一个循环,检查 count 是否小于 5 且 finished 是否不等于 10。如果这两个条件都满足,我们就调用 cond.Wait() 方法,这将会释放 mu 锁并让当前协程进入等待状态。
	for count < 5 && finished != 10 {
		// 当其他协程调用 cond.Broadcast() 时,正在等待的协程将会被唤醒,并重新获取 mu 锁,然后继续执行循环体
		cond.Wait()
	}
	if count >= 5 {
		fmt.Println("received 5+ votes!")
	} else {
		fmt.Println("lost")
	}
	mu.Unlock()
}
```
如果有多个cond.Wait(). cond.Broadcast() 唤醒所有cond.Wait() cond.Signal() 只会唤醒一个 cond.Wait()
```go
var (
    mu    sync.Mutex
    cond1 = sync.NewCond(&mu)
    cond2 = sync.NewCond(&mu)
)

go func(){
    for {
        cond1.L.Lock()
        count++
        if count==5{
            cond1.Broadcast()
            cond2.Broadcast()
        }
        cond1.L.Unlock()
        time.Sleep(100 * time.Millisecond)
    }
}()

// 消费者协程 1
go func() {
    for {
        cond1.L.Lock()
        for count < 5 {
            cond1.Wait()
        }
        // 处理 cond1 唤醒
        fmt.Println("Cond1 was signaled")
        cond1.L.Unlock()
    }
}()

// 消费者协程 2
go func() {
    for {
        cond2.L.Lock()
        for count >= 5 {
            cond2.Wait()
        }
        // 处理 cond2 唤醒
        fmt.Println("Cond2 was signaled")
        cond2.L.Unlock()
    }
}()

// 等待协程结束
time.Sleep(time.Second)



Or

// select 用于在当前协程中等待和选择可以执行的通信操作
select {
case <-cond1.Wait():
    // 处理 cond1 唤醒
case <-cond2.Wait():
    // 处理 cond2 唤醒
}

```

```go
cond lock pattern:
mu.Lock()
// do something that might affect the condition
cond.Broadcast()
mu.Unlock()

----------

mu.Lock()
while condition == false{
    cond.Wait()
}
// now condition is true, and we have the lock
mu.Unlock()
```


## Channel
```go
func main(){
    c:=make(chan bool)
    go func(){
        time.Sleep(1*time.Second)
        <-c
    }()
    start:=time.Now()
    c <- true // blocks until other goroutine receives
    fmt.Println("send took %v\n", time.Since(start))
}
```

simplest deadlock
```go
func main(){
    c:=make(chan bool)
    c <- true
    <- c
}
```

simulate wait group
```go
func main(){
    done:=make(chan bool)
    for i:=0;i<5;i++{
        go func(x int){
            sendRPC(x)
            done<-true
        }(i)
    }
    for i :=0; i<5;i++{
        <-done
    }
}
func sendRPC(i int){
    print(i)
}
```