from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        """
@NC250_START

TYPE: INTERVIEW_REFERENCE
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

[STEP_1_UNDERSTAND_THE_PROBLEM]
We are given an array of integers called `nums`. Our goal is to determine if any integer appears more than once in this array. If we find any duplicate value, we should return `True`. If all elements in the array are unique, we should return `False`.

The main challenge is to perform this check efficiently. Since the array can contain up to $10^5$ elements, a naive approach that compares every pair of elements will be too slow. We need a way to remember the elements we have already seen as we scan through the array.

[STEP_2_RESTATE_THE_PROBLEM]
"Given a list of numbers, I need to check if there are any duplicates. If any number appears at least twice, I will return true. If every number in the list is unique, I will return false."

[STEP_3_CLARIFY_AND_CONFIRM]
- **Question**: Can the input array be empty?
  - *Why it matters*: It determines if we need a special base case check.
  - *What the statement establishes*: The constraints state $0 \le \text{nums.length} \le 10^5$, so an empty array is possible.
  - *Safe assumption*: An empty array has no duplicates, so we should return `False`.
- **Question**: Can we modify the input array?
  - *Why it matters*: Some algorithms (like sorting) modify the input array in-place. If the caller expects the original array to remain unchanged, we would need to make a copy first, which uses extra space.
  - *What the statement establishes*: The problem description does not forbid mutation.
  - *Safe assumption*: We can modify it if needed, but a non-destructive approach is preferred if it achieves the same or better performance.
- **Question**: Are there any strict memory limits?
  - *Why it matters*: A hash set uses $O(n)$ extra space, whereas sorting in-place uses $O(1)$ auxiliary space (or $O(n)$ depending on the sorting algorithm).
  - *What the statement establishes*: No explicit memory limits are specified.
  - *Safe assumption*: Standard memory limits apply, and an $O(n)$ space complexity is highly acceptable to achieve optimal time complexity.

[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
- **Input Type**: `nums: List[int]`
- **Output Type**: `bool`
- **Parameter Meaning**: `nums` is the list of integers to check for duplicates.
- **Constraints**:
  - $0 \le \text{nums.length} \le 10^5$
  - $-10^9 \le \text{nums}[i] \le 10^9$
- **Duplicate Behavior**: Any value appearing two or more times triggers a `True` return.
- **Ordering Requirements**: The order of elements in `nums` does not matter.
- **Mutation Behavior**: The preferred solution does not mutate the input array.
- **No-Result Behavior**: If no duplicates exist, return `False`.
- **Edge Cases**:
  - Empty array `[]` -> returns `False`.
  - Single element `[1]` -> returns `False`.
  - Duplicates at the very beginning `[1, 1, 2, 3]` -> should return `True` quickly.
  - Duplicates at the very end `[1, 2, 3, 3]` -> should return `True`.
- **Complexity Variables**: Let $n$ be the length of the `nums` array.

[STEP_5_BASELINE_APPROACH]
The baseline approach is a brute-force search that compares every possible pair of elements.

- **Core Idea**: Check every pair of elements and return `True` if any pair contains equal values.
- **Data Structures**: None (only loop indices).
- **Major Execution Steps**:
  1. Iterate through `nums` with an outer index `i` from `0` to `n - 1`.
  2. For each `i`, start an inner loop with index `j` from `i + 1` to `n - 1`.
  3. Compare `nums[i]` with `nums[j]`.
  4. If they are equal, return `True` immediately.
  5. If the loops finish without finding any duplicates, return `False`.
- **Why it works**: Comparing every possible pair guarantees that any duplicate will eventually be found.
- **Why it is a natural starting point**: It is the most direct implementation of the problem definition and requires no additional data structures.
- **Main Limitation**: It is highly inefficient because it may need to examine every pair in the array, resulting in quadratic time complexity.

[STEP_6_BASELINE_COMPLEXITY]
- **Time Complexity**: $O(n^2)$
  - *Derivation*: In the worst case (when all elements are unique), the nested loops compare every pair of elements. The total number of comparisons is $\frac{n(n - 1)}{2}$, which simplifies to $O(n^2)$.
- **Space Complexity**: $O(1)$
  - *Derivation*: The algorithm only uses loop indices and a constant number of variables. No additional data structures are allocated.

[STEP_7_FIND_THE_BOTTLENECK]
- **Repeated or Expensive Work**: For each element at index `i`, we perform a linear scan of the remaining elements to check for a match.
- **Why it is expensive**: Scanning the remaining elements takes $O(n)$ time. Doing this for each of the $n$ elements leads to $O(n^2)$ total operations.
- **How often it occurs**: It occurs for every element we process until a duplicate is found or the end of the array is reached.
- **Information that could be reused**: We do not remember the elements we have already seen. If we could store previously seen elements in a structure that allows fast lookups, we wouldn't need to scan the rest of the array.
- **What must improve**: We need a way to check if an element has been seen before in $O(1)$ time instead of $O(n)$ time.

[STEP_8_OPTIMIZATION_BRIDGE]
- **What repeated work should be removed**: The linear scan of the remaining elements for each item.
- **What information can be reused, stored, ordered, or discarded**: We can store the elements we have already processed.
- **What technique/data structure enables the change**: A hash set (implemented as `set` in Python) allows us to insert and look up elements in expected $O(1)$ time.
- **Why the change improves performance**: Instead of scanning the rest of the array for each element, we can check if the current element is already in our hash set. This reduces the lookup time from $O(n)$ to expected $O(1)$ per element.
- **What tradeoff it introduces**: It requires $O(n)$ auxiliary space to store the elements in the hash set.
- **Why the tradeoff is acceptable**: Trading memory for a massive speedup (from quadratic $O(n^2)$ to linear $O(n)$ time) is highly favorable, especially since $n \le 10^5$ easily fits within standard memory limits.

[STEP_9_PREFERRED_APPROACH]
The preferred approach uses a hash set to track encountered values.

- **Canonical Approach Name**: Hash Set
- **Central Idea**: Use a hash set to keep track of values already encountered. While scanning `nums`, if the current value is already in the set, then that value must have appeared earlier, proving a duplicate exists.
- **Data Structure**: Hash Set (`set` in Python).
- **Meaning of Important Variables**:
  - `seen`: A set storing the unique integers encountered so far.
  - `num`: The current integer being processed from `nums`.
- **Initialization**: Initialize `seen` as an empty set.
- **Processing Order**: Iterate through `nums` from left to right.
- **Important Conditions**: For each `num`, check if `num` is in `seen`.
- **State Updates**: If `num` is in `seen`, return `True`. Otherwise, add `num` to `seen`.
- **Early Returns**: Return `True` immediately when a duplicate is found.
- **Termination**: If the loop finishes without finding a duplicate, return `False`.
- **Mutation Behavior**: The input array `nums` is not modified.
- **Main Advantage**: Expected linear-time duplicate detection.
- **Main Tradeoff**: Requires additional memory proportional to the number of distinct values.

[STEP_10_CORRECTNESS_REASONING]
- **Claim**: The algorithm correctly returns `True` if and only if there is at least one duplicate in `nums`.
- **Why it remains true**:
  - We maintain the invariant that `seen` contains all elements from `nums` processed so far.
  - If we encounter an element already in `seen`, it means this element appeared earlier in the array, which is the definition of a duplicate. Thus, returning `True` is correct.
  - If we finish the loop without finding any element already in `seen`, it means every element in `nums` was added to `seen` exactly once. Thus, all elements are unique, and returning `False` is correct.
- **Why no valid result is missed**: We process every element in the array from start to end.
- **Why no invalid result is returned**: We only return `True` when an element is already in `seen`, which guarantees it has appeared at least once before.

[STEP_11_EXAMPLE_TRACE]
Custom teaching example:
- **Input**: `nums = [1, 2, 3, 3]`
- **Expected Output**: `True`
- **Initial State**: `seen = set()`

- **Iteration 1**:
  - `num = 1`
  - Is `1` in `seen`? No.
  - Add `1` to `seen`.
  - State: `seen = {1}`

- **Iteration 2**:
  - `num = 2`
  - Is `2` in `seen`? No.
  - Add `2` to `seen`.
  - State: `seen = {1, 2}`

- **Iteration 3**:
  - `num = 3`
  - Is `3` in `seen`? No.
  - Add `3` to `seen`.
  - State: `seen = {1, 2, 3}`

- **Iteration 4**:
  - `num = 3`
  - Is `3` in `seen`? Yes.
  - Return `True` immediately.

- **Final Result**: `True`

[STEP_12_CODE_PLAN]
- Initialize an empty set named `seen`.
- Loop through each element `num` in the input list `nums`.
- Inside the loop, check if `num` is already present in `seen`.
- If it is, return `True` immediately.
- If it is not, add `num` to `seen` and continue to the next element.
- If the loop completes without finding any duplicates, return `False`.

[STEP_13_IMPLEMENTATION]
- **Mapping**:
  - `seen = set()` initializes the hash set.
  - `for num in nums:` iterates through the array.
  - `if num in seen:` performs the $O(1)$ expected lookup.
  - `seen.add(num)` updates the set.
- **Readability**: The structure is concise, uses standard Python idioms, and has a clear early-exit condition.
- **Python-Specific Behavior**: Python's `set` is implemented as a hash table, providing average $O(1)$ time complexity for both lookups (`in`) and insertions (`add`).
- **Early Returns**: Returns `True` as soon as the first duplicate is detected, avoiding unnecessary processing of the rest of the array.
- **Mutation Behavior**: Does not modify the input list `nums`.

[STEP_14_TEST_CASES]
- **Test Case 1: Representative case with duplicates**
  - *Input*: `nums = [1, 2, 3, 3]`
  - *Expected Output*: `True`
  - *What it validates*: Standard duplicate detection at the end of the array.
- **Test Case 2: Representative case with all unique elements**
  - *Input*: `nums = [1, 2, 3, 4]`
  - *Expected Output*: `False`
  - *What it validates*: Correctly identifies when no duplicates exist.
- **Test Case 3: Empty input**
  - *Input*: `nums = []`
  - *Expected Output*: `False`
  - *What it validates*: Handles the minimum boundary constraint correctly.
- **Test Case 4: Single element**
  - *Input*: `nums = [1]`
  - *Expected Output*: `False`
  - *What it validates*: A single element cannot have duplicates.
- **Test Case 5: Duplicates at the beginning**
  - *Input*: `nums = [1, 1, 2, 3]`
  - *Expected Output*: `True`
  - *What it validates*: Early return works immediately on the second element.

[STEP_15_TIME_COMPLEXITY_DERIVATION]
- **Variables**: Let $n$ be the number of elements in `nums`.
- **Implementation Phases**:
  - Initialization: `seen = set()` takes $O(1)$ time.
  - Iteration: We loop through `nums` at most once, processing each element.
- **Operation Counts and Costs**:
  - For each of the $n$ elements, we perform a lookup (`num in seen`) and potentially an insertion (`seen.add(num)`).
  - In Python, hash set lookups and insertions take expected $O(1)$ time.
- **How Costs Combine**: $n \times O(1) = O(n)$.
- **Simplification**: The overall time complexity is dominated by the loop, which is expected $O(n)$.
- **Qualification**: Expected linear time. In extremely rare pathological cases with severe hash collisions, lookups could degrade to $O(n)$, making the worst-case time $O(n^2)$, but in practice, it is $O(n)$.
- **Final Canonical Complexity**: `TIME: O(n)`

[STEP_16_SPACE_COMPLEXITY_DERIVATION]
- **Fixed-Size Variables**: Loop variable `num` takes $O(1)$ space.
- **Growing Structures**: The `seen` set grows as we encounter unique elements.
- **Maximum Sizes**: In the worst case (all elements are unique), the set will store all $n$ elements.
- **Recursion Depth**: No recursion is used, so stack space is $O(1)$.
- **Temporary Storage**: No other temporary copies or slices are created.
- **Output-Space Treatment**: The output is a single boolean, which takes $O(1)$ space.
- **Mutation Behavior**: The input array is not mutated.
- **Final Auxiliary Complexity**: `SPACE: O(n)`
- **Headline Space Complexity**: `SPACE: O(n)`

[STEP_17_APPROACH_TRADEOFFS]
- **S1 - Brute Force**:
  - *Time*: $O(n^2)$
  - *Space*: $O(1)$
  - *Advantage*: No extra memory required, very simple.
  - *Disadvantage*: Extremely slow for large inputs.
- **S2 - Sorting**:
  - *Time*: $O(n \log n)$
  - *Space*: $O(n)$ (due to Timsort's temporary storage in Python)
  - *Advantage*: Avoids the $O(n^2)$ bottleneck without needing a hash set.
  - *Disadvantage*: Modifies the input array (or requires extra space to copy it) and is slower than the hash set approach.
- **S3 - Hash Set (Preferred)**:
  - *Time*: $O(n)$
  - *Space*: $O(n)$
  - *Advantage*: Fastest expected runtime (linear time).
  - *Disadvantage*: Requires extra memory proportional to the number of unique elements.

**Why the preferred approach is chosen**:
The hash set approach provides the optimal time complexity of $O(n)$ by trading a reasonable amount of memory ($O(n)$ space). In most interview scenarios, optimizing time complexity is prioritized over space complexity, making S3 the best choice.

[STEP_18_INTERVIEW_COMMUNICATION]
- **Before Coding**:
  - Restate the problem to ensure alignment.
  - Confirm constraints (e.g., empty array behavior, memory limits).
  - Mention the brute-force $O(n^2)$ approach briefly to establish a baseline.
  - Propose the $O(n)$ hash set approach as the optimal solution.
- **While Coding**:
  - Explain the purpose of the `seen` set.
  - Explain why the lookup `num in seen` is efficient ($O(1)$ expected time).
  - Write clean, readable code with proper indentation.
- **After Coding**:
  - Walk through a simple test case to verify correctness.
  - State and derive the time and space complexities clearly.
  - Discuss the tradeoffs (e.g., time vs. space compared to sorting).

[INTERVIEW_SCRIPT]
"To solve this problem, I'll start by restating it: we want to find if any integer in the array `nums` appears more than once.

A simple brute-force approach would be to compare every pair of elements using nested loops. This would take $O(n^2)$ time and $O(1)$ space. We can do much better.

Another option is to sort the array first, which takes $O(n \log n)$ time, and then check adjacent elements. This is better but still not optimal.

The most efficient approach is to use a hash set to keep track of the numbers we've already seen. As we iterate through the array, we check if the current number is already in our set. If it is, we've found a duplicate and can return `True` immediately. If we finish the loop without finding any duplicates, we return `False`.

This hash set approach runs in expected $O(n)$ time because set lookups and insertions are $O(1)$ on average. It uses $O(n)$ auxiliary space to store the elements in the set.

Let's write the code for this."

[PATTERN_RECOGNITION]
- **Main Pattern**: Using a Hash Set for tracking seen elements.
- **Statement Signals**: "return true if any value appears more than once", "find duplicates", "check if an element has been seen before".
- **Why those signals suggest the technique**: A hash set provides $O(1)$ average-time lookups, making it the perfect tool for checking membership or existence of previously processed elements.
- **Common Relevant Data Structures**: Hash Set (`set`), Hash Map (`dict`).
- **Common Variations**: Finding the first duplicate, counting frequencies of elements, finding all duplicates.
- **False-Positive Signals**: If the problem requires finding duplicates within a specific distance (e.g., Contains Duplicate II), a simple set is not enough; we need a sliding window or a hash map to store indices. If we cannot use extra space at all, we must use sorting or in-place modification.

[COMMON_PITFALLS]
- Adding the element to the set before checking if it is already present (this would make the check always return `True`).
- Returning `False` inside the loop too early (before checking all elements).
- Assuming hash set operations are guaranteed $O(1)$ in the worst case (they are expected $O(1)$ due to potential hash collisions).
- Forgetting that sorting-based approaches modify the input array, which might be an undesired side effect.

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
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
