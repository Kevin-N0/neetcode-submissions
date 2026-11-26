class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Sorting, TC: O(m * n log n), SC: (m * n)
        # str_map = defaultdict(list)
        # for s in strs:
        #     sorted_s = ''.join(sorted(s))
        #     str_map[sorted_s].append(s)
        # return list(str_map.values())


        # Hash Table
        str_map = defaultdict(list)
        for i, s in enumerate(strs):
            counts = [0] * 26
            for c in s:
                counts[ord(c) - ord('a')] += 1
            str_map[tuple(counts)].append(s)
        return list(str_map.values())


        