class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        """
        [S1]-Brute Force
        INT: 
        1. Check every pair of elements & return true if any pair has equal values 
        2. Most intuitive b/c compares all possible pairs 
        3. Least efficient since it examines every combination 

        ALGO: 
        1. Iterate through array using 2 nested loops to check all possible pairs of 
        distint indices 
        2. If any pair has same value, return True 
        3. If all pairs are checked and no duplicates are found, return False 

        TIME: O()
        1. 
        2. 

        SPACE: O()
        1. 
        2. 

        [S2]-Sorting
        INT: 
        1. 
        2. 
        3. 

        ALGO: 
        1. 
        2. 
        3. 
        4.
        5.

        TIME: O()
        1. 
        2. 

        SPACE: O()
        1. 
        2. 


        [S3]-Hasing 
        INT: 
        1. 
        2. 
        3. 

        ALGO: 
        1. 
        2. 
        3. 
        4.
        5.

        TIME: O()
        1. 
        2. 

        SPACE: O()
        1. 
        2. 

        [COMMON PITFALLS]
        - Comparing element with itself 
        - Starting at i instead of i + 1
        


        """
        # S1 CODE - Brute Force: 
        # for i in range(len(nums)): 
        #     for j in range(i+1, len(nums)): 
        #         if nums[i] == nums[j]: 
        #             return True 
        # return False

        # S2 CODE - Sorting: 
        nums.sort()
        for i in range(1, len(nums)): 
            if nums[i] == nums[i - 1]: 
                return True
        return False
        
        # S3 CODE - Hashing: 