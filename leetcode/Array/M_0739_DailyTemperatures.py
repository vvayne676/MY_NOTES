class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        stack=[]
        res=[0]*n

        for i in range(n-1,-1,-1):
            while stack and stack[-1][1]<=temperatures[i]:
                stack.pop()
            if stack:
                res[i]=stack[-1][0]-i
            stack.append([i,temperatures[i]])
        return res