class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        # 1. BF
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] == nums[j]:
        #             return True
        # return False

        # 2. Sorting
        # nums.sort()
        # for i in range(1, len(nums)):
        #     if nums[i] == nums[i - 1]:
        #         return True
        # return False

        # 3. Hash set
        # seen = set()
        # for n in nums: 
        #     if n in seen:
        #         return True
        #     seen.add(n)
        # return False

        # 4. Hash Set Length
        return len(set(nums)) < len(nums)
