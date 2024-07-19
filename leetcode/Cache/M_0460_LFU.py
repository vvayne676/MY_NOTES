class Node:
    def __init__(self, key,val=0,prev=None,nxt=None):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = prev
        self.next = nxt

class DLinkedList:
    def __init__(self):
        self.head=Node('Head')
        self.tail=Node('Tail')
        self.head.next=self.tail
        self.tail.prev=self.head
        self.size = 0

    def addToHead(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next = node
        node.next.prev = node
        self.size += 1

    def removeNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node

from collections import defaultdict
class LFUCache:
    def __init__(self, capacity: int):

        self.dct = {}
        # 使用 defaultdict(DLinkedList) 可以在访问不存在的键时自动创建一个新的 
        # DLinkedList 实例。这避免了在代码中显式检查键是否存在及初始化的繁琐步骤
        self.freq = defaultdict(DLinkedList)
        self.size = 0
        self.capacity = capacity
        self.min_freq = 0

    def get(self, key: int) -> int:
        if key in self.dct:
            node = self.dct[key]
            self.freq[node.freq].removeNode(node)
            if self.min_freq == node.freq and self.freq[node.freq].size == 0:
                self.min_freq += 1
            node.freq += 1
            self.freq[node.freq].addToHead(node)  
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.dct:
            node = self.dct[key]
            node.val = value
            self.freq[node.freq].removeNode(node)
            if self.min_freq == node.freq and self.freq[node.freq].size == 0:
                self.min_freq += 1
            node.freq += 1
            self.freq[node.freq].addToHead(node)
        else:
            self.size += 1
            if self.size > self.capacity:
                node = self.freq[self.min_freq].removeTail()
                self.dct.pop(node.key)
                self.size -= 1
            node = Node(key, value)
            self.dct[key] = node
            self.freq[1].addToHead(node)
            self.min_freq = 1
