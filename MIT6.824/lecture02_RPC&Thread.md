Threads
1. I/O Concurrency
2. multi-core Parallelism
3. Convenience (run some background periodic tasks)

OR

Event-driven programming 

Sort of equivalent yet cannot take advantage of multi-core


Thread challenge
1. Race(generally solved with locks-even in multi-core, MESI can use transaction-bus to solve the race issue. transaction-bus will determine who is the first task and acquire the lock depends on who comes first or who has higher priority.)
2. Coordination
    * channels
    * sync.Cond
    * waitGroup
3. Deadlock

```go
// shared data
type fetchState struct{
    mu sync.Mutex
    fetched map[string]bool
}
func ConcurrentMutex(url string, fetcher Fetcher, f *fetchState){
    f.mu.Lock()
    already:=f.fetched[url]
    f.fetched[url]=true
    f.mu.Unlock()

    if already{
        return
    }

    urls, err:=fetcher.Fetch(url)
    if err!=nil{
        return
    }
    var done sync.WaitGroup
    for _,u := range urls{
        done.Add(1)
        go func(u string){
            defer done.Done()
            ConcurrentMutex(u, fetcher, f)
        }(u)
    }
    done.Wait()
    return
}

// channel
func worker(url string, ch chan []string, fetcher Fetcher){
    urls, err:=fetcher.Fetch(url)
    if err != nil{
        ch <- []string{}
    } else{
        ch <- urls
    }
}

func master(ch chan []string, fetcher Fetcher){
    n := 1
    fetched := make(map[string]bool)
    for urls := range ch {
        for _,u := range urls{
            if fetched[u]==false{
                fetched[u]=true
                n += 1
                go worker(u, ch, fetcher)
            }
        }
        n -= 1
        if n==0{
            break
        }
    }
}

func ConcurrentChannel(url string, fetcher Fetcher){
    ch := make(chan []string)
    go func(){
        ch <- []string{url}
    }()
    master(ch, fetcher)
}
```


transaction-bus 
1. 事务总线的工作机制:
    * 事务总线是一种基于总线的通信机制,用于在多个 CPU 核心之间传递信息和请求。
    * 当一个核心尝试访问某个共享资源时,它会向总线发起一个事务请求。
2. 串行化处理:
    * 事务总线会以串行的方式处理这些事务请求,确保同一时刻只有一个请求被执行。
    * 这种串行化机制可以避免出现典型的竞争条件(Race Condition)。
3. 冲突检测的关键:
    * 您提出的关键问题在于,事务总线能否在同一时刻检测到多个任务(如核心或 goroutine)试图访问同一共享资源的情况。
    * 如果事务总线无法及时检测到这种并发访问的情况,那么它就无法有效地解决竞争条件。
4. 事务总线的冲突检测机制:
    * 事务总线确实具有及时检测并发访问的能力。它会监听总线上的所有事务请求,并能够识别出同时发起的多个请求。
    * 当事务总线检测到同一时刻有多个请求试图访问同一共享资源时,就会触发一个冲突检测机制。
5. 冲突解决过程:
    * 一旦检测到冲突,事务总线会对这些并发的事务请求进行仲裁和排序,确保它们以串行的方式被执行。
    * 通常情况下,事务总线会采用先到先服务的策略,按照请求的先后顺序来处理这些事务。


要实现并行检测，冲突检测电路需要使用一些特定的硬件组件和设计原理。以下是一个简化的设计方案和实现原理   \
设计方案：
1. 多路复用器（Multiplexer, MUX）：
    * 用于选择多个输入信号中的一个，并将其传递到单个输出。在冲突检测中，可以使用多路复用器来选择不同处理器核心发出的地址信号。
2. 比较器（Comparator）：
    * 用于比较两个信号是否相等。在冲突检测电路中，比较器用于比较来自不同处理器核心的地址信号。
3. 逻辑门（Logic Gates）：
    * 如AND、OR和NOT门，用于实现简单的逻辑函数。这些可以用来组合和处理比较器的输出，以及控制信号。
4. 锁存器（Latch）或触发器（Flip-Flop）：
    * 用于存储信号状态。这些可以用来保存地址和控制信号，以便在同一时钟周期内进行比较。
实现原理：\

1. 地址信号的并行输入：
    * 每个处理器核心的地址信号都连接到一个中央的比较网络。这个网络由多个比较器组成，每个比较器都能同时接收两个地址信号。
2. 比较器网络：

    * 每个比较器并行地比较两个地址信号。如果两个地址相同，比较器输出一个高电平信号（表示冲突）。
3. 控制信号的逻辑处理：

    * 控制信号（指示读或写操作）通过逻辑门与比较器的输出相结合。例如，如果有一个写操作和一个冲突，AND门将输出一个高电平信号。
4. 冲突检测输出：

    * 所有比较器的输出通过OR门汇总。如果任何比较器检测到冲突，OR门的输出将是高电平，表示总体上存在冲突。
5. 同步和锁存：
    * 为了确保所有信号都在同一时钟周期内被比较，地址和控制信号在进入比较网络之前被锁存或触发。这样可以保证比较是基于同步的信号进行的。
6. 仲裁和控制信号生成：
    * 如果检测到冲突，冲突检测电路将生成一个控制信号，用于触发仲裁机制或直接控制处理器核心的访问请求。

通过这种设计，冲突检测电路能够在硬件级别上并行地监控和处理多个信号，从而实现高效的冲突检测。这种并行处理是通过使用多个比较器和逻辑门来实现的，它们可以在没有时间延迟的情况下同时处理多个信号。这种设计的关键在于高速的硬件组件和精确的时钟同步，以确保所有信号都能够在正确的时间被比较和处理。