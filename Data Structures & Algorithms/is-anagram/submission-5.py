class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_count = Counter(s)
        t_count = Counter(t)
        print(s_count == t_count)

        return s_set == t_set and len(s_set) == len(t_set)
            
