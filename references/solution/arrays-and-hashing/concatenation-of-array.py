from typing import List


class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        """
        @NC250_START

        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S2

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
        Build a new result list by iterating through nums twice. During the first pass, append every value from nums. During the second pass, append every value again. This directly creates nums followed by nums.

        ALGO:
        1. Create an empty result list.
        2. Repeat the traversal of nums two times.
        3. During each traversal, append every element to the result list.
        4. Return the completed result list.

        TIME: O(n)
        We traverse all n elements twice. The total work is O(n) + O(n) = O(n), where n is the length of the input array nums.

        SPACE: O(1)
        Auxiliary space is O(1) as we only use a few loop variables. The output array itself takes O(n) space to store 2n elements.


        [S2]-[Iteration - Preallocated Output]

        INT:
        Since the final result always has exactly 2n elements, allocate the full output list immediately. For every nums[i], place the value in two positions: ans[i] and ans[i + n]. This fills both copies of nums during a single traversal.

        ALGO:
        1. Let n be the length of nums.
        2. Allocate ans with length 2n.
        3. Iterate through nums with both index i and value num.
        4. Store num at ans[i].
        5. Store the same num at ans[i + n].
        6. Return ans.

        TIME: O(n)
        The loop processes each of the n input elements exactly once. Each iteration performs constant-time assignments. Therefore, the total time complexity is O(n), where n is the length of the input array nums.

        SPACE: O(1)
        Auxiliary space is O(1) as we only use a few loop variables. The output array itself takes O(n) space to store 2n elements.


        [APPROACH_COMPARISON]

        - Approach: S1 - Iteration - Two Pass
          Time: O(n)
          Time qualification: n is the length of nums
          Space: O(1)
          Input modified: No
          Main advantage: Very simple and easy to understand.
          Main disadvantage: Performs two explicit passes through nums.

        - Approach: S2 - Iteration - Preallocated Output
          Time: O(n)
          Time qualification: n is the length of nums
          Space: O(1)
          Input modified: No
          Main advantage: Uses one traversal and directly writes each value to its two final positions.
          Main disadvantage: Requires managing indices and preallocating the exact output size.


        [COMMON_PITFALLS]

        - Forgetting that the result must preserve the original order twice.
        - Writing to ans[i + n] with an incorrect offset.
        - Allocating only n output positions instead of 2n.
        - Confusing required output space with auxiliary space.
        - Accidentally modifying nums when the problem only requires returning a new array.

        @CONTENT_END

        @NC250_END
        """

        # S2 is the preferred solution
        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = num
            ans[i + n] = num

        return ans

        # S1 CODE - Iteration (Two Pass)
        # ans = []
        # for _ in range(2):
        #     for num in nums:
        #         ans.append(num)
        # return ans
