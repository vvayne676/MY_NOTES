计算机的2种存储方式 顺序存储 数组 和 链式存储 链表。 除此之外的数据结构都是衍生品。

## Cycle Array 
环形数组O(1)增删头部元素
[1,2,3,_,_,_] start 0, end 2
删头部 [_,2,3,_,_,_] start 1, end 2
头部插4 [4,2,3,_,_,_] start 0, end 2
头部插5 [4,2,3,_,_,5] start 5, end 2

当 start, end 移动超出数组边界 做 求模运算
区间为[start, end) 初始化 start=end=0 时候 [0,0)其中没有元素

头尾操作确实O(1) 但是中间操作数组还是要O(n)移动
### cycle array impl stack/queue
所以除了链表可以实现 stack/queue, 环形数组 CycleArray也可以

## Hash Table/Map
key hash之后放入table数组, 如何把key转化? 简单的方法返回该对象的内存地址. 如果 hash 冲突了
2种方法
1. 拉链 数组元素是个链表 往上面加
2. 开放寻址 当前位置往后顺序加

hash table Java为例初始16长度, load factor 0.75, 当哈希表的元素数量达到容量的75%时, 哈希表会进行扩容, 容量 double(Python的 dict 会根据插入和删除操作的频率动态调整容量, 以保持较高的性能)

从 key 的 hash 结果可以理解为什么 哈希表 的遍历顺序是不确定的
这里的不确定包含两种不确定
1. 和插入顺序不一样 (hash 映射后 在table中的位置 和 插入顺序无关)
2. 多次遍历 key 出现的顺序不一样 (扩容后 table 中的位置会变化)
Python 的 OrderedDict 通过维护一个双向链表来记录 K/V 的插入顺序. 

一般 hash table的实现都是基于 拉链法
### 开放寻址的难点
1. 需要环形数组 不然一直找到数组的末尾还没找到空位
2. 删除复杂 因为要维护元素的连续性
    * table 中删除元素时 把 hash(key)=x 的元素都往前挪 来保证线性探查的正确
    * 占位符 标记 简单但是占位符越来越多会影响 get 的效率 (最坏的情况 不停插入删除全是占位符 调用get因为环形数组原因会 死循环)

## Binary Tree
### Full Binary Tree
Each node either have left&right or not have both
### Complete Binary Tree

### Perfect Binary Tree
Each row have 2^n-1 node
### Binary Search Tree
Every node's left sub tree is less than its value, right sub tree is greater than its value

### Implementation of Binary Tree
1. 
```python
class Node:
    def __init__(self,val,left=None,right=None):
        self.val=val
        self.left=left
        self.right=right
```

2. Binary Heap

## Binary Heap
主要两个操作 sink 和 swim

主要用途 Priority Queue 和 Heap Sort

性质 - 任意节点的值 都 大/小于等于 其左右子树所有节点的值. 如果大于等于 称大顶堆 小于等于 小顶堆 增删复杂度 O(logN) N为二叉堆中的元素个数

# 数据结构基操
各种数据结构的 遍历 + 访问 两种形式：线性的和非线性的
* 迭代 for/while
* 递归 

## N叉树遍历
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
## 二叉树遍历
```python
def traverse(root):
    # pre-order operation
    traverse(root.left)
    # in-order operation
    traverse(root.right)
    # post-order operation