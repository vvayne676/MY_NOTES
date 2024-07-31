'''
1. 倒序找到第一个降序的元素
2. 再倒序找到第一个大于降序元素的元素
3. 交换然后对第一个降序元素后面的升序排列
'''
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n=len(nums)
        i=n-2
        j=n-1
        k=n-1
        while i>=0 and nums[i]>=nums[j]:
            i-=1
            j-=1
        # tail up
        if j==n-1:
            nums[i],nums[j]=nums[j],nums[i]
            return nums
        if i==-1:
            return nums.reverse()
        while k>j and nums[k]<=nums[i]:
            k-=1
        nums[i],nums[k]=nums[k],nums[i]
        nums[j:]=reversed(nums[j:])
        return nums
    
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        i = len(nums) -1
        while i > 0 and nums[i-1] >= nums[i]:
            i-=1
        if i!=0:
            j=len(nums)-1
            while nums[j]<=nums[i-1]:
                j-=1
            nums[i-1],nums[j]=nums[j],nums[i-1]
        nums[i:]=sorted(nums[i:])