class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        pre=0
        maxx=nums[0]
        for v in nums:
            pre=max(v,pre+v)
            maxx=max(pre,maxx)
        return maxx

    def maxSubArrayT(self, nums: List[int]) -> int:
        # 以 i 为结尾的子数组的最大和
        dp=[0]*len(nums)
        dp[0]=nums[0]
        maxx=nums[0]
        for i in range(1,len(nums)):
            dp[i]=dp[i-1]+nums[i] if dp[i-1]>0 else nums[i]
            maxx=max(maxx,dp[i])
        return maxx