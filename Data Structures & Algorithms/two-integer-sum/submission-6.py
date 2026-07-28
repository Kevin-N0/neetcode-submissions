class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {} # val -> index
        for i in range(len(nums)): 
            diff = target - nums[i]
            if diff in seen: 
                return [seen[diff], i]
            seen[nums[i]] = i
        return
#        return [0, 0]
            
        