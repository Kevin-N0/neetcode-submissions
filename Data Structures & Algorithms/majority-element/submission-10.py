class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # 1. Brute Force, O(n^2), O(1)
        # l_num = len(nums)
        # for num in nums:
        #     count = 0 
        #     for val in nums:
        #         if val == num:
        #             count += 1
        #     if count > l_num // 2:
        #         return num

        # l_num = len(nums)
        # for num in nums:
        #     count = sum(1 for val in nums if val == num)
        #     if count > l_num // 2:
        #         return num

        # 2. Hash Map, O(), O()
        count = defaultdict(int)
        # count = {}
        majority_val = max_count = 0
        for num in nums:
            # count[num] = 1 + count.get(num, 0)
            count[num] += 1
            if max_count < count[num]:
                majority_val = num
                max_count = count[num]
        return majority_val




        # 3. Sorting, O(), O()

        # 4. Bit Manipulation, O(), O()









