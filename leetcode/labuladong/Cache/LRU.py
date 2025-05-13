class DLinkedList():
    def __init__(self, key, val=0, prev=None, nxt=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.nxt = nxt

        
class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.dct = dict()
        self.head = DLinkedList('HEAD')
        self.tail = DLinkedList('TAIL')
        self.head.nxt = self.tail
        self.tail.prev = self.head

    def removeNode(self, node):
        node.prev.nxt = node.nxt
        node.nxt.prev = node.prev

    def removeTail(self):
        
        node = self.tail.prev
        
        self.removeNode(node)
        return node
    
    def addToHead(self, node):
        tmp = self.head.nxt

        self.head.nxt = node
        node.prev = self.head

        node.nxt =  tmp
        tmp.prev = node
    
  
       

    def get(self, key):
        if key not in self.dct:
            return -1
        node = self.dct[key]

        self.removeNode(node)
        self.addToHead(node)
        
        return node.val
    
    def put(self, key, val):
        if key not in self.dct:
            node = DLinkedList(key, val)
            self.addToHead(node)
            self.size += 1
            self.dct[key] = node

            if self.size > self.capacity:
                tail = self.removeTail()
                self.dct.pop(tail.key)
                self.size -= 1
        else:
            node = self.dct[key]
            node.val = val
            self.moveToHead(node)