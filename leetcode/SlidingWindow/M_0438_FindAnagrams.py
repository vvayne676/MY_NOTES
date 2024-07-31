'''
1. 先把窗口建立起来然后判断是否有满足条件的结果
2. for loop开始 移动窗口检查是否有符合条件的结果
'''
class Solution:
    # 函数返回的是起始index
    def findAnagrams(self, s: str, p: str) -> List[int]:
        dic=defaultdict(int)
        windowDict=defaultdict(int)
        if len(s)<len(p):
            return []
        res=[]
        for x in p:
            dic[x]+=1
        # if len(p)=3, window[s0,s1,s2]
        for i in range(len(p)):
            windowDict[s[i]]+=1
        
        if windowDict==dic:
            res.append(0)
      
        # 3,n
        for i in range(len(p),len(s)):
            # window add s3
            windowDict[s[i]]+=1
            # window remove s0
            windowDict[s[i-len(p)]] -= 1
            # new window comes del key whose value is 0
            if windowDict[s[i-len(p)]]==0:
                del windowDict[s[i-len(p)]]
            
            if windowDict==dic:
                res.append(i-len(p)+1)
            
           
        return res
    


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        left=0
        right=0
        dic = defaultdict(int)
        window = defaultdict(int)
        n=len(s)
        valid=0

        for v in p:
            dic[v]+=1
        
        res=[]
        while right<n:
            c=s[right]
     
            if c in dic:
                window[c]+=1
                if window[c]==dic[c]:
                    valid+=1
            right+=1
            while right-left==len(p):
                if valid == len(dic):
                    res.append(left)
                d=s[left]
                left+=1
                if d in dic:
                    if window[d]==dic[d]:
                        valid-=1
                    window[d]-=1
        return res
