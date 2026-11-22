class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # O(n^2), O(1)
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [min(i, j), max(i, j)]
        prev = {} # K: num, V: index
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in prev:
                return [prev[diff], i]
            prev[nums[i]] = i
            
        