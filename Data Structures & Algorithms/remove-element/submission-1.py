class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # nums = [3, 2, 2, 3]
        # val = 3

        # Brute Force 
        # Time: 
        # Space: 
        # Feedback: 
        tmp = []
        for num in nums: 
            if num == val: 
                continue 
            tmp.append(num)
        for i in range(len(tmp)): 
            nums[i] = tmp[i]
        return len(tmp)
            




        # Two Pointers - I 
        # Time: 
        # Space: 
        # Feedback: 

        # Two Pointers - II 
        # Time: 
        # Space: 
        # Feedback: 
        