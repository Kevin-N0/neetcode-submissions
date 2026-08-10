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
We are given an array of integers called nums. Our goal is to determine if there are any duplicate values in this array.
- If any integer appears at least twice, we must return True.
- If every single integer in the array is unique, we must return False.
What makes this problem interesting is balancing the time spent searching for duplicates against the extra memory used to remember the numbers we have already seen.

[STEP_2_RESTATE_THE_PROBLEM]
"Given an array of numbers, I need to check if there are any duplicate values. If any number appears more than once, I should return true. If every number in the array is unique, I should return false."

[STEP_3_CLARIFY_AND_CONFIRM]
- Question: Can the input array be empty?
  - Why it matters: It determines if we need a special base case or if our main loop handles it naturally.
  - What the statement establishes: The constraints state 0 <= nums.length <= 10^5, so the array can be empty. An empty array has no duplicates, so we should return False.
- Question: Is input mutation allowed?
  - Why it matters: If we can sort the array in-place, we can avoid using extra memory, but it modifies the caller's data.
  - What the statement establishes: The statement does not specify whether input mutation is permitted. The preferred implementation does not mutate nums, so no mutation assumption is required.
- Question: Are there any explicit memory limits?
  - Why it matters: It helps us decide whether to prioritize minimizing space (like sorting) or minimizing time (like using a hash set).
  - What the statement establishes: No explicit memory limit is provided.

[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
- Input: nums (a list of integers).
- Output: A boolean value (True if duplicates exist, False otherwise).
- Constraints:
  - Array length: 0 <= nums.length <= 10^5.
  - Element values: -10^9 <= nums[i] <= 10^9.
- Duplicate behavior: Any value appearing more than once triggers a True return.
- Ordering: The input array is not guaranteed to be sorted.
- Mutation: The preferred approach does not mutate the input.
- No-result behavior: If the array is empty or has only 1 element, it cannot contain duplicates, so we return False.

[STEP_5_BASELINE_APPROACH]
The earliest meaningful documented approach is the Brute Force approach (S1).
- Core idea: Compare every possible pair of elements in the array.
- Data structures: None (only loop indices).
- Major execution steps:
  1. Use an outer loop with index i from 0 to n - 1.
  2. Use an inner loop with index j from i + 1 to n - 1.
  3. Compare nums[i] with nums[j].
  4. If they are equal, return True immediately.
  5. If both loops finish without finding a match, return False.
- Why it works: It exhaustively checks every pair, guaranteeing that if a duplicate exists, it will be found.
- Why it is a natural starting point: It requires no extra memory and directly implements the definition of a duplicate.
- Main limitation: It is highly inefficient for large arrays because it performs quadratic comparisons.

[STEP_6_BASELINE_COMPLEXITY]
- Time Complexity: O(n^2)
  - Let n be the number of elements in nums. In the worst case (when all elements are unique), the nested loops compare every pair of elements. The number of comparisons is n(n - 1) / 2, which simplifies to O(n^2).
- Space Complexity: O(1)
  - The algorithm only uses loop indices and a constant number of variables. No additional data structures are allocated.

[STEP_7_FIND_THE_BOTTLENECK]
The bottleneck in the brute-force approach is the repeated scanning of the array to check if the current element has appeared before.
- For each element at index i, we scan all subsequent elements j to see if any match. This results in redundant comparisons.
- We need a way to remember elements we have already seen in expected O(1) time, rather than scanning the rest of the array.

[STEP_8_OPTIMIZATION_BRIDGE]
To eliminate the quadratic time complexity, we need to reduce the lookup time for previously seen elements.
- If we store the elements we have already visited in a data structure that supports fast lookups, we can check for duplicates in a single pass.
- A hash set is ideal for this because it provides expected O(1) time complexity for both insertions and lookups.
- Tradeoff: We trade space for time. We use O(n) auxiliary space to store the elements in the hash set, but we reduce the time complexity from O(n^2) to expected O(n).

[STEP_9_PREFERRED_APPROACH]
The canonical preferred approach is the Hash Set approach (S3).
- Central idea: Maintain a hash set of elements we have already seen. As we iterate through the array, we check if the current element is already in the set.
- Variables: seen (a hash set to store visited integers).
- Steps:
  1. Initialize an empty hash set named seen.
  2. Iterate through each number num in nums.
  3. Check if num is in seen.
  4. If it is, return True immediately (duplicate found).
  5. If not, add num to seen.
  6. If the loop completes without finding any duplicates, return False.
- Mutation: Does not mutate the input array.
- Main advantage: Expected linear time complexity O(n).
- Main tradeoff: Requires O(n) auxiliary space.

[STEP_10_CORRECTNESS_REASONING]
We can prove the correctness of the hash-set approach using a loop invariant.
An invariant is a fact that remains true throughout the algorithm.
- Invariant: At the start of each iteration for index i, the set seen contains all elements from nums[0...i-1], and no duplicates exist in this prefix.
- Initialization: Before the first iteration (i = 0), seen is empty. The prefix nums[0...-1] is empty, so it contains no duplicates. The invariant holds.
- Maintenance: During the iteration for nums[i], we check if nums[i] is in seen.
  - If nums[i] is in seen, then nums[i] appeared in nums[0...i-1]. We have found a duplicate and return True. This is correct.
  - If nums[i] is not in seen, we add it to seen. The set now contains all elements from nums[0...i], and since we did not return True, no duplicates exist in nums[0...i]. The invariant holds for the next iteration.
- Termination: If the loop completes, we have processed all elements without returning True. By the invariant, the entire array contains no duplicates, so returning False is correct. No valid duplicate can be missed because every element is checked against all preceding elements stored in seen.

[STEP_11_EXAMPLE_TRACE]
Custom teaching example: nums = [1, 2, 3, 2]
- Initial state: seen = set()
- Iteration 1: num = 1
  - Is 1 in seen? No.
  - Add 1 to seen.
  - State: seen = {1}
- Iteration 2: num = 2
  - Is 2 in seen? No.
  - Add 2 to seen.
  - State: seen = {1, 2}
- Iteration 3: num = 3
  - Is 3 in seen? No.
  - Add 3 to seen.
  - State: seen = {1, 2, 3}
- Iteration 4: num = 2
  - Is 2 in seen? Yes.
  - Return True immediately.
- Final result: True

[STEP_12_CODE_PLAN]
1. Initialize an empty set named seen.
2. Loop through each element num in the input list nums.
3. Inside the loop, check if num is already present in seen.
4. If num is in seen, return True immediately.
5. If num is not in seen, add num to seen using seen.add(num).
6. If the loop completes without returning, return False.

[STEP_13_IMPLEMENTATION]
The implementation uses Python's built-in set, which is implemented as a hash table.
- The in operator on a set has an expected time complexity of O(1).
- The add method also has an expected time complexity of O(1).
- This structure is highly readable and concise.
- It returns early as soon as a duplicate is detected, which can save time in practice.
- It does not mutate the input array.

[STEP_14_TEST_CASES]
- Test Case 1 (Representative Case with Duplicate):
  - Input: nums = [1, 2, 3, 3]
  - Expected Output: True
  - Validation: Validates that a duplicate at the end of the array is correctly identified.
- Test Case 2 (Representative Case without Duplicate):
  - Input: nums = [1, 2, 3, 4]
  - Expected Output: False
  - Validation: Validates that an array with all unique elements returns False.
- Test Case 3 (Empty Input):
  - Input: nums = []
  - Expected Output: False
  - Validation: Validates the boundary case of an empty array.
- Test Case 4 (Single Element):
  - Input: nums = [1]
  - Expected Output: False
  - Validation: Validates that a single-element array cannot have duplicates.
- Test Case 5 (All Duplicates):
  - Input: nums = [5, 5, 5]
  - Expected Output: True
  - Validation: Validates that multiple duplicates are handled correctly and returns early on the first duplicate.

[STEP_15_TIME_COMPLEXITY_DERIVATION]
Let n be the number of elements in nums.
1. We initialize the hash set seen, which takes O(1) time.
2. We iterate through the array nums of size n.
3. In each iteration, we perform:
   - A membership check: num in seen
   - An insertion: seen.add(num)
4. For Python's built-in set (which is implemented as a hash table), both membership checks and insertions have an expected time complexity of O(1).
5. In the worst case, we perform these operations n times.
6. Therefore, the expected total time complexity is O(n).
7. In highly rare pathological cases with extreme hash collisions, set operations can degrade to O(n) worst-case, making the total time O(n^2). However, in practice, the expected time complexity is O(n).
- Final canonical time complexity: O(n)

[STEP_16_SPACE_COMPLEXITY_DERIVATION]
Let n be the number of elements in nums.
1. The algorithm allocates a hash set seen to store visited elements.
2. In the worst case, all elements in nums are unique.
3. In this case, the set seen will grow to store all n elements.
4. Each element stored in the set requires O(1) auxiliary space.
5. Therefore, the maximum auxiliary space used by the set is O(n).
6. No other growing data structures or recursive call stacks are used.
- Final canonical space complexity: O(n)

[STEP_17_APPROACH_TRADEOFFS]
We compare the three documented approaches:
- S1 (Brute Force):
  - Time: O(n^2)
  - Space: O(1)
  - Advantage: No extra memory required.
  - Disadvantage: Extremely slow for large inputs.
- S2 (Sorting):
  - Time: O(n log n)
  - Space: O(n) (due to Python's Timsort worst-case space complexity).
  - Advantage: Simple adjacent scan after sorting.
  - Disadvantage: Modifies the input array and is slower than the hash-set approach.
- S3 (Hash Set - Preferred):
  - Time: O(n) (expected)
  - Space: O(n)
  - Advantage: Expected time complexity of O(n), which is lower than S1 and S2. Does not modify the input.
  - Disadvantage: Requires extra memory proportional to the number of unique elements.
Why S3 is preferred: It provides an expected time complexity of O(n) and does not modify the input array, which avoids side effects.

[STEP_18_INTERVIEW_COMMUNICATION]
- Before Coding:
  - Restate the problem to ensure alignment.
  - Clarify constraints (e.g., empty array, mutation permission).
  - Mention the brute-force approach (O(n^2) time, O(1) space) and explain its bottleneck (repeated scanning).
  - Propose the hash-set approach to optimize the lookup time to expected O(1), resulting in O(n) time and O(n) space.
- While Coding:
  - Explain the purpose of the seen set.
  - Explain the early return condition (if num in seen).
  - Explain why we add the element to the set only after checking.
- After Coding:
  - Trace the code with a simple example.
  - State the time complexity (O(n)) and space complexity (O(n)).
  - Discuss the tradeoff between the sorting approach (which modifies input) and the hash-set approach.

[INTERVIEW_SCRIPT]
"To solve this problem, I'll start by restating it: we want to find if any integer in the array appears more than once. If it does, we return true; otherwise, we return false.

A simple brute-force approach would be to compare every pair of elements using nested loops. This would take O(n^2) time and O(1) space. However, the bottleneck is that we are repeatedly scanning the array to check for duplicates.

We can optimize this by using a hash set to keep track of the numbers we have already seen. As we iterate through the array, we can check if the current number is already in our set in expected O(1) time. If it is, we immediately return true. If we finish the loop without finding any duplicates, we return false.

This approach improves the time complexity to expected O(n), while requiring O(n) auxiliary space to store the elements in the set.

Let's write the code for this."

[PATTERN_RECOGNITION]
- Main pattern: Using a Hash Set for tracking visited elements.
- Signals:
  - "Find duplicates", "Check if an element has appeared before", "Find the first repeating element".
  - Any problem where you need to check membership or frequency of elements in a collection with fast lookups.
- Common variations:
  - Two Sum (using a hash map to find the complement).
  - First Unique Character in a String (using a hash map to count frequencies).
- False-positive signals:
  - If the input array is already sorted, we don't need a hash set; we can just compare adjacent elements in O(1) space.
  - If the elements are bounded in a very small range (e.g., 1 to n), we might be able to use the array itself as a hash map (in-place marking) to achieve O(1) auxiliary space, though that mutates the input.

[COMMON_PITFALLS]
- Adding the current element to the set before checking if it is already in the set (this would cause the check to always return True).
- Returning False inside the loop instead of after the loop finishes.
- Assuming hash set operations are guaranteed O(1) worst-case instead of expected O(1).
- Forgetting that sorting the array in-place (like nums.sort()) mutates the input, which might not be allowed or expected.

[FINAL_REVIEW_CHECKLIST]
1. Can I restate the problem clearly?
2. Do I know the input, output, and constraints?
3. Did I clarify if the input array can be empty?
4. Can I explain the brute-force baseline and its O(n^2) bottleneck?
5. Can I explain how a hash set optimizes the lookup time?
6. Can I explain why the hash-set approach is correct using a loop invariant?
7. Can I trace a small example step-by-step?
8. Did I handle the empty array edge case correctly?
9. Can I derive the expected O(n) time complexity?
10. Can I derive the O(n) space complexity?
11. Can I discuss the tradeoffs between the hash-set and sorting approaches?
12. Can I communicate my thought process clearly before writing code?

@CONTENT_END

@NC250_END
"""
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
