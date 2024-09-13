# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        stack=deque()
        res=[]
        if not root :
            return res
        stack.append(root)
        layer=0
        while stack:
            size = len(stack)
            res.append(layer)
            for i in range(size):
                
                node=stack.popleft()
                
                res[layer]=node.val
                if node.left:
                    stack.append(node.left)
                if node.right:
                    stack.append(node.right)
                    
            layer+=1
            