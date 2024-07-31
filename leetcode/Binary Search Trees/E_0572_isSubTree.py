# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:

        def check(cur, t):
            if not cur and not t: return True
            if not cur or not t: return False
            if cur.val != t.val: return False
            return check(cur.left, t.left) and check(cur.right, t.right)

        def dfs(s, t):
            if not s:
                return False
            return check(s, t) or dfs(s.left, t) or dfs(s.right, t)

        return dfs(s, t)



# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def equvalient(root,subRoot):
            if root is None and subRoot is None:
                return True
            if root is None or subRoot is None or root.val!=subRoot.val:
                return False

            left=equvalient(root.left,subRoot.left)
            right=equvalient(root.right,subRoot.right)

            return left and right
            
        def helper(root,subRoot):
            if not root and not subRoot:
                return True
            if not root or not subRoot:
                return False
            e=equvalient(root,subRoot)
            if e: return True
            else:
                left=helper(root.left,subRoot)
                right=helper(root.right,subRoot)
                return left or right
        return helper(root,subRoot)