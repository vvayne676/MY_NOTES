

def heapSort(arr):
    buildHeap(arr)

    for i in range(len(arr)-1, 0,-1):
        swap(arr,0,i)
        heapify_down(arr,i)
    return arr


def buildHeap(arr):
    # last non-leaf node
    size=len(arr)
    lastNonLeaf = (size-1-1)//2
    for i in range(lastNonLeaf, -1, -1):
        heapify_down(arr, i)

# 实际上是从上往下的一个遍历保证以 i 为根结点的树符合 heap 特性
# 交换 i 和 left/right 的值之后 往下走 看是否继续交换
def heapify_down_re(arr, i):
    left = 2*i+1
    right = 2*i+2
    largest = i

    if left < len(arr) and arr[left] > arr[largest]:
        largest = left
    if right < len(arr) and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        swap(arr, i, largest)
        heapify_down(arr, largest)

def heapify_up_re(arr, i):
    non_leaf = (i-1)//2
    if i > 0 and arr[i] > arr[non_leaf]:
        swap(arr, i, non_leaf)
        heapify_up_re(arr, non_leaf)

def heapify_up(arr, i):
    while i > 0:
        non_leaf = (i-1)//2
        if arr[i] > arr[non_leaf]:
            swap(i, non_leaf)
            i = non_leaf
        else:
            break

def heapify_down(arr, i):
    while True:
        left = 2*i+1
        right = 2*i+2
        largest = i

        if left < len(arr) and arr[left] > arr[largest]:
            largest = left
        if right < len(arr) and arr[right] > arr[largest]:
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
    heapify_up(arr, len(arr)-1)


def delete(arr, val):
    size = len(arr)
    i = 0
    for i in range(size):
        if arr[i]==val:
            break
    swap(arr,i,-1) # swap with last element
    arr.pop() # remove the last element 

    if i < len(arr):
        heapify_down(arr, len(arr),i)
