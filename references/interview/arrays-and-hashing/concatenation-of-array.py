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
- **What is given**: An integer array `nums` of length `n`.
- **What must be returned**: A new array `ans` of length `2n`.
- **The central relationship**: The first half of `ans` (indices `0` to `n-1`) must be identical to `nums`, and the second half of `ans` (indices `n` to `2n-1`) must also be identical to `nums`.
- **What makes it nontrivial**: It is a very straightforward array duplication problem, but we want to do it efficiently. We can either append elements in multiple passes or preallocate the array and fill both halves in a single pass.
- **Vocabulary**: "Concatenation" means joining two sequences end-to-end. Here, we concatenate `nums` with itself.

[STEP_2_RESTATE_THE_PROBLEM]
"We are given an array of integers called `nums`. We need to create and return a new array that is twice as long, containing the elements of `nums` repeated twice in the exact same order. For example, if the input is `[1, 2, 1]`, the output should be `[1, 2, 1, 1, 2, 1]`."

[STEP_3_CLARIFY_AND_CONFIRM]
- **Question**: Can the input array `nums` be empty?
  - **Why it matters**: If `nums` is empty, the output should also be empty.
  - **What the statement establishes**: The constraints don't explicitly forbid empty arrays, but typically `nums` has at least one element. Our code should handle empty arrays naturally.
- **Question**: Should we modify the input array in-place, or return a new array?
  - **Why it matters**: Modifying the input array in-place is a different operation and might not be possible if the array size is fixed.
  - **What the statement establishes**: The problem asks us to "create an array `ans`", which means we should return a new array and leave `nums` unmodified.
- **Question**: What are the types of elements in `nums`?
  - **Why it matters**: Knowing the types helps us understand if we need to perform deep copies or if simple assignment is sufficient.
  - **What the statement establishes**: `nums` contains integers, so simple assignment is perfectly safe and efficient.

[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
- **Input types**: `nums: List[int]`
- **Output type**: `List[int]`
- **Parameter meanings**: `nums` is the input list of integers of length `n`.
- **Supported official constraints**:
  - `nums` contains integers.
  - The returned array must contain the original sequence twice, in the same order.
- **Duplicate behavior**: Duplicates in `nums` are preserved in their original relative order.
- **Ordering requirements**: The order of elements in both halves of the output must match the input.
- **Mutation behavior**: The input array `nums` is not mutated.
- **No-result behavior**: Not applicable, as a concatenation is always possible.
- **Important edge cases**: Single-element array (e.g., `[1]`), empty array (if allowed), or arrays with duplicate elements.
- **Relevant complexity variables**: `n`, the length of the input array `nums`.

[STEP_5_BASELINE_APPROACH]
- **Core idea**: Build a new result list by iterating through `nums` twice. During the first pass, append every value from `nums`. During the second pass, append every value again.
- **Data structures**: A dynamic list `ans` that grows as we append elements.
- **Major execution steps**:
  1. Create an empty list `ans`.
  2. Loop through `nums` and append each element to `ans`.
  3. Loop through `nums` a second time and append each element to `ans` again.
  4. Return `ans`.
- **Why it works**: It directly places the elements of `nums` in the first half, and then places them again in the second half.
- **Why it is a natural starting point**: It is highly intuitive because it mimics the literal definition of "concatenating" by doing it sequentially.
- **Main limitation**: It requires two separate passes over the input array and relies on dynamic array resizing (appending), which can have overhead.

[STEP_6_BASELINE_COMPLEXITY]
- **Time complexity**: O(n). We traverse all `n` elements twice. The total work is O(n) + O(n) = O(2n) = O(n). Each append operation takes O(1) amortized time.
- **Space complexity**: O(n). The returned result contains `2n` elements, which is O(n) space. Auxiliary working space outside the required output is O(1) because we only use a few loop variables.

[STEP_7_FIND_THE_BOTTLENECK]
- The baseline performs two separate passes over the input array.
- It also relies on dynamic resizing of the list as we append elements, which can cause the underlying memory to be reallocated and copied multiple times.
- If we know the final size of the output array is exactly `2n`, we can avoid dynamic resizing overhead and complete the task in a single pass.

[STEP_8_OPTIMIZATION_BRIDGE]
- Instead of dynamically appending elements and traversing the input twice, we can preallocate the output array of size `2n` immediately.
- Since we know the exact destination indices for each element `nums[i]` (which are `i` and `i + n`), we can write to both positions during a single traversal of `nums`.
- This technique (preallocation and single-pass index mapping) eliminates the need for a second pass and avoids any dynamic resizing overhead.

[STEP_9_PREFERRED_APPROACH]
- **Canonical approach name**: Iteration - Preallocated Output
- **Central idea**: Preallocate the full output list of size `2n` and fill both halves simultaneously in a single pass.
- **Data structure**: A preallocated list `ans` of size `2n`.
- **Meaning of important variables**:
  - `n`: length of the input array `nums`.
  - `ans`: the preallocated output list of size `2 * n`.
  - `i`: the current index in the input array `nums`.
  - `num`: the value at `nums[i]`.
- **Initialization**: `ans = [0] * (2 * n)`.
- **Processing order**: Iterate through `nums` from index `0` to `n - 1`.
- **Important conditions**: For each element, write to `ans[i]` and `ans[i + n]`.
- **State updates**: Update the values at indices `i` and `i + n` in `ans`.
- **Early returns**: None.
- **Termination**: The loop terminates after processing all `n` elements.
- **Final return**: Return `ans`.
- **Mutation behavior**: The input array `nums` is not mutated.
- **Main advantage**: Only a single pass is made over the input array, and no dynamic resizing occurs.
- **Main tradeoff**: Requires managing indices and preallocating the exact output size.

[STEP_10_CORRECTNESS_REASONING]
- **Claim**: The returned array `ans` is the concatenation of `nums` with itself.
- **Why it remains true**:
  - The output array `ans` is initialized to size `2n`.
  - For every index `i` in `0 <= i < n`, we assign `ans[i] = nums[i]` and `ans[i + n] = nums[i]`.
  - This guarantees that the first `n` elements of `ans` are identical to `nums`, and the next `n` elements of `ans` are also identical to `nums`.
  - Since every index from `0` to `2n - 1` is filled exactly once, the final array is fully populated and correct.
  - No valid result is missed, and no invalid result is returned.

[STEP_11_EXAMPLE_TRACE]
Custom teaching example:
- **Input**: `nums = [1, 3, 2]`
- **Expected output**: `[1, 3, 2, 1, 3, 2]`
- **Initial state**:
  - `n = 3`
  - `ans = [0, 0, 0, 0, 0, 0]`
- **Iterations**:
  - **Iteration 0**: `i = 0`, `num = 1`.
    - `ans[0] = 1`
    - `ans[0 + 3] = ans[3] = 1`
    - `ans` state: `[1, 0, 0, 1, 0, 0]`
  - **Iteration 1**: `i = 1`, `num = 3`.
    - `ans[1] = 3`
    - `ans[1 + 3] = ans[4] = 3`
    - `ans` state: `[1, 3, 0, 1, 3, 0]`
  - **Iteration 2**: `i = 2`, `num = 2`.
    - `ans[2] = 2`
    - `ans[2 + 3] = ans[5] = 2`
    - `ans` state: `[1, 3, 2, 1, 3, 2]`
- **Return point**: Loop ends. Return `ans` which is `[1, 3, 2, 1, 3, 2]`.

[STEP_12_CODE_PLAN]
1. Find the length of `nums` and store it in `n`.
2. Preallocate the output list `ans` of size `2 * n` with placeholder values (e.g., `0`).
3. Use `enumerate(nums)` to iterate through the input array, obtaining both the index `i` and the value `num`.
4. Inside the loop, assign `num` to `ans[i]` and `ans[i + n]`.
5. After the loop completes, return `ans`.

[STEP_13_IMPLEMENTATION]
- **How major code blocks map to the algorithm**:
  - `n = len(nums)` and `ans = [0] * (2 * n)` handle the initialization and preallocation.
  - The `for i, num in enumerate(nums):` loop handles the single-pass traversal.
  - The assignments `ans[i] = num` and `ans[i + n] = num` map the elements to their correct positions.
- **Why the structure is readable**: It is concise, uses standard Python idioms like `enumerate`, and avoids complex index arithmetic.
- **Python-specific behavior**: `[0] * (2 * n)` is an efficient way to preallocate a list of a specific size in Python.

[STEP_14_TEST_CASES]
- **Test Case 1: Representative Case**
  - **Input**: `nums = [1, 2, 1]`
  - **Expected output**: `[1, 2, 1, 1, 2, 1]`
  - **What it validates**: Standard behavior with duplicates in the input.
- **Test Case 2: Smallest Valid Input**
  - **Input**: `nums = [1]`
  - **Expected output**: `[1, 1]`
  - **What it validates**: Correct behavior with a single-element array.
- **Test Case 3: All Identical Elements**
  - **Input**: `nums = [4, 4, 4]`
  - **Expected output**: `[4, 4, 4, 4, 4, 4]`
  - **What it validates**: Correctness when all elements are identical.

[STEP_15_TIME_COMPLEXITY_DERIVATION]
- Let `n` be the length of the input array `nums`.
- The algorithm consists of two main phases:
  1. Preallocating the list of size `2n`, which takes O(n) time.
  2. Iterating through `nums` once. The loop runs exactly `n` times.
- Inside the loop, we perform two array assignments: `ans[i] = num` and `ans[i + n] = num`. Each assignment is a constant-time O(1) operation.
- The total time is the sum of preallocation and the loop: O(n) + O(n) = O(n).
- Final canonical complexity: O(n).

[STEP_16_SPACE_COMPLEXITY_DERIVATION]
- The output array `ans` requires `2n` elements, which takes O(n) space.
- Auxiliary space (excluding the required output array) is O(1) because we only use a few scalar variables (`n`, `i`, `num`) which require constant space.
- Since the problem requires returning a new array of size `2n`, the total space complexity including the output is O(n).
- Final canonical complexity: O(n).

[STEP_17_APPROACH_TRADEOFFS]
- **S1 (Two Pass)**:
  - **Time**: O(n) (processes each element twice)
  - **Space**: O(n)
  - **Advantage**: Extremely simple, no index arithmetic needed.
  - **Disadvantage**: Performs two explicit passes and relies on dynamic resizing (appending).
- **S2 (Preallocated Output)**:
  - **Time**: O(n) (processes each element once)
  - **Space**: O(n)
  - **Advantage**: Single pass, avoids dynamic resizing overhead.
  - **Disadvantage**: Requires managing indices and preallocating the exact output size.
- **Why S2 is preferred**: It is more efficient in practice because it avoids the overhead of dynamic array resizing and reduces the number of passes over the input array from two to one.

[STEP_18_INTERVIEW_COMMUNICATION]
- **BEFORE CODING**: Restate the problem, confirm that we should return a new array rather than modifying the input in-place, and propose the preallocated single-pass approach as an optimization over the naive two-pass approach.
- **WHILE CODING**: Explain that we are preallocating the array to avoid dynamic resizing overhead, and explain how the index `i + n` maps elements to the second half of the output.
- **AFTER CODING**: Walk through a simple trace to verify that the indices are mapped correctly, and state the O(n) time and O(n) space complexities.

[INTERVIEW_SCRIPT]
"To solve this problem, we need to create a new array that contains the elements of `nums` repeated twice. A simple way to do this would be to iterate through `nums` twice and append each element to a new list. However, we can optimize this by preallocating the output array of size `2n` immediately. This avoids the overhead of dynamic resizing. Then, we can iterate through `nums` just once. For each element at index `i`, we place it at `ans[i]` and also at `ans[i + n]`. This fills both halves of the output array in a single pass. The time complexity will be O(n) because we traverse the input array once, and the space complexity will be O(n) to store the output array."

[PATTERN_RECOGNITION]
- **Pattern**: Array Preallocation / Index Mapping.
- **Signals**: When the output size is a known, fixed function of the input size (e.g., double, triple, or a specific transformation), and elements are mapped to predictable positions.
- **Why those signals suggest the technique**: Preallocating the output array avoids dynamic resizing overhead and allows direct index-based assignments, which is often faster and cleaner.
- **False-positive signals**: If the output size is dynamic or depends on filtering conditions (e.g., "remove all even numbers"), preallocation is harder because the final size is not known beforehand.

[COMMON_PITFALLS]
- Forgetting that the result must preserve the original order twice.
- Writing to `ans[i + n]` with an incorrect offset (e.g., using `i + 1` instead of `i + n`).
- Allocating only `n` output positions instead of `2n`.
- Confusing required output space with auxiliary space.
- Accidentally modifying `nums` when the problem only requires returning a new array.

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
