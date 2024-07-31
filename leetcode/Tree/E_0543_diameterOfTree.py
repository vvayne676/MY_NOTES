# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def helper(root)-> int:
            nonlocal res
            if root is None:
                return 0
            left = helper(root.left)
            right = helper(root.right)
            res=max(res,left+right)
            return max(left,right)+1
        
        res = 0
        helper(root)  
        return res      
