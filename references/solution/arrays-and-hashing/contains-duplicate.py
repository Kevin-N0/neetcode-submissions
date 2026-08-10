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
        Check every pair of elements. If any pair contains the same value, then the array contains a duplicate and we can return True immediately. This directly checks every possible pair, but it performs quadratic work in the worst case.

        ALGO:
        1. Iterate through nums with an outer index i.
        2. For each i, start an inner loop at i + 1.
        3. Compare nums[i] with nums[j].
        4. If they are equal, return True.
        5. If every pair is checked without finding a match, return False.

        TIME: O(n^2)
        In the worst case, we compare every pair of elements. The number of comparisons is approximately n(n - 1) / 2. Therefore the total time complexity is O(n^2).

        SPACE: O(1)
        The algorithm only uses loop indices and fixed variables. No additional data structure grows with the size of nums.


        [S2]-[Sorting]

        INT:
        Sort nums so that equal values appear next to each other. After sorting, any duplicate must appear as a pair of adjacent equal values. We can then scan the array once and compare each value with the previous value.

        ALGO:
        1. Sort nums.
        2. Iterate from index 1 through the end of the array.
        3. Compare nums[i] with nums[i - 1].
        4. If they are equal, return True.
        5. If the scan finishes without a match, return False.

        TIME: O(n log n)
        Sorting dominates the runtime. The adjacent scan is O(n), so the total is O(n log n) + O(n) = O(n log n).

        SPACE: O(n)
        Python's sorting implementation (Timsort) may require temporary storage proportional to n in the worst case.


        [S3]-[Hash Set]

        INT:
        Use a hash set to remember every value already seen. While scanning nums, if the current value is already in the set, then we know it appeared earlier and therefore have found a duplicate. Otherwise, add the value to the set and continue.

        ALGO:
        1. Create an empty set named seen.
        2. Iterate through each num in nums.
        3. If num is already in seen, return True.
        4. Otherwise, add num to seen.
        5. If the loop finishes, return False.

        TIME: O(n)
        Each element is processed at most once. Hash-set membership checks and insertions are expected O(1). Therefore the expected total runtime is O(n).

        SPACE: O(n)
        In the worst case, the set stores every distinct value from nums. Therefore the auxiliary space complexity is O(n).


        [APPROACH_COMPARISON]

        - Approach: S1
          Time: O(n^2)
          Time qualification: Worst case
          Space: O(1)
          Input modified: No
          Main advantage: Very direct and uses constant auxiliary space.
          Main disadvantage: Performs quadratic work in the worst case.

        - Approach: S2
          Time: O(n log n)
          Time qualification: Dominating sorting step
          Space: O(n)
          Input modified: Yes
          Main advantage: Simple duplicate detection after sorting.
          Main disadvantage: Modifies nums and is slower than expected hash-set lookup.

        - Approach: S3
          Time: O(n)
          Time qualification: Expected
          Space: O(n)
          Input modified: No
          Main advantage: Expected linear time and simple implementation.
          Main disadvantage: Requires additional memory for the set.


        [COMMON_PITFALLS]
        - Comparing nums[i] with nums[i] in the sorting approach instead of nums[i - 1].
        - Starting the sorted scan at index 0 and accidentally comparing the first element with nums[-1].
        - Adding num to the hash set before checking membership.
        - Forgetting that nums.sort() modifies the original input.
        - Claiming hash-set membership is guaranteed O(1) rather than expected O(1).
        - Returning False too early before the complete search has finished.

        @CONTENT_END

        @NC250_END
        """

        # S3 - Hash Set (Preferred Solution)
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

        # S2 CODE - Sorting
        # nums.sort()
        #
        # for i in range(1, len(nums)):
        #     if nums[i] == nums[i - 1]:
        #         return True
        #
        # return False
