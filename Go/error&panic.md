error and panic are both available to be handled by developers. fatal error is beyond us.

Fatal Error:
1. concurrent r/w map
2. stack overflow (unlimit recursive)
3. go of nil func value ([var f func()] [go f()])
4. all goroutines are asleep - deadlock!( func foo(){ select {} })
5. fatal error: thread exhaustion (如果你的 goroutines 被 IO 操作阻塞了，新的线程可能会被启动来执行你的其他 goroutines。Go 的最大的线程数是有默认限制的，如果达到了这个限制，你的应用程序就会崩溃。)
6. runtime: out of memory (如果你执行的操作，例如：下载大文件等。导致应用程序占用内存过大，程序上涨，导致 OOM)