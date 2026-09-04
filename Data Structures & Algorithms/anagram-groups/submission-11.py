class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # 1. Sorting, O(), O()
        res = defaultdict(list)
        for s in strs: 
            sorted_s = "".join(sorted(s))
            res[sorted_s].append(s)
        return list(res.values())


        # 2. Hash Table, O(), O()


        