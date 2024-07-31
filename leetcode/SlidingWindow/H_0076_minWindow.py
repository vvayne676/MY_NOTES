class Solution:
    def minWindow(self, s: str, t: str) -> str:
        result=s+"a"
        targetPattern = defaultdict(int)
        for i in range(len(t)):
            targetPattern[t[i]]+=1
        valid=0
        window=defaultdict(int)
        left,right=0,0
       
        while right<len(s):
            c=s[right]
            window[c]+=1
    
            if window[c]==targetPattern[c]:
                valid+=1
            if targetPattern[c]==0:
                del targetPattern[c]
            right+=1
            
           
            while left<right and valid==len(targetPattern):
               
                d=s[left]
               
                if right-left < len(result):
                    result = s[left:right]
            
                if targetPattern[d]>0:
                    if window[d]==targetPattern[d]:
                        valid-=1
                else:
                    del targetPattern[d]
               
                window[d]-=1
                left+=1

        return result if result!=s+"a" else ""

