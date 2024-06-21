from typing import List, Optional
import math
class TreeNode:
    def __init__(self,val: int=0,children: Optional[List['TreeNode']]=None):
        self.val=val
        self.children = children if children is not None else []
    def traverse(self,root: 'TreeNode')->None:
        for child in root.children:
            self.traverse(child)

# 二叉树 求深度
depth = 0
res=0
def traverse(root: TreeNode, k: int) -> None:
    global depth,res
    if root == None:
        return math.max(res,depth)
    
    depth+=1
    traverse(root.left)
    traverse(root.right)
    depth-=1

# 回溯 全排列
res=[]
track=[]
def backtrack(nums: Optional[List[int]]=None):
    if len(track) == len(nums):
        res.append(track)
        return
    for i in range(len(nums)):
        if nums[i] in track:
            continue
        track.add(nums[i])
        backtrack(nums)
        track.pop()

def max_depth(root: TreeNode)->int:
    if root ==None:
        return 0
    left_max=max_depth(root.left)
    right_max=max_depth(root.right)
    res = math.max(left_max,right_max)+1
    return res

def coin_change(coins: Optional[List[int]],amount:int):
    if amount==0:
        return 0
    if amount<0:
        return -1
    res = float('inf')
    for coin in coins:
        sub_problem=coin_change(coins,amount-coin)
        if sub_problem==-1:
            continue
        res=math.min(res,sub_problem+1)
    return -1 if float('inf')==res else res

if __name__ == "__main__":
    node1=TreeNode(1,[1,2])
    print(node1)