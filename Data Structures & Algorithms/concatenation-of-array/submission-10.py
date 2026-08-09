from typing import List


class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: [OPTIONAL]

        @PROBLEM_DETAILS_START

        PROBLEM: Concatenation of Array

        URL: https://neetcode.io/problems/concatenation-of-array/solution

        DIFFICULTY: Easy

        PROBLEM DETAILS:

        Given an integer array nums of length n, create an array ans of
        length 2n where:

        - ans[i] == nums[i]
        - ans[i + n] == nums[i]

        for 0 <= i < n.

        In other words, ans is the concatenation of nums with itself.

        Example 1:

        Input:
        nums = [1, 2, 1]

        Output:
        [1, 2, 1, 1, 2, 1]

        Explanation:

        The result is formed by placing nums immediately after itself.

        Example 2:

        Input:
        nums = [1, 3, 2, 1]

        Output:
        [1, 3, 2, 1, 1, 3, 2, 1]

        Constraints:

        - nums contains integers.
        - The returned array must contain the original sequence twice,
          in the same order.

        @PROBLEM_DETAILS_END

        @CONTENT_START


        [S1]-[Iteration - Two Pass]

        INT:

        Build a new result list by iterating through nums twice.

        During the first pass, append every value from nums.
        During the second pass, append every value again.

        This directly creates nums followed by nums.


        ALGO:

        1. Create an empty result list.
        2. Repeat the traversal of nums two times.
        3. During each traversal, append every element to the result list.
        4. Return the completed result list.


        TIME: O(n)

        We traverse all n elements twice.

        The total work is:

        O(n) + O(n) = O(2n) = O(n)


        SPACE: O(n)

        The returned result contains 2n elements.

        Auxiliary working space outside the required output is constant,
        but the constructed result itself requires O(n) space.



        [S2]-[Iteration - Preallocated Output]

        INT:

        Since the final result always has exactly 2n elements, allocate the
        full output list immediately.

        For every nums[i], place the value in two positions:

        - ans[i]
        - ans[i + n]

        This fills both copies of nums during a single traversal.


        ALGO:

        1. Let n be the length of nums.
        2. Allocate ans with length 2n.
        3. Iterate through nums with both index i and value num.
        4. Store num at ans[i].
        5. Store the same num at ans[i + n].
        6. Return ans.


        TIME: O(n)

        The loop processes each of the n input elements exactly once.

        Each iteration performs constant-time assignments.

        Therefore the total time complexity is O(n).


        SPACE: O(n)

        The returned result contains 2n elements.

        Auxiliary working space besides the required output is O(1),
        while the output itself requires O(n) space.



        [APPROACH_COMPARISON]

        S1:

        - Approach: Iterate through nums twice and append each element.
        - Time: O(n)
        - Space: O(n) including the required output.
        - Main advantage: Very simple and easy to understand.
        - Main disadvantage: Performs two explicit passes through nums.

        S2:

        - Approach: Preallocate the final 2n output and fill both halves
          during one traversal.
        - Time: O(n)
        - Space: O(n) including the required output.
        - Main advantage: Uses one traversal and directly writes each value
          to its two final positions.
        - Main disadvantage: Requires managing indices and preallocating the
          exact output size.



        [COMMON_PITFALLS]

        - Forgetting that the result must preserve the original order twice.
        - Writing to ans[i + n] with an incorrect offset.
        - Allocating only n output positions instead of 2n.
        - Confusing required output space with auxiliary space.
        - Accidentally modifying nums when the problem only requires returning
          a new array.



        [SOURCE_NOTES]

        The active submitted implementation uses the preallocated-output
        approach.

        A simpler alternate implementation is to append every element during
        two passes.

        Prompt 1 may reconcile the approach comparison, complexity wording,
        preferred solution, and any remaining documentation details from the
        actual implementations.


        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = num
            ans[i + n] = num

        return ans

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Iteration (Two Pass)
        #
        # ans = []
        #
        # for _ in range(2):
        #     for num in nums:
        #         ans.append(num)
        #
        # return ans