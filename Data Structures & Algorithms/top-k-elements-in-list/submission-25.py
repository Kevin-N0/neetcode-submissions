class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Sorting
        # O(n log n), O(n)
        # count_map = {}
        # for num in nums:
        #     count_map[num] = 1 + count_map.get(num, 0)
        # arr = []
        # for num, cnt in count_map.items():
        #     arr.append([cnt, num])
        # arr.sort()
        # res = []
        # while len(res) < k:
        #     res.append(arr.pop()[1])
        # return res

        # Bucket sort
        # O(n), O(n)
        count_map = {}
        for num in nums:
            count_map[num] = count_map.get(num, 0) + 1
        
        freq = [[] for _ in range(len(nums) + 1)]
        for num, cnt in count_map.items():
            freq[cnt].append(num)
        
        res = []
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res


        