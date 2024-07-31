'''
中序遍历BST 得到数组 然后 取 k 
'''

class BST:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def findKthLargestValueInBst(tree, k):
    traversal = []
    def inorderTraverse(tree):
        if tree is None:
            return
        inorderTraverse(tree.left)
        traversal.append(tree.value)
        inorderTraverse(tree.right)
    inorderTraverse(tree)
    return traversal[-k] if len(traversal)>=k else -1