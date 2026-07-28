class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import Counter 
        s_count = Counter(s)
        t_count = Counter(t)
        return (s_count == t_count)

        # return s_set == t_set and len(s_set) == len(t_set)
            
