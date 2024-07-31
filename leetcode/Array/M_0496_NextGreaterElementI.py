class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        n=len(nums2)
        # index is the value of nums2
        d={i:-1 for i in nums2}
        stack=[]
        res=[]
        for i in range(n-1,-1,-1):
            # if cur nums2 greater than top of stack, pop
            while stack and stack[-1] <= nums2[i]:
                stack.pop()
            # top of stack greater than nums2[i]
            # if stack 0 which means no value greater than cur nums2
            # so d[nums2[i]] = -1, otherwise value is stack[-1]
            d[nums2[i]]= stack[-1] if stack else -1
            # push cur nums2[i] into stack
            stack.append(nums2[i])

        for i in nums1:
            res.append(d[i])
        return res