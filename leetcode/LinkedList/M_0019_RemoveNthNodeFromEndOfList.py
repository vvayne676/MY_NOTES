# Constraints:
# The number of nodes in the list is sz.
# 1 <= sz <= 30
# 0 <= Node.val <= 100
# 1 <= n <= sz
# 
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        slow=fast=head
        counter=0
        while counter<n:
            fast=fast.next
            counter+=1
        if fast is None:
            head=head.next
            return head
        while fast.next:
            slow=slow.next
            fast=fast.next
        slow.next=slow.next.next
        return head

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy=ListNode()
        dummy.next=head
        fast=dummy
        slow=dummy
        for x in range(0,n):
            fast=fast.next
        
        while fast.next:
            fast=fast.next
            slow=slow.next
        slow.next=slow.next.next
        return dummy.next