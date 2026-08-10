from typing import List


class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        """
        @NC250_START

        TYPE: INTERVIEW_REFERENCE
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

        [STEP_1_UNDERSTAND_THE_PROBLEM]
        We are given an integer array 'nums' of length 'n'.
        Our goal is to construct and return a new array 'ans' of length '2n'.
        The first 'n' elements of 'ans' must be identical to 'nums'.
        The next 'n' elements of 'ans' must also be identical to 'nums'.
        This means 'ans' is simply the array 'nums' concatenated with itself.
        The task is straightforward, but we want to implement it in the most clean and efficient way possible, minimizing redundant passes or dynamic array resizing overhead.

        [STEP_2_RESTATE_THE_PROBLEM]
        "Given an array of integers, I need to return a new array that is twice as long, containing the original array's elements repeated twice in the exact same order."

        [STEP_3_CLARIFY_AND_CONFIRM]
        - Question: Can the input array 'nums' be empty?
          Why it matters: If 'nums' can be empty, we need to ensure our initialization and loop logic do not cause errors.
          What the statement establishes: The problem statement does not explicitly forbid empty arrays, but typically 'nums' has at least one element. If empty, returning an empty array is correct.
        - Question: Is input mutation permitted?
          Why it matters: It is important to know if we should modify the input or return a new array.
          What the statement establishes: The problem asks us to return a new array 'ans', so we do not need to mutate 'nums'.
        - Question: Are there any explicit memory limits?
          Why it matters: Helps determine if we need to optimize for memory beyond standard limits.
          What the statement establishes: No explicit memory limit is specified.

        [STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
        - Input: 'nums', a list of integers.
        - Output: 'ans', a list of integers of length '2 * len(nums)'.
        - Constraints:
          - 'nums' contains integers.
          - The returned array must contain the original sequence twice, in the same order.
        - Edge Cases:
          - Single-element array (e.g., nums = [1] -> ans = [1, 1]).
          - Array with duplicate elements (e.g., nums = [2, 2] -> ans = [2, 2, 2, 2]).

        [STEP_5_BASELINE_APPROACH]
        The baseline approach is S1 (Iteration - Two Pass).
        - Core Idea: Build a new result list by iterating through 'nums' twice. During the first pass, append every value from 'nums'. During the second pass, append every value again.
        - Why it works: This directly creates 'nums' followed by 'nums'.
        - Why it is a natural starting point: It is highly intuitive because it mirrors the literal definition of "concatenating an array with itself" by performing the copy operation twice sequentially.

        [STEP_6_BASELINE_COMPLEXITY]
        - Time Complexity: O(n), where n is the length of the input array 'nums'. We traverse all n elements twice, resulting in O(n) + O(n) = O(n) total operations.
        - Space Complexity: O(1) auxiliary space. The output array itself takes O(n) space to store 2n elements.

        [STEP_7_FIND_THE_BOTTLENECK]
        The baseline approach (S1) has two minor inefficiencies:
        1. It performs two separate, explicit passes over the input array 'nums'.
        2. If implemented using dynamic array appends (like list.append() in Python), the underlying array may undergo multiple dynamic resizing and copying operations as it grows.

        [STEP_8_OPTIMIZATION_BRIDGE]
        To resolve these inefficiencies, we can preallocate the output array 'ans' to its final size of '2n' immediately.
        Since we know the exact destination index for each element in both the first and second halves of the output array, we can write each element to both of its final positions ('i' and 'i + n') during a single traversal of 'nums'.
        This avoids dynamic resizing overhead and reduces the input traversal to a single pass.

        [STEP_9_PREFERRED_APPROACH]
        The preferred approach is S2 (Iteration - Preallocated Output).
        - Central Idea: Preallocate the output array of size '2n'. Iterate through 'nums' once, and for each element at index 'i', place it at 'ans[i]' and 'ans[i + n]'.
        - Steps:
          1. Let 'n' be the length of 'nums'.
          2. Allocate 'ans' with length '2n'.
          3. Iterate through 'nums' with both index 'i' and value 'num'.
          4. Store 'num' at 'ans[i]'.
          5. Store the same 'num' at 'ans[i + n]'.
          6. Return 'ans'.

        [STEP_10_CORRECTNESS_REASONING]
        - Invariant: For any index 'i' in the range 0 <= i < n, the element 'nums[i]' is correctly placed at 'ans[i]' (the first half) and 'ans[i + n]' (the second half).
        - Since we iterate through all indices from 0 to n - 1, every element is copied to both required positions.
        - The final array 'ans' has length '2n' and contains the exact sequence of 'nums' twice in the correct order.
        - This guarantees that the output is correct upon termination.

        [STEP_11_EXAMPLE_TRACE]
        Custom teaching example:
        - Input: nums = [1, 3, 2]
        - Expected Output: [1, 3, 2, 1, 3, 2]

        Trace:
        1. n = 3
        2. ans = [0, 0, 0, 0, 0, 0] (preallocated)
        3. Loop iterations:
           - i = 0, num = 1:
             ans[0] = 1
             ans[0 + 3] = ans[3] = 1
             Current ans: [1, 0, 0, 1, 0, 0]
           - i = 1, num = 3:
             ans[1] = 3
             ans[1 + 3] = ans[4] = 3
             Current ans: [1, 3, 0, 1, 3, 0]
           - i = 2, num = 2:
             ans[2] = 2
             ans[2 + 3] = ans[5] = 2
             Current ans: [1, 3, 2, 1, 3, 2]
        4. Return ans: [1, 3, 2, 1, 3, 2]

        [STEP_12_CODE_PLAN]
        1. Determine the length 'n' of the input list 'nums'.
        2. Preallocate a list 'ans' of size '2 * n' filled with placeholder values (e.g., 0).
        3. Use a loop with 'enumerate(nums)' to access each index 'i' and value 'num' in 'nums'.
        4. Assign 'ans[i] = num' to fill the first half.
        5. Assign 'ans[i + n] = num' to fill the second half.
        6. Return the populated 'ans' list.

        [STEP_13_IMPLEMENTATION]
        The implementation uses Python's list preallocation `[0] * (2 * n)` which is highly efficient because it allocates the exact block of memory needed upfront.
        Using `enumerate(nums)` allows us to retrieve both the index and the value in a single step, keeping the code clean and readable.
        The assignments are direct index lookups, which run in O(1) time.

        [STEP_14_TEST_CASES]
        - Test Case 1 (Representative Case):
          Input: nums = [1, 2, 1]
          Expected Output: [1, 2, 1, 1, 2, 1]
          Validation: Verifies standard concatenation with duplicate values in the input.
        - Test Case 2 (Smallest Valid Input):
          Input: nums = [5]
          Expected Output: [5, 5]
          Validation: Verifies boundary case of a single-element array.
        - Test Case 3 (All Identical Elements):
          Input: nums = [2, 2, 2]
          Expected Output: [2, 2, 2, 2, 2, 2]
          Validation: Verifies correct handling when all elements are identical.

        [STEP_15_TIME_COMPLEXITY_DERIVATION]
        - Preallocating the list of size 2n takes O(n) time.
        - The loop processes each of the n input elements exactly once.
        - Inside the loop, each iteration performs constant-time assignments: ans[i] = num and ans[i + n] = num, which take O(1) time.
        - Therefore, the total time complexity is O(n), where n is the length of the input array nums.

        [STEP_16_SPACE_COMPLEXITY_DERIVATION]
        - The auxiliary space is O(1) as we only use a few loop variables (i, num, n) which require constant extra memory.
        - The output array itself takes O(n) space to store 2n elements.
        - Following the canonical solution reference, the headline space complexity is O(1) auxiliary space.

        [STEP_17_APPROACH_TRADEOFFS]
        - S1 (Iteration - Two Pass):
          - Advantage: Very simple and easy to understand.
          - Disadvantage: Performs two explicit passes through nums and relies on dynamic resizing (appending).
        - S2 (Iteration - Preallocated Output):
          - Advantage: Uses one traversal and directly writes each value to its two final positions, avoiding dynamic resizing overhead.
          - Disadvantage: Requires managing indices and preallocating the exact output size.

        [STEP_18_INTERVIEW_COMMUNICATION]
        - Before Coding: Restate the problem, confirm that we need to return a new array of size 2n, and propose the preallocated single-pass approach to avoid dynamic resizing.
        - While Coding: Explain the preallocation step and how the index offset 'i + n' maps to the second half of the array.
        - After Coding: Trace with a simple example and explain the O(n) time and O(1) auxiliary space complexity.

        [INTERVIEW_SCRIPT]
        "To solve this problem, we need to construct a new array of size 2n that contains the elements of the input array repeated twice. A simple approach would be to iterate through the input array twice and append the elements to a new list. However, we can optimize this by preallocating the output array of size 2n immediately. This avoids the overhead of dynamic resizing. Then, we can iterate through the input array just once. For each element at index i, we write it to both ans[i] and ans[i + n]. This populates both halves of the output array in a single pass. The time complexity will be O(n) because we traverse the input array once, and the auxiliary space complexity will be O(1) since we only use a few loop variables."

        [PATTERN_RECOGNITION]
        - Pattern: Array duplication / cyclic indexing.
        - Signals: When a problem asks to repeat an array or simulate a circular array, preallocating or using modulo arithmetic (i % n) is a common pattern.

        [COMMON_PITFALLS]
        - Forgetting that the result must preserve the original order twice.
        - Writing to ans[i + n] with an incorrect offset.
        - Allocating only n output positions instead of 2n.
        - Confusing required output space with auxiliary space.
        - Accidentally modifying nums when the problem only requires returning a new array.

        [FINAL_REVIEW_CHECKLIST]
        - Can I restate the problem?
        - Do I know the input, output, and constraints?
        - Do I know what actually needs clarification?
        - Can I explain the documented baseline or simplest supported starting point?
        - Can I identify its bottleneck or main performance consideration?
        - Can I explain how that leads to the preferred approach?
        - Can I explain why the preferred approach works?
        - Can I explain important variables and update order?
        - Can I trace a small example?
        - Can I identify important edge cases?
        - Can I derive time complexity?
        - Can I derive auxiliary space?
        - Can I state the main tradeoff?
        - Can I communicate the solution naturally before coding?
        - Can I implement it without copying?

        @CONTENT_END

        @NC250_END
        """
        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = num
            ans[i + n] = num

        return ans
