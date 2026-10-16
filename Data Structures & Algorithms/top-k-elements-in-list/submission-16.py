class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        res = {}
        for num in nums:
            res[num] = 1 + res.get(num, 0)

        arr = []
        for num, count, in res.items():
            arr.append([count, num])
        arr.sort()

        sol = []
        while len(sol) < k:
            sol.append(arr.pop()[1])
        return sol

