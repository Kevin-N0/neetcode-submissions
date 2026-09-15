class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1. Sorting, O(n log n), O(n)
        # counts = {}
        # for val in nums:
        #     counts[val] = 1 + counts.get(val, 0)
        # arr = []
        # for val, count in counts.items():
        #     arr.append([count, val])
        # arr.sort()
        # res = []
        # while len(res) < k:
        #     res.append(arr.pop()[1])
        # return res
        # 2. Min-Heap
        count = {}
        for val in nums:
            count[val] = 1 + count.get(val, 0)
        heap = []
        for val in count.keys():
            heapq.heappush(heap, (count[val], val))
            if len(heap) > k:
                heapq.heappop(heap)
        res = []
        for i in range(k):
            res.append(heapq.heappop(heap)[1])
        return res

