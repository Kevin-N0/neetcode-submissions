class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Sorting 
        # Time: O(m * nlogn) <-- O(n~is len longest str) + O(m~ num strs)
        # Space: O(m * n)
        # Feedback: 
        # res = defaultdict(list)
        # for s in strs: 
        #     sortedS = ''.join(sorted(s))
        #     res[sortedS].append(s)
        # return list(res.values())

        # Hash Table
        # Time: O(m * n) <-- O(m ~ num strings) + O(n ~ len longest str)
        # Space: 
        # O(m) ~ auxillary space, excluding returned output 
        # O(m * n) total space if output groups are counted 
        # Feedback: 
        # res = defaultdict(list)
        # for s in strs: 
        #     count = [0] * 26
        #     for c in s: 
        #         count[ord(c) - ord('a')] += 1 
        #     res[tuple(count)].append(s)
        # return list(res.values())


        # 
        # Time: 
        # Space: 
        # Feedback: 

        res = defaultdict(list)
        for s in strs: 
            sortedS = ''.join(sorted(s))
            res[sortedS].append(s)
        return list(res.values())

        