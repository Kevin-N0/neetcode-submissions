# 1. Quick Sort, avg~O(N log N) | worst~O(N^2), O(log N)
# Approach 2: 3-Way QuickSort (Dutch National Flag Partition)
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums
        def _quick_sort(left_idx: int, right_idx: int) -> None:
            if left_idx >= right_idx:
                return
            import random
            pivot_idx = random.randint(left_idx, right_idx)
            # pivot_idx = (left_idx + right_idx) // 2
            pivot_val = nums[pivot_idx]

            less_ptr = left_idx
            greater_ptr = right_idx
            curr_idx = left_idx

            while curr_idx <= greater_ptr:
                if nums[curr_idx] < pivot_val:
                    nums[curr_idx], nums[less_ptr] = nums[less_ptr], nums[curr_idx]
                    less_ptr += 1
                    curr_idx += 1
                elif nums[curr_idx] > pivot_val:
                    nums[curr_idx], nums[greater_ptr] = nums[greater_ptr], nums[curr_idx]
                    greater_ptr -= 1
                else:
                    curr_idx += 1
            
            _quick_sort(left_idx, less_ptr - 1)
            _quick_sort(greater_ptr + 1, right_idx)
        _quick_sort(0, len(nums) - 1)
        return nums
        


            
            
            









            
        


























        

# 2. Merge Sort 
### Approach 2: Merge Sort (Guaranteed O(N log N)) - Active
# Time: O(N log N) | Space: O(N)
# class Solution:
#     def sortArray(self, nums: List[int]) -> List[int]:
#         if len(nums) <= 1: 
#             return nums.copy()
#         middle_idx = len(nums) // 2
#         left_sorted = self.sortArray(nums[:middle_idx])
#         right_sorted = self.sortArray(nums[middle_idx:])
#         return self._merge(left_sorted, right_sorted)
#     def _merge(self, left_sorted: List[int], right_sorted: List[int]) -> List[int]:
#         merged: List[int] = []
#         i = j = 0
#         while i < len(left_sorted) and j < len(right_sorted):
#             if left_sorted[i] <= right_sorted[j]:
#                 merged.append(left_sorted[i])
#                 i += 1
#             else: 
#                 merged.append(right_sorted[j])
#                 j += 1
#         merged.extend(left_sorted[i:])
#         merged.extend(right_sorted[j:])
#         return merged

# 3. Heap Sort

# 4. Counting Sort
