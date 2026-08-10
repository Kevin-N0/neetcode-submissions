from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        """
@NC250_START

TYPE: SOLUTION_REFERENCE
SCHEMA_VERSION: 1
CATEGORY: Arrays & Hashing
PREFERRED_SOLUTION: S3

@PROBLEM_DETAILS_START

PROBLEM: Contains Duplicate
URL: https://neetcode.io/problems/duplicate-integer/question?list=neetcode250
DIFFICULTY: Easy
PROBLEM DETAILS:

Given an integer array nums, return true if any value appears more
than once in the array, otherwise return false.

Example 1:

Input:
nums = [1, 2, 3, 3]

Output:
true

Example 2:

Input:
nums = [1, 2, 3, 4]

Output:
false

Constraints:

- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

@PROBLEM_DETAILS_END

@CONTENT_START

[S1]-[Brute Force]

INT:
Check every pair of elements and return True if any pair contains equal values. Comparing every possible pair guarantees that any duplicate will eventually be found. This is the most direct approach, but it is inefficient because it may need to examine every pair in the array.

ALGO:
1. Iterate through nums with an outer index i.
2. For each i, start an inner loop at i + 1.
3. Compare nums[i] with nums[j].
4. If they are equal, return True immediately.
5. If every pair is checked without finding a duplicate, return False.

TIME: O(n^2)
Let n be the number of elements in nums. In the worst case, the nested loops compare every pair of elements. The number of comparisons is n(n - 1) / 2. After simplifying, the dominant term is O(n^2).

SPACE: O(1)
The algorithm only uses loop indices and a constant number of variables. No additional data structure grows with the size of nums.


[S2]-[Sorting]

INT:
Sort nums so equal values appear next to each other. If a duplicate exists, then after sorting at least one pair of adjacent elements must be equal. We can therefore scan the sorted array once and compare each value with the value immediately before it.

ALGO:
1. Sort nums in non-decreasing order.
2. Start scanning from index 1.
3. Compare nums[i] with nums[i - 1].
4. If they are equal, return True.
5. If the scan finishes without finding equal adjacent values, return False.

TIME: O(n log n)
Sorting nums takes O(n log n) time. The adjacent scan takes O(n) time. Therefore, O(n log n) + O(n) = O(n log n).

SPACE: O(n)
Python's sorting implementation (Timsort) may require temporary storage proportional to n in the worst case. The boolean return value and loop variables use constant space. This approach modifies nums.


[S3]-[Hash Set]

INT:
Use a hash set to keep track of values already encountered. While scanning nums, if the current value is already in the set, then that value must have appeared earlier. Finding a value that is already present therefore proves that the array contains a duplicate. Otherwise, add the value to the set and continue scanning.

ALGO:
1. Create an empty set named seen.
2. Iterate through each num in nums.
3. If num is already in seen, return True.
4. Otherwise, add num to seen.
5. If the loop finishes without finding a duplicate, return False.

TIME: O(n)
Each element is processed at most once. Hash-set membership checks and insertions are expected O(1). Therefore, the expected total runtime is O(n). Pathological hash-collision behavior can produce worse theoretical performance, but expected hash-set operations are constant time.

SPACE: O(n)
In the worst case, all values are unique and the set stores all n elements. Therefore, the auxiliary-space complexity is O(n).


[APPROACH_COMPARISON]

- Approach: S1-Brute Force
  Time: O(n^2)
  Time qualification: Worst case when all elements are unique or the duplicate is at the end.
  Space: O(1)
  Input modified: No
  Main advantage: Very direct and requires no additional data structure.
  Main disadvantage: Performs quadratic work in the worst case.

- Approach: S2-Sorting
  Time: O(n log n)
  Time qualification: Dominated by the sorting step.
  Space: O(n)
  Input modified: Yes
  Main advantage: Duplicate detection becomes simple after sorting.
  Main disadvantage: Modifies the input and is slower than the expected hash-set approach.

- Approach: S3-Hash Set
  Time: O(n)
  Time qualification: Expected linear time.
  Space: O(n)
  Input modified: No
  Main advantage: Expected linear-time duplicate detection.
  Main disadvantage: Requires additional memory proportional to the number of distinct values.


[COMMON_PITFALLS]
- Comparing nums[i] with nums[i] in the sorting approach instead of nums[i - 1].
- Starting the sorted scan at index 0 and accidentally using nums[-1].
- Adding num to seen before checking whether it is already present.
- Returning False inside the loop before every necessary element has been processed.
- Forgetting that nums.sort() modifies the input array.
- Claiming hash-set membership and insertion are guaranteed O(1) worst-case instead of expected O(1).

@CONTENT_END

@NC250_END
"""
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False

        # S1 CODE - Brute Force
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] == nums[j]:
        #             return True
        #
        # return False
        #
        #
        # S2 CODE - Sorting
        #
        # nums.sort()
        #
        # for i in range(1, len(nums)):
        #     if nums[i] == nums[i - 1]:
        #         return True
        #
        # return False
