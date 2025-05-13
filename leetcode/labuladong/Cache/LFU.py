from collections import defaultdict
class Node:
    def __init__(self, key,val=0,prev=None,nxt=None):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = prev
        self.nxt = nxt

class DLinkedList:
    def __init__(self):
        self.head = Node('HEAD')
        self.tail = Node('TAIL')
        self.head.nxt = self.tail
        self.tail.prev = self.head
        self.size = 0

    def addToHead(self,node):
        tmp = self.head.next

        node.next = tmp
        node.prev = self.head

        self.head.next=node
        tmp.prev = node

        self.size += 1

    def removeNode(self, node):
        node.prev.nxt = node.nxt
        node.nxt.prev = node.prev
        self.size -= 1
    
    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node

class LFUCache:
    def __init__(self, capacity):
        self.dct = {}
        self.freq = defaultdict(DLinkedList)
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0

    def get(self, key):
        if key in self.dct:
            node = self.dct[key]
            self.freq[node.freq].removeNode(node)
            if self.freq[node.freq].size == 0 and self.min_freq == node.freq :
                self.min_freq += 1
            self.freq[node.freq].addToHead(node)
            return node.val
        return -1
    def put(self, key, val):
        if self.capacity == 0:
            return
        if key in self.dct:
            node = self.dct[key]
            node.val = val
            self.freq[node.freq].removeNode(node)
            if self.freq[node.freq].size == 0 and self.min_freq == node.freq:
                self.min_freq += 1
            node.freq += 1
            self.freq[node.freq].addToHead(node)
        else:
            self.size += 1
            if self.size > self.capacity:
                node = self.freq[self.min_freq].removeTail()
                self.dct.pop(node.key)
                self.size -= 1
            node = Node(key, val)
            self.dct[key] = node
            self.freq[1].addToHead(node)
            self.min_freq = 1