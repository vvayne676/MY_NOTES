def slidingWindow(s: str):
    left=0
    right=0

    n=len(s)

    window=deque()

    while right < n:
        # 更新窗口内数据
        # 当前字符 or whatever 入窗口
        c = s[right]
        window.append(c)

        
        
        # 增大窗口: 实质上没做任何操作只是单纯的为了下面的窗口缩小提供前置条件
        right+=1
        # 此时window内的数据还是 right 而不是 right+1
        # 触发窗口缩小条件 比如 window size大于 给定的值 
        # 比如窗口大小4 则条件为 right - left > size -1
        while left<right and (widnow needs shrink):

            # 更新窗口内数据
            # 一些操作
            # d=s[left]
            # window[d]-=1
            # 或者下面的popleft
            window.popleft()
            
            left+=1
