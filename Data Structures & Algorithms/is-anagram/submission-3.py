class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return set(s) == set(t) and len(set(s)) == len((set(t)))
            
