## 1.1
### 1.1.1 数据结构的存储方式
数据存储方式只有两种：数组（顺序存储）和链表（链式存储）
1. 队列和栈 可以用 array 和 linked list实现
2. 图 邻接表就是链表 邻接矩阵就是二维矩阵
3. 树 数组实现就是堆  链表就是正常普通的树
4. map 拉链 数组配链表 开放寻址 数组

实际应用中 Redis 的各种数据结构底层都是用了两种实现方式

### 1.1.2 数据结构的基本操作
基本操作 遍历+访问 具体就是 CURD

遍历：
1. for/while 迭代
2. 递归

```python
from typing import List, Optional
class TreeNode:
    # Optional类型提示用于表示一个变量可以是某种类型或None
    def __init__(self,val: int=0,children: Optional[List['TreeNode']]=None):
        self.val=val
        self.children = children if children is not None else []
    def traverse(self,root: 'TreeNode')->None:
        for child in root.children:
            self.traverse(child)
```
### 1.1.3 刷题指南
数组/链表->二叉树->二叉树->二叉树->回溯->递归
## 1.2
### 1.2.1 算法本质
<b><i>"穷举"</i></b>
刷题一般都是2种情况
1. 如何穷举 - 一般是递归类问题, 典型就是动态规划系列
2. 如何聪明的穷举 - 非递归类穷举, 大佬发明, 会就是会, 没学过基本就是不会

### 1.2.2 数组/单链表
双指针(一快一慢 中间两边 两边中间) 排序 前缀和 差分 
### 1.2.3 二叉树系列
1. 回溯套路(回溯本质就是多叉树遍历) 遍历二叉树
2. 动态规划套路 分解问题
#### 1.2.3.1 遍历 回溯套路
```python
# 二叉树遍历套路 取最深度
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

# 回溯套路 求全排列(全排列来回颠倒数字位置)
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
```
#### 1.2.3.2 分解问题 动态规划套路
```python
# 分解问题求最大深度
def max_depth(root: TreeNode)->int:
    if root ==None:
        return 0
    left_max=max_depth(root.left)
    right_max=max_depth(root.right)
    res = math.max(left_max,right_max)+1
    return res

# 动态规划凑零钱
# 输入金额 amount 返回凑出 amount 的最少硬币个数
def coin_change(coins: Optional[List[int]],amount:int):
    # base case
    if amount==0:
        return 0
    if amount<0:
        return -1
    
    res = float('inf')
    
    for coin in coins:
        # 递归计算凑出 amount - coin 的最少硬币个数
        sub_problem=coin_change(coins,amount-coin)
        if sub_problem==-1:
            continue
        # 凑出 amount 的最少硬币个数
        res=math.min(res,sub_problem+1)

    return -1 if float('inf')==res else res
```

## 1.3 动态规划解题套路框架
动态规划问题的一般形式是 求最值. 求最值的核心问题就是 穷举. 

正确的 "状态转移方程" 才能正确穷举. 判断算法是否有 "最优子结构", 可以通过自问题的最值的到原问题的最值. DP还有重叠子问题的存在. Memo 或者 DP table 优化 穷举过程

明确 base case -> 明确 "状态" -> 明确 "选择" -> 定义 dp 数组/函数的含义

框架如下:
```python
# 自顶向下递归的动态规划
def dp(状态1,状态2, ...):
    for 选择 in 所有可能的选择:
        # 此时的状态已经因为做了选择而改变
        result = 求最值(result, dp(状态1, 状态2, ...))
    return result

# 自底向上迭代的动态规划
# 初始化 base case
dp[0][0][...] = base case
# 进行状态转移
for 状态1 in 状态1的所有取值:
    for 状态2 in 状态2的所有取值:
        for ...
            dp[状态1][状态2][...]=求最值(选择1, 选择2, ...)
```
## 1.3.1 斐波那契
但凡遇到递归问题 最好都要画出递归树
1. 暴力递归
```python
def fib(N: int):
    if N==1 or N==2:
        return 1
    return fib(N-1)+fib(N-2)
```
递归算法的时间复杂度计算 - 子问题个数乘以解决一个子问题需要的时间 O(2^N)
2. memo 递归
```python
def fib(n: int):
    memo=[0]*(n+1)
    return helper(memo,n)

def helper(memo: List[int], n:int):
    # base case
    if n==0 or n ==1:
        return n
    # calculated
    if memo[n]!=0:
        return memo[n]
    # 递归
    memo[n]=helper(memo,n-1)+helper(memo,n-2)
    return memo[n]

```
算法复杂度 O(N)
3. dp 数组的迭代递推法
```python
def fib(int n):
    if n==0:
        return 0
    dp=[0]*(n+1)
    dp[0]=0
    dp[1]=1
    for i in range(2,n+1):
        dp[i]=dp[i-1]+dp[i-2]
    return dp[n]
```
回溯 -  多叉树遍历
动态规划 - 1. 暴力穷举(状态转移方程) 2. 加备忘录即自顶向下递归 3. 优化之后自底向上地推迭代 4. 空间压缩
数组 - 



