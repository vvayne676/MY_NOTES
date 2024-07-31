'''
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。
'''
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n=len(nums)
        if not nums or n<3:
            return []
        nums.sort()
        res=[]

        for i in range(n):
            if nums[i]>0:
                return res
            if i>0 and nums[i]==nums[i-1]:
                continue
            left=i+1
            right=n-1
            while left<right:
                L=nums[left]
                R=nums[right]
                t=nums[i]
                if L+R+t==0:
                    res.append([nums[i],nums[left],nums[right]])
                    left+=1
                    right-=1
                    while (left<right and nums[left]==nums[left-1]):
                        left+=1
                    while (left<right and nums[right]==nums[right+1]):
                        right-=1
                elif L+R+t>0:
                    right-=1
                elif L+R+t<0:
                    left+=1
        return res