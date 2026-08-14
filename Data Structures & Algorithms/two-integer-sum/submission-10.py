class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Brute Force
        # Time: O(n^2) 
        # Space: O(1)
        # Feedback: 
        # for i in range(len(nums)): 
        #     for j in range(i+1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        # return []

        # Sorting
        # Time: O(O(n) + n log n) --> O(n log n)
        # Space: O(1)
        # Feedback: WRONG
        # nums.sort()
        # l, r = 0, len(nums) - 1
        # while l < r: 
        #     total = nums[l] + nums[r]
        #     if total == target:
        #         return [l, r]
        #     elif total < target: 
        #         l += 1 
        #     else: 
        #         r -= 1 
        # return []

        A = []
        for i, num in enumerate(nums):
            A.append([num, i])
        A.sort()
        l, r = 0, len(nums) - 1
        # while l < r: 
        #     first_val, sec_val = A[l][0], A[r][0]
        #     first_ind, sec_ind = A[l][1], A[r][1]
        #     cur = first_val + sec_val
        #     if cur == target: 
        #         return [min(first_ind, sec_ind), max(first_ind, sec_ind)]
        #     if cur < target: 
        #         l += 1 
        #     else: 
        #         r -= 1 
        # return []
        while l < r: 
            l_val, l_idx = A[l]
            r_val, r_idx = A[r]
            cur = l_val + r_val
            if cur == target: 
                return [min(l_idx, r_idx), max(l_idx, r_idx)]
            if cur < target:
                l += 1 
            else:
                r -= 1 
        return []








        # Hash Map (Two Pass)
        # Time:
        # Space:
        # Feedback: 

        # Hash Map (One Pass)
        # Time:
        # Space:
        # Feedback: 
        