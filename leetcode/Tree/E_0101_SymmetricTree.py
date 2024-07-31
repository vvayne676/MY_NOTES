# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def helper(L, R):
            if L is None and R is None:
                return True
            if L is None or R is None or L.val!=R.val:
                return False

            
            left = helper(L.left,R.right)
            right = helper(L.right,R.left)
            return left and right        
        return helper(root.left,root.right)

        

# L.left and Right.right
# L.right and R.left