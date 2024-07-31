class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:

        result = [-1]*len(nums)
        stack = []
        for i in range(len(nums)*2):
            idx = i%len(nums)
            while stack and nums[stack[-1]] < nums[idx]:
               result[stack.pop()] = nums[idx]    
            stack.append(idx)
        return result

class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n=len(nums)
        stack=[]
        res=[-1]*n
        
        for i in range(2*n-1,-1,-1):
            while stack and stack[-1]<=nums[i%n]: 
                stack.pop()
            if stack:
                res[i%n] = stack[-1]
            stack.append(nums[i%n])

        return res
