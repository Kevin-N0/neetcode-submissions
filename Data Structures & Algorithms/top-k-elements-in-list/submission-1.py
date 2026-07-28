class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 2. Heap 
        count = Counter(nums)
        heap = []
        for num in count.keys():
            heapq.heappush(heap, (count[num], num))
            if len(heap) > k:
                heapq.heappop(heap)
        res = []
        for i in range(k): 
            res.append(heapq.heappop(heap)[1])
        return res



        # 1. Sorting 
        # counts = Counter(nums)
        # count = {}
        # for n in nums: 
        #     count[n] = 1 + count.get(n, 0)
        # arr = []
        # for num, cnt in count.items(): 
        #     arr.append([cnt, num])
        # arr.sort()
        # res = []
        # while len(res) < k: 
        #     res.append(arr.pop()[1])
        # return res 


        

        