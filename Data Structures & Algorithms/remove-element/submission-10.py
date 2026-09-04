class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # 1. Brute Force, O(), O()
        tmp = []
        for n in nums: 
            if n != val: 
                tmp.append(n)
        for i in range(len(tmp)):
            nums[i] = tmp[i]
        return len(tmp)

        # 2. Two Pointers - I, O(), O()
        k = 0 
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k


        # 3. Two Pointers - II, O(), O()
        