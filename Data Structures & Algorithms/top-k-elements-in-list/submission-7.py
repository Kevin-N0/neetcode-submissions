class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for val in nums:
            counts[val] = 1 + counts.get(val, 0)
        arr = []
        for val, count in counts.items():
            arr.append([count, val])
        arr.sort()
        res = []
        while len(res) < k:
            res.append(arr.pop()[1])
        return res