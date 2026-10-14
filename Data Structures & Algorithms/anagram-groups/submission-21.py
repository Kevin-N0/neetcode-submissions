class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            s_sorted = ''.join(sorted(s))
            res[s_sorted].append(s)
        return list(res.values())
        