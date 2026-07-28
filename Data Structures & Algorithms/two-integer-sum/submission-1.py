class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        from collections import Counter
        from collections import defaultdict 
        seen = defaultdict()
        for n in range(len(nums) - 1): 
            diff = target - nums[n]
            if diff in seen: 
                return [seen[diff], n]
            seen[nums[n]] = n
        # return 
            
        