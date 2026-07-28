class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_set = set(s)
        t_set = set(t)

        return s_set == t_set and len(s_set) == len(t_set)
            
