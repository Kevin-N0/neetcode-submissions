class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # 1. BF 
        # if len(s) != len(t):
        #     return False
        # return sorted(s) == sorted(t)

        # 2. Hash Map
        # if len(s) != len(t):
        #     return False
        # countS, countT = {}, {}
        # for i in range(len(s)):
        #     countS[s[i]] = 1 + countS.get(s[i], 0)
        #     countT[t[i]] = 1 + countT.get(t[i], 0)
        # return countS == countT



        # 3. Hash Table Using Array
        if len(s) != len(t): 
            return False
        counts = [0] * 26
        for i in range(len(s)):
            counts[ord(s[i]) - ord('a')] += 1
            counts[ord(t[i]) - ord('a')] -= 1
        for val in counts: 
            if val != 0:
                return False
        return True
                





        

        # s_sorted = ''.join(sorted(s))
        # t_sorted = ''.join(sorted(t))
        # return s_sorted == t_sorted
        
        