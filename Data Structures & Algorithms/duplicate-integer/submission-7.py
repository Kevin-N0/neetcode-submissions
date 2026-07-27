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
        1. If we sort array, any duplicate values will appear next to each other
        2. Sorting groups identical elements together 
        3. Check adjacent positions to detect duplicates. 
        4. Single linear scan after sorting 

        ALGO: 
        1. Sort array in non-decreasing order
        2. Iterate through array starting from index 1
        3. Compare curreent vs. previous element 
        4. If both elements are equal, return True 
        5. If loop finishes without finding equal neighbors, return False 

        TIME: O(n log n)
        1. sorting - n log
        2. 

        SPACE: O(1) or O(n) depending on sorting algo
        1. 
        2. 


        [S3]-Hashing 
        INT: 
        1. Hash set to keep tracke of values already encountered 
        2. Iterate through array --> Check if current value is already prsent in set 
        3. If it is, a duplicate exists 

        ALGO: 
        1. Initialize empty hash set to store seen values 
        2. Iterate through each number in the array 
        3. For each number
        - if in set, return true because duplicate is found
        - otherwise add to set 
        4. If loop finishes without finding any duplicates, return False 

        TIME: O(n)
        1. 
        2. 

        SPACE: O(n)
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
        # nums.sort()
        # for i in range(1, len(nums)): 
        #     if nums[i] == nums[i - 1]: 
        #         return True
        # return False

        # S3 CODE - Hashing: 
        seen = set()
        for num in nums: 
            if num in seen: 
                return True
            seen.add(num)
        return False
            