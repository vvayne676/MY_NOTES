# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        
        head=cur=ListNode()
        while list1 and list2:
            if list1.val<list2.val:
                temp=list1
                cur.next=temp
                list1=list1.next
                cur=cur.next
            else:
                temp = list2
                cur.next=temp
                list2=list2.next
                cur=cur.next
        if list1:
            cur.next=list1
        if list2:
            cur.next=list2
        return head.next