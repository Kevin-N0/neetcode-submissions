class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 1. BF
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        # return []

        # 2. Sorting 
        # A = []
        # for i, num in enumerate(nums):
        #     A.append([num, i])
        # A.sort()
        # l, r = 0, len(nums) - 1
        # while l < r: 
        #     l_val, l_idx = A[l]
        #     r_val, r_idx = A[r]
        #     cur = l_val + r_val
        #     if cur == target:
        #         return [min(l_idx, r_idx), max(l_idx, r_idx)]
        #     if cur < target:
        #         l += 1
        #     else: 
        #         r -= 1
        # return []

        # 3. Hash Map (two pass)
        # indices = {}

        # for i, n in enumerate(nums):
        #     indices[n] = i
        
        # for i, n in enumerate(nums):
        #     diff = target - n
        #     if diff in indices and indices[diff] != i: 
        #         return [i, indices[diff]]
        # return []



        A = []
        for i, n in enumerate(nums):
            A.append([n, i])
        A.sort()
        l, r = 0, len(nums) - 1

        while l < r: 
            l_val, l_idx = A[l]
            r_val, r_idx = A[r]
            curr = l_val + r_val
            if curr == target: 
                return [min(l_idx, r_idx), max(l_idx, r_idx)]
            if curr < target: 
                l += 1 
            else: 
                r -= 1
        return []



            

        