1. Heapify 
    1. start from the first index of non-leaf node whose index is given by n/2-1 (i=n/2-1)
    2. set current element `i` as `largest` (largest = i)
    3.  left child of `i` is `2i+1`, right child is `2i+2`, if element of `2i+1` greater than element `i`, set `2i+1` largest, if element of `2i+2` greater than element `i`, set `2i+2` as largest. 
    4. swap element of `largest` with element of `i`
    5. repeat steps 2-4 until the subtrees are heapified
```
heapify(array, size, i)
    largest=i
    lc=2i+1
    rc=2i+2

    if array[lc]>array[largest]
        largest=lc
    if array[rc]>array[largest]
        largest=rc

construct(array, size)
    loop from the first index of non-leaf node down to zero
        heapify(array, size, i)

For Min-Heap, both leftChild and rightChild must be larger than the parent for all nodes.
```

2. Insert element into Priority queue
    1. insert new element at the end of the tree
    2. heapify the tree

3. Delete element from Priority Queue
    1. select element to be deleted
    2. swap it with the last element
    3. remove the last element
    4. heapify the tree

```python
class MinHeap:
    def __init__(self):
        self.heap = []

    # append to end of list then swim
    def insert(self, val):
        self.heap.append(val)
        self._swim(len(self.heap) - 1)

    # 1. swap end and begining element of list
    # 2. remove end element
    # 3. sink begining element
    def pop(self):
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)
        min_val = self.heap.pop()
        self._sink(0)
        return min_val


    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # smaller element go up
    def _swim(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx] < self.heap[parent]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    # bigger element go down
    def _sink(self, idx):
        n = len(self.heap)
        while 1:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break


if __name__ == '__main__':
    a=[1,4,7,2,6,8,3,7,10]
    heap=MinHeap()
    for v in a:
        heap.insert(v)
    while heap.heap:
        print(heap.pop())
```




```python
def heap_sort(arr):
    build_heap(arr)
    for i in range(len(arr) - 1, 0, -1):
        swap(arr, 0, i)
        heapify_down(arr, 0, i)
        print(arr)


def build_heap(arr):
    # last non-leaf node
    size = len(arr)
    lastNonLeaf = (size - 1 - 1) // 2
    for i in range(lastNonLeaf, -1, -1):
        heapify_down(arr, i, len(arr))


def heapify_up(arr, i):
    while i > 0:
        non_leaf = (i - 1) // 2
        if arr[i] > arr[non_leaf]:
            swap(arr, i, non_leaf)
            i = non_leaf
        else:
            break


def heapify_down(arr, i, end):
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < end and arr[left] > arr[largest]:
            largest = left
        if right < end and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            swap(arr, i, largest)
            i = largest
        else:
            break


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def insert(arr, val):
    arr.append(val)
    heapify_up(arr, len(arr) - 1)


def delete(arr, val):
    size = len(arr)
    i = 0
    for i in range(size):
        if arr[i] == val:
            break
    swap(arr, i, -1)  # swap with last element
    arr.pop()  # remove the last element

    if i < len(arr):
        heapify_down(arr, i, len(arr))


if __name__ == '__main__':
    ar = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    heap_sort(ar)


```


