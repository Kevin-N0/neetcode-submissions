class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # O(n^2), O(1)
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]

        # O(n), O(n)
        prevMap = {} # K: num, V: index
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
        return []
            
        