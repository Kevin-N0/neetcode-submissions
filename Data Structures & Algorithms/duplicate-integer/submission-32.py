class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        # TC: O(n^2) SC: O(1)
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] == nums[j]:
        #             return True
        # return False

        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False
            
            