from collections import deque
class Solution:
    def pizzaDisplay(self, pizzaOrdered: List[int], size: int) -> List[int]:
        
        n = len(pizzaOrdered)
        # store index of minus number
        curMinus = deque()
        res = []
        # initialize first window
        for i in range(size):
            if pizzaOrdered[i] < 0:
                curMinus.append(i)
        # if first window has minus value, append to result
        if curMinus:
            res.append(pizzaOrdered[curMinus[0]])
        # start to move from index as size
        for i in range(size, n):
            if pizzaOrdered[i] < 0:
                curMinus.append(i)
            if not curMinus:
                res.append(0)
            else:
                head = curMinus[0]
                if head <= i and head >= i - size + 1:
                    res.append(pizzaOrdered[head])
                else:
                    res.append(0)
                    curMinus.popleft()
        # 到头之后剩下 window 残留的数据的执行
        for i in range(size):
            if curMinus:
                head=curMinus.popleft()
                res.append(pizzaOrdered[head])
            else:
                res.append(0)

        return res
                        



class Solution:
    def pizzaDisplay(self, pizzaOrdered: List[int], size: int) -> List[int]:
        n = len(pizzaOrdered)
        left = 0
        right = 0

        res = []

        windowD = deque()

        while right < n:
            c = pizzaOrdered[right]
            if c < 0:
                windowD.append(right)

            right += 1
            
            print(windowD)
            while right - left > size-1:
                if windowD:
                    d = windowD[0]
                    if d < left or d > right:
                        res.append(0)
                        windowD.popleft()
                    else:
                        res.append(pizzaOrdered[d])
                else:
                    res.append(0)
                left += 1
        return res

                
                

            



        