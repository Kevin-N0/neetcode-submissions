# 1. Quick Sort, avg~O(N log N) | worst~O(N^2), O(log N)
# class Solution:
#     def sortArray(self, nums: List[int]) -> List[int]:

#         def partition(self, nums: List[int], left: int, right: int) -> int: 
#             # mid = (left + right) >> 1
            
        

# 2. Merge Sort 
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1: 
            return nums.copy()
        middle_idx = len(nums) // 2
        left_sorted = self.sortArray(nums[:middle_idx])
        right_sorted = self.sortArray(nums[middle_idx:])
        return self._merge(left_sorted, right_sorted)
    
    def _merge(self, left_sorted: List[int], right_sorted: List[int]) -> List[int]:
        merged: List[int] = []
        i = j = 0
        while i < len(left_sorted) and j < len(right_sorted):
            if left_sorted[i] <= right_sorted[j]:
                merged.append(left_sorted[i])
                i += 1
            else: 
                merged.append(right_sorted[j])
                j += 1
        merged.extend(left_sorted[i:])
        merged.extend(right_sorted[j:])
        return merged

# 3. Heap Sort

# 4. Counting Sort

# 5. Radix Sort


# 6. Shell Sort