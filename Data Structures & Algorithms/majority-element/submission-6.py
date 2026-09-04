class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # 1. Brute Force, O(), O()
        n = len(nums)
        for num in nums:
            count = 0 
            for val in nums:
                if val == num:
                    count += 1
            if count > n // 2:
                return num
            

        # 2. Hash Map, O(), O()

        # 3. Sorting, O(), O()

        # 4. Bit Manipulation, O(), O()









