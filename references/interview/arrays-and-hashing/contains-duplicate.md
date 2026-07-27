# Contains Duplicate

- **Category:** Arrays & Hashing
- **Difficulty:** Easy
- **Preferred solution:** S3
- **Source submission:** [`submission-10.py`](../../../Data Structures & Algorithms/duplicate-integer/submission-10.py)
- **Solution reference:** [Open](../../solution/arrays-and-hashing/contains-duplicate.py)
- **Study index:** [Back to index](../../README.md)

## Problem Details


Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

Example 1:

Input: nums = [1, 2, 3, 3]

Output: true

Example 2:

Input: nums = [1, 2, 3, 4]

Output: false

Constraints:

0 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9


## 1. Understand the Problem


1. We are given an integer array named nums.
2. We must return True when at least one value appears more than once.
3. We must return False when every value appears at most once.
4. A duplicate is a value that occurs at two or more different positions in the array.
5. The algorithm only needs to detect whether a duplicate exists; it does not need to return the duplicate value or its indices.
6. The main challenge is checking for repeated values efficiently when the array may contain many elements.


## 2. Restate the Problem


Possible spoken response:

"I am given a list of integers, and I need to determine whether any value occurs more than once. I should return True as soon as I know a duplicate exists, and return False if every value is unique."


## 3. Clarify and Confirm


1. Question: Do I only need to return whether a duplicate exists?
   - Why it matters: This determines whether the solution needs to track the duplicate value or its positions.
   - What the statement already establishes: The required output is a Boolean.
   - Safe assumption or implementation choice: Return only True or False.

2. Question: Can the array be empty?
   - Why it matters: An empty array has no pair of equal values.
   - What the statement already establishes: nums.length may be 0.
   - Safe assumption or implementation choice: Return False for an empty array.

3. Question: May the input array be modified?
   - Why it matters: A sorting-based approach changes the order of nums.
   - What the statement already establishes: Mutation permission is not specified.
   - Safe assumption or implementation choice: Prefer a solution that does not modify nums.

4. Question: Can values be negative or repeated many times?
   - Why it matters: The solution must work for all supported integer values and not assume a limited positive range.
   - What the statement already establishes: Values may be between -10^9 and 10^9.
   - Safe assumption or implementation choice: Use a general-purpose set rather than an indexed counting array.

5. Question: Is early return acceptable once a duplicate is found?
   - Why it matters: The algorithm can stop without scanning the remaining elements.
   - What the statement already establishes: Only existence matters.
   - Safe assumption or implementation choice: Return True immediately when a repeated value is detected.


## 4. Inputs, Outputs, and Constraints


1. Input:
   - nums is a List[int].
   - Each element is an integer.

2. Output:
   - Return type: bool.
   - Return True if any value appears more than once.
   - Return False if all values are unique.

3. Parameter meaning:
   - nums contains the values that must be checked for repetition.

4. Supported constraints:
   - 0 <= len(nums) <= 10^5.
   - -10^9 <= nums[i] <= 10^9.

5. Duplicate behavior:
   - One repeated value is enough to return True.
   - A value may appear more than twice, but the second occurrence already proves a duplicate exists.

6. Ordering requirements:
   - The original order does not affect the required Boolean result.
   - The preferred implementation does not reorder the input.

7. Mutation policy:
   - The statement does not explicitly grant permission to modify nums.
   - The preferred implementation leaves nums unchanged.

8. No-result behavior:
   - If no duplicate exists, return False.
   - The empty array and a one-element array both return False.

9. Important edge cases:
   - Empty array.
   - One element.
   - Duplicate at the beginning.
   - Duplicate at the end.
   - All elements equal.
   - All elements unique.
   - Negative values.

10. Complexity variable:
    - Let n be the number of elements in nums.


## 5. Baseline Approach


Approach: Brute Force

1. Core idea:
   - Compare every element with every element that appears after it.
   - If any pair contains equal values, return True.

2. Data structures:
   - No additional growing data structure is needed.
   - Only two loop indices are used.

3. Execution steps:
   - Choose an index i.
   - Compare nums[i] with each later value nums[j].
   - Return True when nums[i] == nums[j].
   - Continue until every distinct pair has been checked.
   - Return False if no equal pair is found.

4. Why it works:
   - Every possible pair of distinct positions is examined.
   - Therefore, any duplicate pair must eventually be compared.

5. Why it is a natural starting point:
   - It directly follows the definition of a duplicate: two different positions containing the same value.
   - It requires no special data structure or preprocessing.

6. Main limitation:
   - The same values participate in many repeated comparisons.
   - The number of comparisons grows quadratically with the input size.


## 6. Baseline Complexity


1. Let n be the number of elements in nums.

2. Main operation:
   - Compare nums[i] with nums[j].

3. Operation count:
   - The first element is compared with n - 1 later elements.
   - The second is compared with n - 2 later elements.
   - This continues down to one final comparison.
   - Total comparisons are:
     (n - 1) + (n - 2) + ... + 1 = n(n - 1) / 2.

4. Cost per operation:
   - Each integer equality comparison costs O(1).

5. Combination:
   - The dependent nested-loop work multiplies into quadratic growth.

6. Simplification:
   - n(n - 1) / 2 becomes O(n^2) after removing constants and lower-order terms.

7. Final time complexity:
   - Worst-case time: O(n^2).

8. Space usage:
   - The algorithm uses only fixed-size loop variables.
   - It creates no structure that grows with n.
   - The input is not modified.

9. Final auxiliary-space complexity:
   - O(1).


## 7. Find the Bottleneck


1. Repeated or expensive work:
   - The brute-force approach repeatedly scans later elements to determine whether the current value has appeared elsewhere.

2. Why it is expensive:
   - Each element may be compared with many other elements.
   - Most comparisons do not reveal new reusable information.

3. How often it occurs:
   - In the worst case, the algorithm performs n(n - 1) / 2 comparisons.

4. Information that could be reused:
   - After processing a value, we could remember that it has already appeared.
   - Then a later occurrence could be recognized immediately.

5. What must improve:
   - Replace repeated pairwise searches with a fast way to answer:
     "Have I already seen this value?"


## 8. Optimization Bridge


1. The repeated work to avoid:
   - For each value, we should not scan many earlier or later elements looking for a match.

2. Information to store:
   - Store every value that has already been processed.

3. Supporting data structure:
   - A hash set stores unique values and supports expected O(1) membership checks and insertions.
   - A membership check asks whether a value is already present in the set.

4. How this reduces the expensive operation:
   - Instead of comparing the current value with many previous values, perform one expected O(1) set lookup.

5. New tradeoff:
   - The set may store up to n distinct values, so the solution uses O(n) auxiliary space.

6. Why the tradeoff is acceptable:
   - The constraints allow as many as 10^5 elements.
   - Reducing expected time from O(n^2) to O(n) is usually worth the additional linear memory.
   - The input remains unchanged.


## 9. Preferred Approach


Approach: Hash Set

A hash set is a collection that stores unique values and supports expected constant-time membership checks.

Important variables:
- seen: the set of values processed before the current iteration.
- num: the current value from nums.

Algorithm:

1. Initialize seen as an empty set.
2. Process the values in nums from left to right.
3. For each num, check whether num is already in seen.
4. If num is already in seen, return True immediately.
5. Otherwise, add num to seen.
6. Continue until every value has been processed.
7. If no repeated value is found, return False.

Why the order matters:
- Membership must be checked before adding the current value.
- Adding first would make every current value appear to be a duplicate of itself.

Mutation behavior:
- nums is not modified.

Main advantage:
- Expected O(n) time with a single left-to-right pass.

Main tradeoff:
- O(n) auxiliary space in the case where all values are distinct.


## 10. Correctness Reasoning


Proof style: Invariant

An invariant is a fact that remains true throughout the algorithm.

Invariant:
- Before each iteration, seen contains exactly the values that appeared earlier in nums.

1. Initialization:
   - Before the first iteration, no values have been processed.
   - seen is empty, so the invariant is true.

2. Why the invariant remains true:
   - If the current num is not in seen, the algorithm adds it.
   - After that update, seen contains all values processed so far.
   - Therefore, before the next iteration, seen again contains exactly the earlier values.

3. Why no valid duplicate is missed:
   - Suppose the current num appeared earlier.
   - By the invariant, that earlier occurrence is already stored in seen.
   - The membership check succeeds, so the algorithm returns True.

4. Why no invalid result is returned:
   - The algorithm returns True only when num is already in seen.
   - By the invariant, seen contains only values from earlier positions.
   - Therefore, the same value appears at two distinct positions.

5. Why termination gives the required result:
   - If the loop finishes, every value was checked and none appeared in seen before.
   - Therefore, all values are unique, so returning False is correct.


## 11. Example Trace


Official example:

Input:
- nums = [1, 2, 3, 3]

Expected output:
- True

Initial state:
- seen = set()

Iteration 1:
- num = 1
- Is 1 in seen? No.
- Add 1.
- seen = {1}

Iteration 2:
- num = 2
- Is 2 in seen? No.
- Add 2.
- seen = {1, 2}

Iteration 3:
- num = 3
- Is 3 in seen? No.
- Add 3.
- seen = {1, 2, 3}

Iteration 4:
- num = 3
- Is 3 in seen? Yes.
- Return True immediately.

Final result:
- True, because 3 appears more than once.


## 12. Code Plan


1. Imports:
   - Import List for the method's type annotation.

2. Method signature:
   - Preserve hasDuplicate(self, nums: List[int]) -> bool.

3. Data structure:
   - Create an empty set named seen.

4. Loop:
   - Use a for loop to process each num in nums.

5. Key condition:
   - Check if num in seen before changing the set.

6. Early return:
   - Return True immediately when the membership check succeeds.

7. State update:
   - Add num to seen only when it has not appeared before.

8. Final return:
   - Return False after the loop if no duplicate was detected.

9. Mutation choice:
   - Do not sort, reorder, or otherwise modify nums.


## 13. Implementation


1. The first code block creates seen, matching the algorithm's stored history of previously processed values.
2. The for loop performs one left-to-right pass through nums.
3. The condition num in seen implements the duplicate test.
4. The early return avoids unnecessary work after a duplicate is confirmed.
5. seen.add(num) updates the stored state for future iterations.
6. The final return False handles empty input, one-element input, and arrays containing only unique values.
7. Python set membership and insertion are expected O(1), although pathological hash collisions can make them slower.
8. The implementation does not modify nums.


## 14. Test Cases


1. Purpose: Representative duplicate case
   - Input: [1, 2, 3, 3]
   - Expected output: True
   - What it validates: A repeated value is detected after several unique values.

2. Purpose: Representative unique case
   - Input: [1, 2, 3, 4]
   - Expected output: False
   - What it validates: The method returns False after scanning all unique values.

3. Purpose: Empty input
   - Input: []
   - Expected output: False
   - What it validates: The allowed smallest array contains no duplicate.

4. Purpose: One element
   - Input: [7]
   - Expected output: False
   - What it validates: One value cannot form a duplicate pair.

5. Purpose: Earliest possible duplicate
   - Input: [5, 5, 8, 9]
   - Expected output: True
   - What it validates: The early return occurs on the second element.

6. Purpose: Duplicate at the end
   - Input: [1, 2, 3, 4, 1]
   - Expected output: True
   - What it validates: Previously stored values remain available throughout the scan.

7. Purpose: All values repeated
   - Input: [6, 6, 6]
   - Expected output: True
   - What it validates: The second occurrence is enough to return True.

8. Purpose: Negative values
   - Input: [-3, -1, -3]
   - Expected output: True
   - What it validates: The method works across the supported integer range.

9. Purpose: Mutation-sensitive behavior
   - Input: [3, 1, 2]
   - Expected output: False
   - What it validates: The method can produce the result without changing the original ordering.


## 15. Time Complexity Derivation


1. Define the variable:
   - Let n be the number of elements in nums.

2. Initialization phase:
   - Creating an empty set costs O(1).

3. Iteration phase:
   - In the worst case for the loop count, every element is processed once.
   - Therefore, there are at most n iterations.

4. Work per iteration:
   - One set membership check: expected O(1).
   - At most one set insertion: expected O(1).

5. Combining the costs:
   - The operations within each iteration are sequential, so they add to expected O(1).
   - Repeating expected O(1) work n times gives expected O(n).

6. Simplification:
   - O(1) + n · O(1) simplifies to O(n).

7. Qualification:
   - Python set operations are expected O(1), not guaranteed worst-case O(1).
   - Pathological hash collisions could make the overall worst case O(n^2).

8. Final complexity:
   - Expected time complexity: O(n).

Interview-ready statement:
- "I scan the array once, and each set lookup and insertion is expected O(1), so the total expected time is O(n)."


## 16. Space Complexity Derivation


1. Fixed-size variables:
   - num stores one current value.
   - These fixed variables use O(1) space.

2. Growing structure:
   - seen stores values that have already been processed.

3. Maximum size:
   - If every value is unique, seen contains all n values.
   - Therefore, seen may require O(n) space.

4. Recursion depth:
   - The implementation is iterative, so no recursion stack is used.

5. Temporary storage:
   - No copies, slices, sorting workspace, or additional growing structures are created.

6. Output-space treatment:
   - The required Boolean output uses O(1) space.

7. Mutation:
   - nums is not modified.

8. Combining storage:
   - O(n) for seen plus O(1) for fixed variables simplifies to O(n).

9. Final auxiliary complexity:
   - O(n).

Interview-ready statement:
- "The set can hold up to all n distinct values, so the auxiliary-space complexity is O(n)."


## 17. Approach Tradeoffs


Baseline: Brute Force
- Main idea: Compare every distinct pair of positions.
- Time: O(n^2) worst-case.
- Space: O(1).
- Advantage: Uses constant auxiliary space and is straightforward.
- Disadvantage: Performs many repeated comparisons.

Intermediate approach: Sorting
- Main idea: Sort values so duplicates become adjacent, then scan neighboring elements.
- Time: O(n log n) worst-case.
- Space: O(n) worst-case for Python sorting workspace.
- Advantage: Avoids quadratic pairwise comparison.
- Disadvantage: Modifies nums and remains slower than expected linear hashing.

Preferred approach: Hash Set
- Main idea: Store previously seen values and check each new value against the set.
- Time: O(n) expected.
- Space: O(n).
- Advantage: Expected linear time and no input mutation.
- Disadvantage: Requires additional memory.

Why choose the preferred approach:
- It removes the brute-force bottleneck of repeatedly searching for a matching value.
- One expected O(1) set lookup replaces many pairwise comparisons.
- It is concise, readable, and directly expresses the question: "Have I seen this value before?"

Memory tradeoff:
- The faster expected running time requires storing up to n values.

Mutation tradeoff:
- Unlike sorting, the hash-set approach preserves the original input order.

Interview readability:
- The implementation is short, and its key invariant is easy to explain.

When the baseline might be acceptable:
- The brute-force approach may be acceptable for very small inputs or when constant auxiliary space is required and slower time is permitted.


## 18. Interview Communication


BEFORE CODING:

1. Restate the problem:
   - "I need to return whether any integer appears more than once."

2. Confirm important assumptions:
   - "The output is only a Boolean, and I will avoid modifying the input."

3. Introduce the baseline:
   - "A direct approach is to compare every pair of values."

4. Identify the bottleneck:
   - "That repeats many comparisons and takes O(n^2) time."

5. Propose the preferred approach:
   - "I can store previously seen values in a set and check each value in expected O(1) time."

WHILE CODING:

1. Explain important variables:
   - "seen contains exactly the values processed earlier."

2. State the key invariant:
   - "Before each iteration, seen represents all prior values."

3. Narrate update order:
   - "I check membership before insertion so the current value is not compared with itself."

4. Verify logic:
   - "A successful membership check means the same value appeared at an earlier index."

5. Correct mistakes calmly:
   - "I need the check before seen.add(num); otherwise every value would immediately appear present."

AFTER CODING:

1. Trace or test:
   - Walk through a small duplicate case and a unique case.

2. Explain correctness:
   - Use the invariant that seen contains all earlier values.

3. Derive time:
   - n iterations with expected O(1) set operations gives expected O(n).

4. Derive space:
   - The set may hold n distinct values, giving O(n) auxiliary space.

5. State the tradeoff:
   - The solution uses more memory to avoid quadratic repeated comparisons.


## Interview Script


"I am given an integer array and need to return True if any value occurs more than once, otherwise False. The output is only a Boolean, and I will avoid modifying the input.

A straightforward baseline is to compare every pair of positions. That is correct because it checks all possible duplicate pairs, but in the worst case it performs O(n^2) comparisons.

The bottleneck is repeatedly searching through other values to determine whether the current value has appeared before. I can avoid that by storing previously processed values in a hash set.

I will initialize an empty set called seen. Then I will scan nums from left to right. Before each iteration, seen contains exactly the values from earlier positions. If the current number is already in seen, then I have found the same value at two different positions, so I return True. Otherwise, I add it to seen. If the loop finishes, every value was unique, so I return False.

For example, with [1, 2, 3, 3], I add 1, 2, and 3 to the set. When I reach the final 3, it is already present, so I return True.

The loop processes at most n values. Set membership and insertion are expected O(1), so the expected time complexity is O(n). The set may store up to n distinct values, so the auxiliary-space complexity is O(n). The main tradeoff is using linear extra memory to get expected linear time without modifying the input."


## Pattern Recognition


Main pattern:
- Use a hash set when the problem asks whether an item has appeared before.

Statement signals:
1. "Contains a duplicate."
2. "Repeated value."
3. "Already seen."
4. "Unique elements."
5. "Return whether any value occurs more than once."

Why these signals suggest a hash set:
- The task requires fast membership testing.
- A set records which values have already appeared.
- The second occurrence can be detected immediately.

Common data structures:
- Hash set when only existence matters.
- Hash map when counts, indices, or additional information must be stored.

Common variations:
1. Return the first repeated value.
2. Count how often each value appears.
3. Find all duplicated values.
4. Check whether a duplicate appears within a limited index distance.
5. Determine whether two different inputs share a value.

Questions to ask:
1. Do I need only a Boolean, or the duplicate itself?
2. Do I need counts or positions?
3. May I modify the input?
4. Is extra O(n) memory acceptable?
5. Is there a distance or ordering restriction?

False-positive signals:
- The presence of repeated values does not always mean a plain set is sufficient.
- If the problem asks for frequencies, indices, or distances, a hash map or sliding-window structure may be needed.

When the pattern appears applicable but is not enough:
- If duplicates must be found within k positions, storing every historical value can retain stale information.
- If memory must be constant and input mutation is allowed, sorting may be more appropriate.
- If values come from a small fixed range, a counting array may be possible.

Neighboring patterns:
- Frequency counting with a hash map.
- Sorting followed by an adjacent scan.
- Sliding window with a set for nearby duplicates.
- Two-sum style complement lookup with a hash map.


## Common Pitfalls


UNDERSTANDING AND COMMUNICATION:

1. Restating the task as returning the duplicated value instead of a Boolean.
2. Assuming the input may be modified without confirming it.
3. Skipping the brute-force baseline and failing to explain what the optimized solution improves.
4. Saying "use hashing" without explaining that the set stores previously seen values.
5. Using the term expected O(1) without understanding that hash operations are not guaranteed worst-case O(1).
6. Stating O(n) time without deriving it from n iterations and expected constant-time set operations.

IMPLEMENTATION:

1. Adding num to seen before checking membership, which makes every value appear duplicated immediately.
2. Forgetting to add unseen values to seen.
3. Returning False inside the loop after the first unique value instead of waiting until all values are checked.
4. Using list membership for previously seen values, which makes each lookup O(n) and can restore O(n^2) total time.
5. Sorting nums unintentionally when the chosen approach is supposed to preserve the input.
6. Comparing adjacent sorted values with nums[i] instead of nums[i - 1], which is always equal to itself.

COMPLEXITY:

1. Treating expected O(1) set operations as guaranteed worst-case O(1).
2. Calling the total complexity O(1) because each individual lookup is expected O(1), while ignoring that up to n lookups occur.
3. Claiming O(1) auxiliary space while ignoring the growing seen set.
4. Counting the original nums array as auxiliary space.
5. Forgetting that an early return improves some inputs but does not change the expected worst-input loop count of n.


## Final Review Checklist


1. Can I restate the problem using the input, Boolean output, and duplicate condition?
2. Do I know the supported input size and value range?
3. Do I know that empty and one-element arrays return False?
4. Can I explain the brute-force baseline?
5. Can I derive its O(n^2) time from the number of pairs?
6. Can I identify repeated pairwise searching as the bottleneck?
7. Can I explain why storing previously seen values removes that bottleneck?
8. Can I define what the seen set contains before each iteration?
9. Can I explain why membership must be checked before insertion?
10. Can I trace [1, 2, 3, 3] correctly?
11. Can I name important tests, including empty input and all-unique input?
12. Can I derive expected O(n) time from the actual code?
13. Can I derive O(n) auxiliary space from the maximum set size?
14. Can I state the time-memory and mutation tradeoffs?
15. Can I explain and write the solution naturally without copying?

## Executable Preferred Implementation

```python
from typing import List

class Solution:

    def hasDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```
