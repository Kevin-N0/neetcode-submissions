# =====================================================================
# PROBLEM 6: Longest Consecutive Sequence
# =====================================================================

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing / Hash Set
        PREFERRED_SOLUTION: S3

        @PROBLEM_DETAILS_START

        PROBLEM: Longest Consecutive Sequence

        URL: https://neetcode.io/problems/longest-consecutive-sequence/question?list=blind75

        DIFFICULTY: Medium

        PROBLEM DETAILS:

        Given an array of integers nums, return the length of the longest
        consecutive sequence of elements that can be formed.

        A consecutive sequence is a sequence of elements in which each element
        is exactly 1 greater than the previous element. The elements do not
        have to be consecutive in the original array.

        You must write an algorithm that runs in O(n) time.

        Example 1:

        Input:
        nums = [2,20,4,10,3,4,5]

        Output:
        4

        Explanation:
        The longest consecutive sequence is [2, 3, 4, 5].

        Example 2:

        Input:
        nums = [0,3,2,5,4,6,1,1]

        Output:
        7

        Constraints:

        - 0 <= nums.length <= 100,000
        - -10^9 <= nums[i] <= 10^9

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Brute Force

        INT:

        Convert nums to a set for membership checks, but still start a forward
        streak search from every original number. This repeats work for numbers
        belonging to the same sequence.

        ALGO:

        1. Build a set of nums.
        2. For each num in the original list, start curr = num.
        3. While curr exists in the set, increase streak and curr.
        4. Track the largest streak.

        TIME: O(n^2)

        Overlapping sequences can be rescanned many times.

        SPACE: O(n)

        The set stores the distinct input values.


        [S2]-Sorting

        INT:

        Sort the numbers so consecutive values sit next to one another.
        Duplicates are skipped while gaps reset the current streak.

        ALGO:

        1. Return 0 for empty input.
        2. Sort nums.
        3. Track the expected current value and streak length.
        4. Skip duplicates.
        5. Extend while consecutive values continue; reset after a gap.

        TIME: O(n log n)

        Sorting dominates the scan.

        SPACE: O(1) or O(n)

        Extra space depends on the language/runtime sorting implementation.


        [S3]-Hash Set

        INT:

        Only begin counting when num is the first value of a sequence, meaning
        num - 1 is absent from the set. Then extend forward as long as each
        next value exists. This prevents recounting the same sequence from
        every member.

        ALGO:

        1. Convert nums to a set.
        2. Initialize longest = 0.
        3. For each num in the set, test whether num - 1 is absent.
        4. If it is a sequence start, grow length while num + length exists.
        5. Update longest.

        TIME: O(n)

        Each sequence is expanded only from its start, giving linear expected
        work with average O(1) set membership.

        SPACE: O(n)

        The set stores distinct values.


        [S4]-Hash Map Boundary Merging

        INT:

        For each unseen value, read the sequence lengths immediately to its
        left and right, merge them with the new value, and write the merged
        length to the sequence boundaries.

        ALGO:

        1. Maintain a map from selected values/boundaries to sequence lengths.
        2. Skip a number already represented in the map.
        3. Compute length = left_length + right_length + 1.
        4. Store that length at the new value.
        5. Update the left and right boundary positions to the merged length.
        6. Track the maximum.

        TIME: O(n)

        Each input value is processed with average O(1) hash-map operations.

        SPACE: O(n)

        The hash map can grow linearly.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Start a set-based forward scan from every number.
        - Time: O(n^2)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Simple membership-based logic.
        - Main disadvantage: Recounts overlapping sequences.

        S2:

        - Approach: Sort then scan consecutive values.
        - Time: O(n log n)
        - Space: O(1) or O(n)
        - Input modified: Yes
        - Main advantage: Easy ordered scan.
        - Main disadvantage: Does not meet the required O(n) runtime.

        S3:

        - Approach: Expand only from sequence starts using a set.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Directly meets the required linear runtime.
        - Main disadvantage: Requires O(n) hash-set space.

        S4:

        - Approach: Merge neighboring sequence lengths in a hash map.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Also achieves expected linear time.
        - Main disadvantage: More bookkeeping than the start-detection set
          approach.

        [COMMON_PITFALLS]

        - Starting a streak from every number can degrade to O(n^2).
        - Duplicates should not cause repeated sequence work; iterating over a
          set naturally removes them.
        - Empty input must return 0.

        [SOURCE_NOTES]

        - Active submitted implementation uses S3 because it directly satisfies
          the O(n) requirement with the simpler sequence-start invariant.
        - S4 is retained as an alternate expected-O(n) approach.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        numSet = set(nums)
        longest = 0

        for num in numSet:
            if (num - 1) not in numSet:
                length = 1
                while (num + length) in numSet:
                    length += 1
                longest = max(length, longest)
        return longest

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Brute Force
        #
        # res = 0
        # store = set(nums)
        #
        # for num in nums:
        #     streak, curr = 0, num
        #     while curr in store:
        #         streak += 1
        #         curr += 1
        #     res = max(res, streak)
        # return res
        #
        #
        # S2 CODE - Sorting
        #
        # if not nums:
        #     return 0
        # res = 0
        # nums.sort()
        #
        # curr, streak = nums[0], 0
        # i = 0
        # while i < len(nums):
        #     if curr != nums[i]:
        #         curr = nums[i]
        #         streak = 0
        #     while i < len(nums) and nums[i] == curr:
        #         i += 1
        #     streak += 1
        #     curr += 1
        #     res = max(res, streak)
        # return res
        #
        #
        # S4 CODE - Hash Map Boundary Merging
        #
        # mp = defaultdict(int)
        # res = 0
        #
        # for num in nums:
        #     if not mp[num]:
        #         mp[num] = mp[num - 1] + mp[num + 1] + 1
        #         mp[num - mp[num - 1]] = mp[num]
        #         mp[num + mp[num + 1]] = mp[num]
        #         res = max(res, mp[num])
        # return res