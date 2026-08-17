class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # Brute Force 
        # Time: O(n * n) 
        # Space: O(1)
        # Feeback: O(n^2) <-- we definitely have to iterate over 2x 
        # n = len(nums)
        # for num in nums: 
        #     count = sum(1 for i in nums if i == num)
        #     if count > n // 2: 
        #         return num 

        # n = len(nums)
        # for num in nums: 
        #     count = 0 
        #     for i in nums: 
        #         if i == num: 
        #             count += 1 
        #     if count > n // 2: 
        #         return num 
    



        # Hash Map 
        # Time: O(n)
        # Space: O(n)
        # Feeback: 
        count = defaultdict(int)
        finalRes = maxCount = 0 
        for num in nums: 
            count[num] += 1 
            if maxCount < count[num]: 
                finalRes = num 
                maxCount = count[num]
        return finalRes 
            


        # Sorting
        # Time: 
        # Space: 
        # Feeback: 