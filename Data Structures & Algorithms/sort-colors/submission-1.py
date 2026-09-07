class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 1. Brute Force, O(N log N), O(1) | O(N) depending on sorting algo
        nums.sort()

        # 2. Counting Sort, O(n), O(1)
        count = [0] * 3
        for num in nums:
            count[num] += 1
        write_idx = 0
        for i in range(3):
            while count[i]:
                count[i] -= 1
                nums[write_idx] = i
                write_idx += 1

        # 3. Three Pointers - I, O(), O()
        

        # 4. Three Pointers - II, O(), O()

        # 5. Three Pointers - III, O(), O()
