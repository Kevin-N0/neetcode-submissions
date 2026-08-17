class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # Brute Force 
        # Time: 
        # Space: 
        # Feeback: 
        # n = len(nums)
        # for num in nums: 
        #     count = sum(1 for i in nums if i == num)
        #     if count > n // 2: 
        #         return num 

        n = len(nums)
        for num in nums: 
            count = 0 
            for i in nums: 
                if i == num: 
                    count += 1 
            if count > n // 2: 
                return num 
    



        # Hash Map 
        # Time: 
        # Space: 
        # Feeback: 


        # Sorting
        # Time: 
        # Space: 
        # Feeback: 