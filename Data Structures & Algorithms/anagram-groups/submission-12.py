class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # 1. Sorting, O(L * N log N), O(N * L)
        # N is num of strings, L is lenth of longest str
        # res = defaultdict(list)
        # for s in strs: 
        #     sorted_s = "".join(sorted(s))
        #     res[sorted_s].append(s)
        # return list(res.values())


        # 2. Hash Table, O(), O()
        res = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s: 
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s)
        return list(res.values())


        