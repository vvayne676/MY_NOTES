class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        
        n=len(nums)
        ileft=[1]*n
        iright=[1]*n
        ans=[1]*n

        for i in range(1,n):
            ileft[i] = ileft[i-1]*nums[i-1]
        
        for j in range(n-2,-1,-1):
            iright[j] = iright[j+1]*nums[j+1]
        
        for k in range(n):
            ans[k]=ileft[k]*iright[k]
        return ans