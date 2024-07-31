class Solution:
    def lengthOfLongestNonRepeatedSubstring(self, s: str) -> int:

        window=deque()
        res=0
        for i in range(len(s)):
            if s[i] not in window:
                window.append(s[i])
            else:
                while s[i] in window:
                    window.popleft()
                window.append(s[i])
            res=max(res,len(window))
        return res

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window=defaultdict(int)

        left=0
        right=0
        res=0

        while right<len(s):
            c = s[right]
            window[c]+=1
            
            right+=1

            while left<right and  window[c]>1:
                d=s[left]
                window[d]-=1

                left+=1
            res = max(res,right-left) 

        return res
