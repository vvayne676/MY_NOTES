
class Solution:
    def applePurchase(self, quantity: int, shop1: int,shop1Price:int, shop2:int, shop2Price:int) -> int:
        def helper(quantity: int,cost:int):
            nonlocal res
            if quantity<0:
                return
            if quantity==0:
                res=min(res,cost)
                return
            
            cost+=shop1Price
            helper(quantity-shop1,cost)
            cost-=shop1Price

            cost+=shop2Price
            helper(quantity-shop2,cost)
            cost-=shop2Price
        res=quantity*max(shop2Price,shop1Price)
        helper(quantity,0)
        return res