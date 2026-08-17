class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # nums = [3, 2, 2, 3]
        # val = 3

        # Brute Force 
        # Time: O(n)
        # Space: O(n)
        # Feedback: 
        # tmp = []
        # for num in nums: 
        #     if num == val: 
        #         continue 
        #     tmp.append(num)
        # for i in range(len(tmp)): 
        #     nums[i] = tmp[i]
        # return len(tmp)
            
        # Two Pointers - I 
        # Time: O(n)
        # Space: O(1)
        # Feedback: 
        # k = 0 
        # for i in range(len(nums)): 
        #     if nums[i] != val: 
        #         nums[k] = nums[i]
        #         k += 1 
        # return k 

        # Two Pointers - II 
        # Time: O(n)
        # Space: O(1)
        # Feedback: When few elements...prev approach does unnessary copying 
        # i = 0 
        # n = len(nums)
        # while i < n: 
        #     if nums[i] == val: 
        #         n -= 1
        #         nums[i] = nums[n]

        #     else: 
        #         i += 1
        # return n 

        # BF
        # nums = [3, 2, 2, 3]
        # val = 3
        tmp = []

        for num in nums: 
            if num == val: 
                continue 
            tmp.append(num)
        for i in range(len(tmp)): 
            nums[i] = tmp[i]
        return len(tmp)

        # Two Pointers - I 


        # Two Pointers - II 


        