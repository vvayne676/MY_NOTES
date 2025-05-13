# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def helper(root,depth):
            nonlocal maxDepth
            if root is None:
                maxDepth=max(maxDepth,depth)
                return
            helper(root.left,depth+1)
            helper(root.right,depth+1)
        
        maxDepth=0
        helper(root,0)
        return maxDepth
    
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def process(root):
            if root==None:
                return 0
            leftD=process(root.left)
            rightD=process(root.right)
            return max(leftD,rightD)+1
        return process(root)