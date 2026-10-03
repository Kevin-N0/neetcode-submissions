# =====================================================================
# PROBLEM 1: Two Sum
# =====================================================================

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S4

        @PROBLEM_DETAILS_START

        PROBLEM: Two Sum

        URL: https://neetcode.io/problems/two-integer-sum/question?list=blind75

        DIFFICULTY: Easy

        PROBLEM DETAILS:

        Given an array of integers nums and an integer target, return the
        indices i and j such that nums[i] + nums[j] == target and i != j.

        You may assume that every input has exactly one pair of indices i and j
        that satisfy the condition.

        Return the answer with the smaller index first.

        Example 1:

        Input:
        nums = [3,4,5,6], target = 7

        Output:
        [0,1]

        Explanation:
        nums[0] + nums[1] == 7, so we return [0, 1].

        Example 2:

        Input:
        nums = [4,5,6], target = 10

        Output:
        [0,2]

        Example 3:

        Input:
        nums = [5,5], target = 10

        Output:
        [0,1]

        Constraints:

        - 2 <= nums.length <= 1000
        - -10,000,000 <= nums[i] <= 10,000,000
        - -10,000,000 <= target <= 10,000,000
        - Only one valid answer exists.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Brute Force

        INT:

        Check every pair of different elements and return the first pair whose
        sum equals target. This directly mirrors the problem statement, but it
        repeats pair checks and is the least efficient extracted approach.

        ALGO:

        1. Iterate i through the array.
        2. Iterate j from i + 1 through the array.
        3. If nums[i] + nums[j] == target, return [i, j].
        4. Return [] only as a fallback.

        TIME: O(n^2)

        Two nested loops may inspect every pair.

        SPACE: O(1)

        Only constant auxiliary state is used.


        [S2]-Sorting / Two Pointers

        INT:

        Attach each value to its original index, sort by value, then use a
        left and right pointer. Sorting allows the sum to be adjusted
        monotonically while original indices remain recoverable.

        ALGO:

        1. Build [value, original_index] pairs.
        2. Sort the pairs.
        3. Place pointers at both ends.
        4. Move the left pointer right when the sum is too small.
        5. Move the right pointer left when the sum is too large.
        6. When the sum equals target, return the original indices in
           increasing order.

        TIME: O(n log n)

        Sorting dominates the two-pointer scan.

        SPACE: O(n)

        A separate list of value/index pairs is stored.


        [S3]-Hash Map (Two Pass)

        INT:

        Store every value and its index first. A second pass checks whether
        target - nums[i] exists at a different index.

        ALGO:

        1. Build a value -> index map.
        2. Traverse nums again.
        3. Compute diff = target - nums[i].
        4. If diff is in the map and maps to a different index, return the
           pair.

        TIME: O(n)

        Both passes are linear with average O(1) hash operations.

        SPACE: O(n)

        The hash map may store every input value.


        [S4]-Hash Map (One Pass)

        INT:

        As each value is visited, check whether its needed complement was
        already seen. If so, the previously stored index and the current
        index form the answer. Otherwise store the current value and index.

        ALGO:

        1. Initialize an empty value -> index map.
        2. For each index i and value n, compute diff = target - n.
        3. If diff is already in the map, return [map[diff], i].
        4. Otherwise store n -> i.

        TIME: O(n)

        Each element is processed once with average O(1) hash lookup/insertion.

        SPACE: O(n)

        The map can hold up to n entries.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Check all pairs.
        - Time: O(n^2)
        - Space: O(1)
        - Input modified: No
        - Main advantage: Simplest direct implementation.
        - Main disadvantage: Quadratic runtime.

        S2:

        - Approach: Sort value/index pairs and use two pointers.
        - Time: O(n log n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Avoids quadratic pair enumeration.
        - Main disadvantage: Sorting is slower than the hash-map approaches.

        S3:

        - Approach: Build a full hash map, then search complements.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Linear expected runtime.
        - Main disadvantage: Requires two passes.

        S4:

        - Approach: Check complements while building the hash map.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Linear expected runtime in one pass.
        - Main disadvantage: Uses O(n) auxiliary hash-map space.

        [COMMON_PITFALLS]

        - Do not use the same array element twice.
        - Return the smaller index first.
        - Duplicates are valid, so store indices rather than only testing
          value existence.

        [SOURCE_NOTES]

        - Active submitted implementation uses S4.
        - The source guarantees exactly one valid answer.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        prevMap = {}  # val -> index

        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Brute Force
        #
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        # return []
        #
        #
        # S2 CODE - Sorting / Two Pointers
        #
        # A = []
        # for i, num in enumerate(nums):
        #     A.append([num, i])
        #
        # A.sort()
        # i, j = 0, len(nums) - 1
        # while i < j:
        #     cur = A[i][0] + A[j][0]
        #     if cur == target:
        #         return [min(A[i][1], A[j][1]),
        #                 max(A[i][1], A[j][1])]
        #     elif cur < target:
        #         i += 1
        #     else:
        #         j -= 1
        # return []
        #
        #
        # S3 CODE - Hash Map (Two Pass)
        #
        # indices = {}  # val -> index
        #
        # for i, n in enumerate(nums):
        #     indices[n] = i
        #
        # for i, n in enumerate(nums):
        #     diff = target - n
        #     if diff in indices and indices[diff] != i:
        #         return [i, indices[diff]]
        # return []
