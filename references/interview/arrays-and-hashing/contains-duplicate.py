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
        - We are given an array of integers called `nums`.
        - Our goal is to determine if any integer appears at least twice in this array.
        - If we find any duplicate value, we must return `True`.
        - If all elements in the array are completely unique, we must return `False`.
        - The problem is nontrivial because the array can contain up to 100,000 elements. A naive search that compares every element to every other element will be too slow. We need an efficient way to track elements we have already seen.

        [STEP_2_RESTATE_THE_PROBLEM]
        "Given an array of numbers, I need to check if there are any duplicates. If any number appears more than once, I should return true. If every number in the array is unique, I should return false."

        [STEP_3_CLARIFY_AND_CONFIRM]
        - **Question**: Can the input array be empty?
          - *Why it matters*: It determines if we need an explicit base case check for length 0.
          - *What the statement establishes*: The constraints state `0 <= nums.length <= 10^5`.
          - *Safe assumption*: An empty array has no duplicates, so we should return `False`.
        - **Question**: Can we modify the input array?
          - *Why it matters*: If we can modify the array, we can sort it in-place to save memory. If we cannot modify it, we must either copy it or use an approach that does not alter the input.
          - *Safe assumption*: In a real interview, always ask before mutating input. If mutation is allowed, sorting is a viable alternative.
        - **Question**: Are there any strict memory limits?
          - *Why it matters*: It helps us choose between an $O(1)$ auxiliary space approach (like sorting or brute force) and an $O(n)$ space approach (like using a hash set).

        [STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
        - **Input**: `nums: List[int]` (an array of integers).
        - **Output**: `bool` (`True` if duplicates exist, `False` otherwise).
        - **Constraints**:
          - Array length: $0 \le \text{len}(nums) \le 10^5$.
          - Element values: $-10^9 \le nums[i] \le 10^9$.
        - **Duplicate Behavior**: Any element appearing 2 or more times triggers a `True` return.
        - **Ordering**: The input array is unsorted.
        - **Mutation**: Not required, but possible depending on the approach.
        - **No-Result Behavior**: An empty array or an array with all unique elements returns `False`.

        [STEP_5_BASELINE_APPROACH]
        - **Core Idea**: The simplest way to find a duplicate is to compare every possible pair of elements in the array. If any pair contains the same value, we have found a duplicate.
        - **Data Structures**: None (only loop indices).
        - **Major Execution Steps**:
          1. Use an outer loop with index `i` from `0` to `len(nums) - 1`.
          2. Use an inner loop with index `j` from `i + 1` to `len(nums) - 1`.
          3. Compare `nums[i]` with `nums[j]`.
          4. If they are equal, return `True`.
          5. If both loops finish without finding any equal pair, return `False`.
        - **Why it works**: It exhaustively checks all possible pairs of elements.
        - **Why it is a natural starting point**: It requires no extra memory and directly implements the definition of a duplicate.
        - **Main Limitation**: It is extremely slow for large arrays because it performs quadratic work.

        [STEP_6_BASELINE_COMPLEXITY]
        - **Time Complexity**: $O(n^2)$ where $n$ is the length of `nums`.
          - *Derivation*: The outer loop runs $n$ times. For each index `i`, the inner loop runs from `i + 1` to $n$. The total number of comparisons is $(n - 1) + (n - 2) + \dots + 1 = \frac{n(n - 1)}{2}$, which simplifies to $O(n^2)$.
        - **Space Complexity**: $O(1)$ auxiliary space.
          - *Derivation*: Only a constant number of variables (`i`, `j`) are used to keep track of indices. No additional data structures are allocated.

        [STEP_7_FIND_THE_BOTTLENECK]
        - The brute-force approach is slow because it repeatedly scans the array to look for matches. For each element, it searches the rest of the array from scratch, forgetting all the elements it has already seen.
        - This "forgetfulness" forces us to perform $O(n^2)$ comparisons. If we could remember the elements we have already seen in a single pass, we wouldn't need to compare every pair.

        [STEP_8_OPTIMIZATION_BRIDGE]
        - To eliminate the $O(n^2)$ bottleneck, we need a way to check if an element has been seen before in $O(1)$ time.
        - A hash set is the perfect data structure for this. It allows us to insert elements and check for membership in expected $O(1)$ time.
        - By trading a small amount of memory ($O(n)$ space to store the seen elements) for speed, we can reduce the time complexity from $O(n^2)$ to $O(n)$.

        [STEP_9_PREFERRED_APPROACH]
        - **Name**: Hash Set Lookup.
        - **Central Idea**: Maintain a set of all numbers encountered so far. As we iterate through the array, check if the current number is already in the set.
        - **Data Structure**: Python `set` (hash set).
        - **Meaning of Variables**:
          - `seen`: A set storing the unique integers we have processed so far.
          - `num`: The current integer being inspected.
        - **Steps**:
          1. Initialize an empty set `seen`.
          2. Loop through each `num` in `nums`.
          3. Check if `num` is in `seen`. If yes, return `True` immediately (duplicate found).
          4. If not, add `num` to `seen`.
          5. If the loop completes without finding any duplicates, return `False`.

        [STEP_10_CORRECTNESS_REASONING]
        - **Invariant**: At the start of each iteration for element `num`, the set `seen` contains exactly the elements of `nums` that appeared before `num`.
        - **Claim**: The algorithm returns `True` if and only if there is a duplicate.
        - **Why no valid result is missed**: If a duplicate exists, say at indices `i` and `j` (where `i < j` and `nums[i] == nums[j]`), then when the loop reaches index `j`, `nums[i]` will already have been added to `seen`. The check `nums[j] in seen` will evaluate to `True`, and the algorithm will correctly return `True`.
        - **Why no invalid result is returned**: If all elements are unique, the check `num in seen` will always be `False` because no element has been seen before. The loop will finish, and the algorithm will return `False`.
        - **Termination**: The loop runs at most $n$ times, so it is guaranteed to terminate.

        [STEP_11_EXAMPLE_TRACE]
        - **Input**: `nums = [1, 2, 3, 3]`
        - **Expected Output**: `True`
        - **Trace**:
          - Initial state: `seen = set()`
          - Iteration 1: `num = 1`. Is `1` in `seen`? No. Add `1` to `seen`. `seen = {1}`.
          - Iteration 2: `num = 2`. Is `2` in `seen`? No. Add `2` to `seen`. `seen = {1, 2}`.
          - Iteration 3: `num = 3`. Is `3` in `seen`? No. Add `3` to `seen`. `seen = {1, 2, 3}`.
          - Iteration 4: `num = 3`. Is `3` in `seen`? Yes! Return `True` immediately.
        - **Result**: `True` (correct).

        [STEP_12_CODE_PLAN]
        - **Initialize the hash set**: Create an empty set named `seen`.
        - **Iterate through the input**: Use a `for` loop to iterate through each element `num` in `nums`.
        - **Check membership**: Inside the loop, check if `num` is already in `seen` using the `in` operator.
        - **Early return**: If `num` is in `seen`, return `True` immediately.
        - **Update state**: If `num` is not in `seen`, add it to `seen` using `seen.add(num)`.
        - **Final return**: If the loop completes without returning `True`, return `False`.

        [STEP_13_IMPLEMENTATION]
        - The code is highly readable and direct.
        - Python's `set` is implemented as a hash table, which provides average $O(1)$ time complexity for both lookups (`in`) and insertions (`add`).
        - The early return allows the algorithm to terminate as soon as a duplicate is found, which can be much faster than scanning the entire array in practice.

        [STEP_14_TEST_CASES]
        - **Test 1 (Representative case with duplicates)**:
          - *Input*: `nums = [1, 2, 3, 3]`
          - *Expected Output*: `True`
          - *Validation*: Validates that a duplicate at the end of the array is correctly detected.
        - **Test 2 (Representative case with no duplicates)**:
          - *Input*: `nums = [1, 2, 3, 4]`
          - *Expected Output*: `False`
          - *Validation*: Validates that an array of unique elements returns `False`.
        - **Test 3 (Smallest valid input - empty array)**:
          - *Input*: `nums = []`
          - *Expected Output*: `False`
          - *Validation*: Validates that an empty array is handled correctly without errors.
        - **Test 4 (Single element array)**:
          - *Input*: `nums = [1]`
          - *Expected Output*: `False`
          - *Validation*: Validates that a single element cannot have duplicates.
        - **Test 5 (All elements are duplicates)**:
          - *Input*: `nums = [5, 5, 5, 5]`
          - *Expected Output*: `True`
          - *Validation*: Validates that multiple duplicates are handled correctly and triggers an early return on the second element.

        [STEP_15_TIME_COMPLEXITY_DERIVATION]
        - Let $n$ be the number of elements in `nums`.
        - The algorithm consists of a single loop that iterates through `nums` at most once.
        - In each iteration, we perform two main operations:
          1. A membership check: `num in seen`.
          2. An insertion: `seen.add(num)`.
        - For a hash set, both membership checks and insertions have an expected time complexity of $O(1)$.
        - Therefore, the expected work per element is $O(1)$.
        - Since we process at most $n$ elements, the total expected time complexity is $O(n)$.
        - **TIME: O(n)**

        [STEP_16_SPACE_COMPLEXITY_DERIVATION]
        - The algorithm uses a hash set `seen` to store the elements of `nums`.
        - In the worst case (when all elements in `nums` are unique), the set `seen` will grow to store all $n$ elements.
        - Each element in the set takes $O(1)$ space.
        - Therefore, the auxiliary space complexity is $O(n)$.
        - **SPACE: O(n)**

        [STEP_17_APPROACH_TRADEOFFS]
        - **Brute Force (S1)**:
          - *Time*: $O(n^2)$
          - *Space*: $O(1)$
          - *Advantage*: No extra memory required.
          - *Disadvantage*: Extremely slow for large inputs.
        - **Sorting (S2)**:
          - *Time*: $O(n \log n)$
          - *Space*: $O(n)$ (due to Timsort's auxiliary space in Python) or $O(1)$ if in-place sorting is used and input mutation is allowed.
          - *Advantage*: Better time complexity than brute force, and can be $O(1)$ auxiliary space if we can mutate the input.
          - *Disadvantage*: Modifies the input array (which might not be allowed or desired) and is slower than the hash set approach.
        - **Hash Set (S3)**:
          - *Time*: $O(n)$
          - *Space*: $O(n)$
          - *Advantage*: Fastest expected runtime (linear time).
          - *Disadvantage*: Requires extra memory proportional to the size of the input.
        - **Why S3 is preferred**: In most software engineering scenarios, time is a more critical resource than memory. The transition from $O(n^2)$ or $O(n \log n)$ to $O(n)$ is a massive performance improvement for large datasets, making the $O(n)$ space tradeoff highly acceptable.

        [STEP_18_INTERVIEW_COMMUNICATION]
        - **Before Coding**:
          - Restate the problem to ensure alignment.
          - Ask clarifying questions about constraints, empty inputs, and whether input mutation is allowed.
          - Mention the brute-force $O(n^2)$ approach briefly to establish a baseline, then propose the $O(n)$ hash set approach as the optimal solution.
        - **While Coding**:
          - Explain the purpose of the `seen` set.
          - Walk through the loop and explain the early return condition.
          - Mention that set lookups and insertions are expected $O(1)$ time.
        - **After Coding**:
          - Trace the code with a simple example (e.g., `[1, 2, 3, 3]`).
          - State and derive the time and space complexities clearly.

        [INTERVIEW_SCRIPT]
        "To solve this problem, I'll start by restating it: we want to find if any integer in the array appears more than once. If it does, we return true; otherwise, we return false.

        A simple brute-force approach would be to compare every pair of elements using nested loops. This would take $O(n^2)$ time and $O(1)$ space.

        We can optimize this by using a hash set to keep track of the numbers we've already seen. As we iterate through the array, we check if the current number is in our set. If it is, we've found a duplicate and can return true immediately. If not, we add it to the set and continue.

        This approach is much faster because hash set lookups and insertions take expected $O(1)$ time. Therefore, the overall time complexity will be $O(n)$, and the space complexity will be $O(n)$ to store the elements in the set. Let's write the code for this."

        [PATTERN_RECOGNITION]
        - **Pattern**: Using a Hash Set for tracking seen elements.
        - **Signals**:
          - "Find duplicates", "has any element appeared before", "check uniqueness".
          - Need to find if an element exists in a collection in $O(1)$ time.
        - **Common Variations**: Two Sum (using a hash map to find the complement), First Unique Character in a String.
        - **False-Positive Signals**: If the array is sorted, or if we have strict $O(1)$ space constraints and are allowed to mutate the input, a sorting-based approach or two-pointer approach might be preferred over a hash set.

        [COMMON_PITFALLS]
        - Adding the element to the set *before* checking if it is already in the set (which would make the check always return `True`).
        - Returning `False` inside the loop instead of waiting for the loop to complete.
        - Claiming hash set operations are guaranteed $O(1)$ worst-case (they are expected $O(1)$ due to potential hash collisions).
        - Forgetting that sorting-based approaches modify the input array.

        [FINAL_REVIEW_CHECKLIST]
        - Can I restate the problem clearly?
        - Do I understand the input, output, and constraints?
        - Did I clarify if the input array can be empty or if mutation is allowed?
        - Can I explain the brute-force $O(n^2)$ baseline?
        - Can I identify the bottleneck of the brute-force approach (forgetting seen elements)?
        - Can I explain how a hash set solves this bottleneck?
        - Can I implement the hash set approach from scratch?
        - Did I place the `seen.add(num)` step after the membership check?
        - Can I trace the code with a simple duplicate and non-duplicate example?
        - Can I derive the $O(n)$ time and $O(n)$ space complexities?
        - Can I discuss the tradeoffs between the brute-force, sorting, and hash set approaches?

        @CONTENT_END

        @NC250_END
        """
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
