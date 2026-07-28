class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # counts = Counter(nums)
        count = {}
        for n in nums: 
            count[n] = 1 + count.get(n, 0)

        arr = []
        for k, v in count.items(): 
            arr.append([k, v])
        print(arr)
        arr.sort()
        print(arr)
        

        