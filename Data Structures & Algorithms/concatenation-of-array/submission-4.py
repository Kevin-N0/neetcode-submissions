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

        You are given an integer array nums of length n. Create an array ans
        of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for
        0 <= i < n (0-indexed).

        Specifically, ans is the concatenation of two nums arrays.

        Return the array ans.

        Example 1:

        Input: nums = [1,4,1,2]
        Output: [1,4,1,2,1,4,1,2]

        Example 2:

        Input: nums = [22,21,20,1]
        Output: [22,21,20,1,22,21,20,1]

        Constraints:

        1 <= nums.length <= 1000
        1 <= nums[i] <= 1000

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Iteration (Two Pass)

        INT:
        To concatenate an array with itself, create a new result list that
        contains every element of nums twice while maintaining the original
        order. The first pass appends the original sequence, and the second
        pass appends that same sequence again.

        For example, if nums = [1, 2, 3]:
        - The first pass appends [1, 2, 3].
        - The second pass appends [1, 2, 3].
        - The result is [1, 2, 3, 1, 2, 3].

        This approach is simple and directly models concatenating nums with
        itself, but it iterates over nums twice.

        ALGO:
        1. Initialize an empty result list ans.
        2. Run an outer loop twice.
        3. During each pass, iterate through every num in nums.
        4. Append each num to ans.
        5. Return ans after both passes are complete.

        TIME: O(n)

        1. Let n be the length of nums.
        2. The outer loop runs exactly 2 times.
        3. During each outer-loop iteration, the algorithm visits all n
           elements of nums.
        4. Each list append is amortized O(1).
        5. The total work is 2 * n amortized constant-time appends.
        6. After removing the constant factor, the time complexity is O(n).
        7. Therefore, the amortized time complexity is O(n).

        SPACE: O(1) auxiliary space, O(n) required output space

        1. The algorithm uses the result list ans and fixed loop variables.
        2. ans grows to contain 2n elements, so the required output uses O(n)
           space.
        3. No additional data structure grows with the input.
        4. There is no recursion stack.
        5. The remaining loop variables use O(1) space.
        6. Required output space is excluded from auxiliary space.
        7. The input is not modified.
        8. Therefore, the auxiliary-space complexity is O(1).

        [S2]-Iteration (One Pass)

        INT:
        The problem defines the result so that ans[i] == nums[i] and
        ans[i + n] == nums[i] for every valid index i. Instead of iterating
        through nums twice, allocate the complete result array first and fill
        both required positions for each element during one pass.

        This directly uses the index mapping i and i + n. It still performs
        the necessary 2n writes, but requires only one traversal of nums.

        ALGO:
        1. Determine n, the length of nums.
        2. Initialize ans as a list of size 2n.
        3. Iterate through nums with both index i and value num.
        4. Set ans[i] to num.
        5. Set ans[i + n] to the same num.
        6. Return ans after every input element has been processed.

        TIME: O(n)

        1. Let n be the length of nums.
        2. Creating [0] * (2 * n) initializes 2n list elements, which costs
           O(n).
        3. The loop visits each of the n input elements exactly once.
        4. Each iteration performs two constant-time indexed list assignments.
        5. The initialization and loop are sequential, giving O(n) + O(n).
        6. After simplifying, the dominant term is O(n).
        7. Therefore, the worst-case time complexity is O(n).

        SPACE: O(1) auxiliary space, O(n) required output space

        1. The algorithm uses the result list ans, n, i, and num.
        2. ans contains 2n elements, so the required output uses O(n) space.
        3. No additional data structure grows with the input.
        4. There is no recursion stack.
        5. The remaining variables use O(1) space.
        6. Required output space is excluded from auxiliary space.
        7. The input is not modified.
        8. Therefore, the auxiliary-space complexity is O(1).

        [APPROACH_COMPARISON]

        S1:
        - Approach: Iteration (Two Pass)
        - Time: O(n)
        - Time qualification: Amortized
        - Space: O(1) auxiliary space, O(n) required output space
        - Input modified: No
        - Main advantage: Simple and directly models appending nums twice.
        - Main disadvantage: Traverses the input twice.

        S2:
        - Approach: Iteration (One Pass)
        - Time: O(n)
        - Time qualification: Worst-case
        - Space: O(1) auxiliary space, O(n) required output space
        - Input modified: No
        - Main advantage: Fills both halves of the result during one traversal.
        - Main disadvantage: Requires preallocating the result and correctly
          calculating the i + n offset.

        [COMMON_PITFALLS]

        1. Incorrect result array size:
           Allocating an array of size n instead of 2n does not provide enough
           space for the second copy of nums.

        2. Off-by-one error with the index offset:
           In the one-pass approach, the second occurrence of nums[i] must be
           written to ans[i + n]. Using the wrong offset places elements in
           incorrect positions or accesses an invalid index.

        3. Forgetting both copies:
           The returned list must contain every element of nums twice in the
           same order, producing exactly 2n elements.

        @CONTENT_END
        @NC250_END
        """

        # S1 CODE - Iteration (Two Pass):
        # ans = []
        # for i in range(2):
        #     for num in nums:
        #         ans.append(num)
        # return ans

        # S2 CODE - Iteration (One Pass):
        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = ans[i + n] = num

        return ans