class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # 1. Brute Force, O(n), O(n)
        # tmp = []
        # for n in nums: 
        #     if n != val: 
        #         tmp.append(n)
        # for i in range(len(tmp)):
        #     nums[i] = tmp[i]
        # return len(tmp)

        # 2. Two Pointers - I, O(n), O(1)
        # k = 0 
        # for i in range(len(nums)):
        #     if nums[i] != val:
        #         nums[k] = nums[i]
        #         k += 1
        # return k


        # 3. Two Pointers - II, O(), O()
        l, r = 0, len(nums)
        while l < r: 
            if nums[l] == val:
                r -= 1
                nums[l] = nums[r]
            else:
                l += 1
        return r

        