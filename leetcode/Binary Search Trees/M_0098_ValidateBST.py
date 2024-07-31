# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validateTree(tree, minVal, maxVal):
            if tree is None:
                return True
            if tree.val <= minVal or tree.val >= maxVal:
                return False
            left = validateTree(tree.left, minVal, tree.val)
            right = validateTree(tree.right, tree.val, maxVal)
            return left and right
        return validateTree(root, float('-inf'), float('inf'))