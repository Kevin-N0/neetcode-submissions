class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # 1. BF 
        # if len(s) != len(t):
        #     return False
        # return sorted(s) == sorted(t)

        # 2. Hash Map
        if len(s) != len(t):
            return False
        countS, countT = {}, {}
        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)
        return countS == countT




        # counts = [0] * 26
        # for c in s: 
        #     counts[ord(c) - ord('a')] += 1
        # for c in t: 
        #     counts[ord(c) - ord('a')] -= 1
        # return counts





        

        # s_sorted = ''.join(sorted(s))
        # t_sorted = ''.join(sorted(t))
        # return s_sorted == t_sorted
        
        