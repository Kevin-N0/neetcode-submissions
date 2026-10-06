class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        str_map = defaultdict(list)
        for s in strs:
            s_sorted = ''.join(sorted(s))
            str_map[s_sorted].append(s)
        return list(str_map.values())