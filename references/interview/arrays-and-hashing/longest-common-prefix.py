from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        """
        @NC250_START

        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S3

        @PROBLEM_DETAILS_START

        PROBLEM: Longest Common Prefix
        URL: https://leetcode.com/problems/longest-common-prefix/
        DIFFICULTY: Easy
        PROBLEM DETAILS:
        Write a function to find the longest common prefix string amongst an array of strings.

        If there is no common prefix, return an empty string "".

        Example 1:
        Input: strs = ["flower","flow","flight"]
        Output: "fl"

        Example 2:
        Input: strs = ["dog","racecar","car"]
        Output: ""
        Explanation: There is no common prefix among the input strings.

        Constraints:
        - 1 <= strs.length <= 200
        - 0 <= strs[i].length <= 200
        - strs[i] consists of only lowercase English letters.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [STEP_1_UNDERSTAND_THE_PROBLEM]
        We are given an array of strings, `strs`. Our goal is to find the longest common prefix string shared among all strings in the array.
        - A prefix is a substring that starts at the very beginning of a string.
        - A common prefix is a prefix that is shared by every single string in the array.
        - If there is no common prefix, we must return an empty string `""`.
        - The problem is nontrivial because strings can have different lengths, and we want to find the maximum length of a prefix that is shared by all of them without doing redundant character comparisons.

        [STEP_2_RESTATE_THE_PROBLEM]
        "Given a list of strings, I need to find the longest sequence of characters at the start of these strings that is identical across all of them. If they don't share any starting characters, I should return an empty string."

        [STEP_3_CLARIFY_AND_CONFIRM]
        - Question: What should be returned if the input list is empty?
          - Why it matters: Prevents index out of bounds errors.
          - What the statement establishes: The constraints state `1 <= strs.length <= 200`, so the list will always contain at least one string.
        - Question: Are the characters case-sensitive?
          - Why it matters: Case differences (e.g., 'A' vs 'a') affect character matching.
          - What the statement establishes: The constraints state `strs[i]` consists of only lowercase English letters.
        - Question: Is input mutation allowed?
          - Why it matters: Sorting the input list in-place modifies the caller's list.
          - What the statement establishes: The problem statement does not specify whether input mutation is permitted. The preferred implementation uses `sorted(strs)`, which creates a new sorted list and does not mutate the original input list in-place.

        [STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
        - Input: `strs: List[str]`
        - Output: `str`
        - Constraints:
          - `1 <= strs.length <= 200`
          - `0 <= strs[i].length <= 200`
          - `strs[i]` consists of only lowercase English letters.
        - Duplicate behavior: Duplicate strings are handled naturally; they share the same prefix.
        - Ordering requirements: The input list is unordered.
        - Mutation behavior: The preferred implementation does not mutate the input list in-place because it uses `sorted(strs)`.
        - No-result behavior: Returns `""` if there is no common prefix.
        - Edge cases:
          - A single string in the list: The common prefix is the string itself.
          - Empty string `""` as one of the elements: The common prefix must be `""`.
          - No common prefix at all: Returns `""`.

        [STEP_5_BASELINE_APPROACH]
        The earliest documented approach is S1 (Horizontal Scanning).
        - Core idea: Find the longest common prefix of the first two strings, then use that prefix to find the common prefix with the third string, and so on. If at any point the prefix becomes empty, we can return immediately.
        - Data structures: A string variable `prefix` to store the running common prefix.
        - Major execution steps:
          1. If the input list `strs` is empty, return an empty string.
          2. Initialize `prefix` as the first string `strs[0]`.
          3. Iterate through the remaining strings in `strs` from index 1 to the end.
          4. For each string, compare characters with `prefix` up to the minimum length of both.
          5. Update `prefix` to be the common prefix found.
          6. If `prefix` becomes empty, return `""`.
          7. Return `prefix` after checking all strings.
        - Why it works: If a prefix is common to all strings, it must be common to any subset of them.
        - Why it is a natural starting point: It mimics how we might compare them one by one.

        [STEP_6_BASELINE_COMPLEXITY]
        - Time Complexity: O(n * m) where n is the number of strings and m is the average length of the strings. In the worst case, we compare all characters of all strings.
        - Space Complexity: O(1) auxiliary space, as we only store the prefix and indices.

        [STEP_7_FIND_THE_BOTTLENECK]
        In horizontal scanning, we compare the running prefix against every single string. If we have a very long prefix that matches almost all strings but fails on the last one, we might perform many redundant character comparisons. Specifically, we are comparing intermediate strings that might not contribute to narrowing down the prefix any more than comparing the most extreme strings would.

        [STEP_8_OPTIMIZATION_BRIDGE]
        - If we sort the strings lexicographically, they are ordered alphabetically.
        - In an alphabetically sorted list, the two most different strings will be at the very beginning (index 0) and the very end (index -1).
        - Any common prefix shared by all strings in the sorted list must also be shared by the first and last strings.
        - More importantly, the common prefix of the entire set is exactly the common prefix of just the first and last strings in the sorted list.
        - Therefore, by sorting, we can reduce the problem of comparing all strings to comparing just two strings: the first and the last.
        - This introduces a tradeoff: sorting takes O(n * m * log n) time and O(n * m) space (for the sorted copy), but the comparison phase becomes extremely simple and only requires comparing two strings.

        [STEP_9_PREFERRED_APPROACH]
        - Name: Sorting-Based Prefix Comparison (S3)
        - Central idea: Sort the list of strings lexicographically, then find the common prefix of only the first and last strings.
        - Meaning of variables:
          - `strs`: The input list of strings.
          - `first_str`: The lexicographically first string after sorting.
          - `last_str`: The lexicographically last string after sorting.
          - `min_len_str`: The minimum length between `first_str` and `last_str`.
          - `i`: The loop index for character comparison.
        - Initialization:
          - If `len(strs) == 1`, return `strs[0]` immediately.
          - Sort the list using `sorted(strs)`.
          - Assign `first_str = strs[0]` and `last_str = strs[-1]`.
        - Processing order:
          - Iterate `i` from `0` to `min_len_str - 1`.
        - Important conditions:
          - If `first_str[i] != last_str[i]`, return `first_str[:i]`.
        - Termination:
          - If the loop completes without mismatch, return `first_str`.
        - Mutation behavior: Does not mutate the input list in-place because `sorted()` creates a new list.
        - Main advantage: Only compares two strings after sorting.
        - Main tradeoff: Sorting all strings is asymptotically slower than linear scanning when n is large, and it requires extra space to store the sorted copy.

        [STEP_10_CORRECTNESS_REASONING]
        - Claim: The longest common prefix of a lexicographically sorted list of strings is equal to the longest common prefix of its first and last elements.
        - Why it remains true: Lexicographical sorting orders strings by their characters from left to right. If the first string and the last string share a prefix of length k, then any string sorted between them must also share at least that same prefix of length k. This is because any intermediate string is lexicographically greater than or equal to the first string, and less than or equal to the last string.
        - Why no valid result is missed: Any character mismatch between the first and last strings at index i means the prefix cannot be longer than i.
        - Why no invalid result is returned: We only return characters that match in both the first and last strings, which guarantees they match in all intermediate strings.

        [STEP_11_EXAMPLE_TRACE]
        Custom teaching example:
        - Input: `strs = ["flower", "flow", "flight"]`
        - Expected output: `"fl"`
        - Initial state: `len(strs)` is 3, so we proceed.
        - Sorting: `strs = sorted(strs)` results in `["flight", "flow", "flower"]`.
        - First and last strings:
          - `first_str = "flight"`
          - `last_str = "flower"`
        - Minimum length: `min_len_str = min(6, 6) = 6`.
        - Iterations:
          - `i = 0`: `first_str[0]` is 'f', `last_str[0]` is 'f'. Match.
          - `i = 1`: `first_str[1]` is 'l', `last_str[1]` is 'l'. Match.
          - `i = 2`: `first_str[2]` is 'i', `last_str[2]` is 'o'. Mismatch!
        - Return point: Return `first_str[:2]`, which is `"fl"`.
        - Final result: `"fl"`.

        [STEP_12_CODE_PLAN]
        - Check if the input list has only 1 string. If so, return it immediately.
        - Sort the list of strings lexicographically using `sorted(strs)` and assign the result back to `strs`.
        - Retrieve the first string `first_str` (at index 0) and the last string `last_str` (at index -1).
        - Find the minimum length between `first_str` and `last_str` using `min(len(first_str), len(last_str))`.
        - Loop through indices `i` from `0` to `min_len_str - 1`.
        - Inside the loop, check if `first_str[i]` is not equal to `last_str[i]`.
        - If they are not equal, return the substring of `first_str` from index `0` up to `i` (exclusive).
        - If the loop completes without finding any mismatch, return `first_str` (which is the common prefix up to `min_len_str`).

        [STEP_13_IMPLEMENTATION]
        - The implementation begins with a base case check `len(strs) == 1` to handle single-string inputs efficiently.
        - It uses Python's built-in `sorted()` function, which implements Timsort. This is highly optimized and stable.
        - By extracting `strs[0]` and `strs[-1]`, we avoid comparing any other strings in the list.
        - The loop uses a simple index-based comparison.
        - Slicing `first_str[:i]` is used to return the prefix when a mismatch is found.

        [STEP_14_TEST_CASES]
        - Test Case 1 (Representative Case):
          - Input: `strs = ["flower", "flow", "flight"]`
          - Expected output: `"fl"`
          - What it validates: Standard behavior with a common prefix of length 2.
        - Test Case 2 (No Common Prefix):
          - Input: `strs = ["dog", "racecar", "car"]`
          - Expected output: `""`
          - What it validates: Correctly returns an empty string when there is no common prefix.
        - Test Case 3 (Single String):
          - Input: `strs = ["apple"]`
          - Expected output: `"apple"`
          - What it validates: Correctly handles the single-string edge case via the early return.
        - Test Case 4 (One Empty String):
          - Input: `strs = ["", "b"]`
          - Expected output: `""`
          - What it validates: Handles empty strings in the input list correctly.

        [STEP_15_TIME_COMPLEXITY_DERIVATION]
        - Let n be the number of strings in `strs` and m be the maximum length of a string.
        - Sorting n strings of maximum length m takes O(m * n log n) time. This is because comparing two strings of length m takes O(m) time, and Timsort performs O(n log n) comparisons.
        - Finding the minimum length of the first and last strings takes O(1) time.
        - The comparison loop runs at most `min_len_str` times, which is at most m iterations. Each character comparison takes O(1) time.
        - Slicing the string to return the prefix takes at most O(m) time.
        - Combining these phases, the dominant operation is sorting.
        - Therefore, the final canonical time complexity is O(n * m * log n).

        [STEP_16_SPACE_COMPLEXITY_DERIVATION]
        - The `sorted(strs)` function creates a new sorted list of strings.
        - This requires storing references to all n strings, which takes O(n) space.
        - Additionally, Timsort requires auxiliary space. In Python, sorting a list of size n takes O(n) auxiliary space.
        - Since the strings themselves are not copied (only references are stored), the auxiliary space to store the sorted copy of the strings is O(n * m) in the worst case if we consider the total size of the strings, or O(n) if we only count the references.
        - Following the canonical SOLUTION_REFERENCE, the space complexity is stated as O(n * m) auxiliary space to store the sorted copy of the strings.
        - Auxiliary space excluding the returned output: O(n * m) to store the sorted copy.

        [STEP_17_APPROACH_TRADEOFFS]
        - S1 (Horizontal Scanning):
          - Time: O(n * m) where m is the average length.
          - Space: O(1).
          - Advantage: Simple, memory-efficient, does not modify or copy the input.
          - Disadvantage: May perform redundant comparisons if the prefix is long but mismatch occurs late.
        - S2 (Vertical Scanning):
          - Time: O(n * m) where m is the length of the shortest string.
          - Space: O(1).
          - Advantage: Early termination on mismatch, optimal for most cases.
          - Disadvantage: Requires nested loops over all strings.
        - S3 (Sorting):
          - Time: O(n * m * log n).
          - Space: O(n * m).
          - Advantage: Only compares two strings (first and last) after sorting, which simplifies the comparison logic.
          - Disadvantage: Sorting all strings is asymptotically less efficient than linear scanning and requires extra memory.

        [STEP_18_INTERVIEW_COMMUNICATION]
        - BEFORE CODING:
          - Restate the problem: "I need to find the longest common prefix among an array of strings."
          - Ask clarification questions: "Are all characters lowercase? Yes, the constraints confirm this. Is the input list guaranteed to be non-empty? Yes, the constraints state at least one string is present."
          - Propose the approach: "While we can scan horizontally or vertically in linear time, another interesting approach is to sort the strings lexicographically. This places the most different strings at the first and last positions, allowing us to find the common prefix by comparing only those two strings."
        - WHILE CODING:
          - Explain variables: "I'll first handle the single-string case. Then I'll sort the list, extract the first and last strings, and compare them character by character."
        - AFTER CODING:
          - Trace the solution: Walk through with `["flower", "flow", "flight"]`.
          - State complexity: "The time complexity is dominated by sorting, which is O(n * m * log n). The space complexity is O(n * m) to store the sorted copy."

        [INTERVIEW_SCRIPT]
        "To solve the Longest Common Prefix problem, we want to find the longest starting substring shared by all strings in the input list.

        A straightforward way to do this is to compare the strings one by one, or character by character across all strings. However, we can also leverage sorting. If we sort the list of strings lexicographically, the strings are ordered alphabetically. This means the two strings that are most different from each other will end up at the very beginning and the very end of the sorted list.

        Because of this ordering, any common prefix shared by all strings must be shared by the first and last strings. Thus, the longest common prefix of the entire array is simply the common prefix of the first and last strings in the sorted array.

        Let's write the code for this. First, if there is only one string, we return it immediately. Otherwise, we sort the list. We then take the first and last strings, find the minimum of their lengths, and iterate through their characters. As soon as we find a mismatch, we return the substring up to that index. If we finish the loop without a mismatch, we return the first string itself.

        This approach has a time complexity of O(n * m * log n) due to the sorting step, where n is the number of strings and m is the maximum length of a string. The space complexity is O(n * m) because sorted() creates a new sorted copy of the list."

        [PATTERN_RECOGNITION]
        - Main pattern: Lexicographical sorting to find extreme elements.
        - Statement signals: "longest common prefix", "common substring among all elements", or problems involving finding boundaries in sorted string sets.
        - Why those signals suggest the technique: Sorting strings lexicographically groups similar prefixes together and puts the most divergent strings at the boundaries.
        - Common variations: Finding the shortest/longest string, grouping anagrams, or finding the lexicographical range.
        - False-positive signals: If we need to find common subsequences (which are not contiguous prefixes), sorting lexicographically will not help.

        [COMMON_PITFALLS]
        - Single string input: If the input list contains only one string, we must handle it correctly (e.g., by returning it immediately) to avoid unnecessary sorting or index errors.
        - Empty input list: Although constraints say `strs.length >= 1`, in general, accessing `strs[0]` on an empty list would raise an `IndexError`.
        - Modifying the input: Using `strs.sort()` mutates the original list in-place. If the caller expects the input list to remain unchanged, we should use `sorted(strs)` instead.
        - Assuming O(n log n) sorting time for strings: Remember that string comparison is not O(1); it takes O(m) time where m is the length of the string. Thus, sorting n strings takes O(m * n log n) time.

        [FINAL_REVIEW_CHECKLIST]
        - Can I restate the problem?
        - Do I know the input, output, and constraints?
        - Do I know what actually needs clarification?
        - Can I explain the horizontal scanning baseline?
        - Can I identify its bottleneck?
        - Can I explain how sorting simplifies the comparison?
        - Can I explain why comparing only the first and last strings is correct?
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
        if len(strs) == 1: 
            return strs[0]
        
        strs = sorted(strs)
        first_str, last_str = strs[0], strs[-1]
        min_len_str = min(len(first_str), len(last_str))

        for i in range(min_len_str):
            if first_str[i] != last_str[i]: 
                return first_str[:i]
        return first_str
