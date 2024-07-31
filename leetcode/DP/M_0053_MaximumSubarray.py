class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n=len(nums)
        dp=(n)*[-10001]
        # 以 nums[i] 为结尾的子数组 最大和
        dp[0]=nums[0]
        for i in range(1,n):
            # 以 nums[i-1]为结尾的最大子数组和 dp[i-1]如果小于 0 就可以直接忽略
            # 加一个负数只会更小
            dp[i]=dp[i-1]+nums[i] if dp[i-1]>0 else nums[i]
        return max(dp)