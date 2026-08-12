class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
      # appeares more than once --> return False 

      # Brute Force 1: 
      # Time: O(n)
      # Space: O(n)
      # vals = []
      # for num in nums: 
      #   if num in vals: 
      #     return True 
      #   vals.append(num)
      # return False 

      # Brute Force 2: 
      # Time: O(n^2)
      # Space: O(1)
      # for i in range(len(nums)): 
      #   for j in range(i+1, len(nums)): 
      #     if nums[i] == nums[j]: 
      #       return True 
      # return False 



      # Sorting 
      # Time: O(n)
      # Space: O(n)
      # nums = sorted(nums)
      # Feedback: sort in place better
      nums.sort()
      for i in range(1, len(nums)): 
        if nums[i] == nums[i - 1]: 
          return True
      return False

      # Hash Set 
      # Time: O(n)
      # Space: O(n)
      # Feedback: You used a dict {} - which is NOT a hash set
      # -> Use set()
      # seen = {}
      # for num in nums:
      #   if num in seen: 
      #     return True 
      #   seen.add(num)
      # return False 

      # Hash Set Length 
      return len(set(nums)) < len(nums)

        