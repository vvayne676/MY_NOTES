class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
       
        def quick_sort(nums,low,high):
            if low < high:
                p=partition(nums,low,high)
                quick_sort(nums,low,p-1)
                quick_sort(nums,p+1,high)

        def partition(nums,low,high):
            pivot=nums[low]
            
            left,right=low+1,high
            while left <= right:
                while left <= right and nums[left] <= pivot:
                    left += 1
                while left <= right and nums[right] > pivot:
                    right -= 1
                if left < right:
                    nums[left], nums[right] = nums[right], nums[left]
            nums[low], nums[right] = nums[right], nums[low]

            return right
        quick_sort(nums,0,len(nums)-1)
        return nums
