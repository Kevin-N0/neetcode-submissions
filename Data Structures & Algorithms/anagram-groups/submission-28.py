class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res_map = defaultdict(list)
        for s in strs:
            sorted_s = ''.join(sorted(s))
            res_map[sorted_s].append(s)
        return list(res_map.values())