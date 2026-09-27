class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        @NC250_START

        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Valid Anagram
        URL: https://neetcode.io/problems/is-anagram/question?list=neetcode250
        DIFFICULTY: Easy

        PROBLEM DETAILS:

        Given two strings s and t, return True if the two strings are anagrams
        of each other. Otherwise, return False.

        Two strings are anagrams if they contain the same characters, with each
        character appearing the same number of times, regardless of order.

        Because s and t consist only of lowercase English letters, there are
        exactly 26 possible characters that need to be tracked.


        Example 1:

        Input:

        s = "racecar", t = "carrace"

        Output:

        true

        Explanation:

        Both strings contain exactly the same characters with the same
        frequencies, only in a different order.


        Example 2:

        Input:

        s = "jar", t = "jam"

        Output:

        false

        Explanation:

        The strings do not contain the same characters with the same
        frequencies. The first string contains 'r', while the second contains
        'm'.


        Example 3:

        Input:

        s = "x", t = "x"

        Output:

        true

        Explanation:

        Both strings contain the same single character exactly once.


        Constraints:

        - 1 <= s.length, t.length <= 5 * 10^4
        - s and t consist of lowercase English letters.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [STEP_1_UNDERSTAND_THE_PROBLEM]
        We are given two strings, s and t. We need to determine if they are anagrams of each other.
        An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.
        In other words, s and t must contain the exact same characters with the exact same frequencies.
        The problem guarantees that both strings consist only of lowercase English letters, which limits the alphabet size to 26.

        [STEP_2_RESTATE_THE_PROBLEM]
        "I need to write a function that takes two strings, s and t, and returns True if they have the exact same characters with the exact same counts, and False otherwise."

        [STEP_3_CLARIFY_AND_CONFIRM]
        - Question: Can the strings contain uppercase letters or special characters?
          Why it matters: It affects the size of our frequency tracker.
          What the statement establishes: The constraints state that s and t consist only of lowercase English letters.
        - Question: Are we allowed to modify the input strings?
          Why it matters: If we can sort them in-place, it might affect space complexity.
          What the statement establishes: Strings in Python are immutable, so we cannot modify them in-place.
        - Question: What should we return if the strings have different lengths?
          Why it matters: If they have different lengths, they cannot be anagrams, and we can return False immediately.
          What the statement establishes: This is a fundamental property of anagrams.

        [STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
        - Input types: s (str), t (str)
        - Output type: bool
        - Constraints:
          - 1 <= s.length, t.length <= 5 * 10^4
          - s and t consist of lowercase English letters.
        - Duplicate behavior: Duplicate characters must be counted exactly.
        - Ordering requirements: Order does not matter.
        - Mutation behavior: The input strings are not mutated.
        - Important edge cases: Single character strings, strings of different lengths.
        - Relevant complexity variables: n is the length of string s (and t).

        [STEP_5_BASELINE_APPROACH]
        The baseline approach is to sort both strings and compare them (S3).
        - Core idea: Sorting both strings places their characters into a canonical order. If they are anagrams, their sorted representations will be identical.
        - Data structures: Lists of characters created during sorting.
        - Major execution steps:
          1. Compare the lengths of s and t. If they are different, return False.
          2. Sort the characters in s.
          3. Sort the characters in t.
          4. Compare the two sorted results.
          5. Return whether they are equal.
        - Why it works: Sorting canonicalizes the strings, making comparison straightforward.
        - Why it is a natural starting point: It requires very little code and directly leverages the definition of anagrams.
        - Main limitation: Sorting takes O(n log n) time and O(n) space in Python.

        [STEP_6_BASELINE_COMPLEXITY]
        - Time complexity: O(n log n) because sorting a string of length n takes O(n log n) time. Comparing the sorted lists takes O(n) time.
        - Auxiliary space: O(n) because Python's sorted() function creates a new list of characters of size n.

        [STEP_7_FIND_THE_BOTTLENECK]
        The bottleneck in the sorting approach is the sorting step itself, which takes O(n log n) time.
        We are sorting the characters to compare their frequencies, but we do not actually need to order the characters to count them.
        Ordering is unnecessary work. We only need to verify that the counts of each character are identical.

        [STEP_8_OPTIMIZATION_BRIDGE]
        Instead of sorting, we can count the occurrences of each character.
        Since the alphabet is limited to 26 lowercase English letters, we can use a fixed-size array of size 26 to store the counts.
        This allows us to count characters in a single pass, reducing the time complexity from O(n log n) to O(n).
        It also reduces the auxiliary space from O(n) to O(1) because the array size is fixed at 26 regardless of the input string length.

        [STEP_9_PREFERRED_APPROACH]
        The preferred approach is Fixed Array Frequency Count (S1).
        - Central idea: Use a fixed-size array of 26 counters to track the difference in character frequencies between s and t.
        - Meaning of important variables:
          - counts: An array of 26 integers, initialized to 0, representing the net frequency of each character ('a' through 'z').
          - i: Loop index to iterate through the strings.
        - Initialization: counts = [0] * 26
        - Processing order: Iterate from index 0 to len(s) - 1.
        - Important conditions:
          - If len(s) != len(t), return False immediately.
        - State updates:
          - For each index i, increment counts[ord(s[i]) - ord('a')] and decrement counts[ord(t[i]) - ord('a')].
        - Termination: After the loop, check if all values in counts are 0.
        - Final return: True if all values are 0, otherwise False.
        - Mutation behavior: Does not mutate the input strings.
        - Main advantage: O(n) time and O(1) auxiliary space.
        - Main tradeoff: Relies on the fixed alphabet size (lowercase English letters).

        [STEP_10_CORRECTNESS_REASONING]
        An invariant is a fact that remains true throughout the algorithm.
        In this algorithm, the invariant is that counts[c] represents the frequency of character c in the prefix of s processed so far minus the frequency of c in the prefix of t processed so far.
        If s and t are anagrams, every character must appear the same number of times in both. Thus, the total increments from s must exactly balance the total decrements from t for every character.
        If any count is non-zero at the end, it means there is a mismatch in frequency, so they cannot be anagrams.
        Since we check all 26 positions, we guarantee no mismatch is missed.

        [STEP_11_EXAMPLE_TRACE]
        Custom teaching example:
        - Input: s = "rat", t = "car"
        - Expected output: False
        - Initial state:
          - len(s) == len(t) == 3 (lengths match, proceed)
          - counts = [0] * 26
        - Iteration 1 (i = 0):
          - s[0] = 'r': index = ord('r') - ord('a') = 17. counts[17] becomes 1.
          - t[0] = 'c': index = ord('c') - ord('a') = 2. counts[2] becomes -1.
        - Iteration 2 (i = 1):
          - s[1] = 'a': index = ord('a') - ord('a') = 0. counts[0] becomes 1.
          - t[1] = 'a': index = ord('a') - ord('a') = 0. counts[0] becomes 0.
        - Iteration 3 (i = 2):
          - s[2] = 't': index = ord('t') - ord('a') = 19. counts[19] becomes 1.
          - t[2] = 'r': index = ord('r') - ord('a') = 17. counts[17] becomes 0.
        - End of loop. counts state:
          - counts[2] = -1 (for 'c')
          - counts[19] = 1 (for 't')
          - All other indices are 0.
        - Scan counts:
          - At index 2, value is -1 (not 0). Return False.

        [STEP_12_CODE_PLAN]
        - Check if len(s) is not equal to len(t). If so, return False.
        - Initialize a list counts of size 26 with all zeros.
        - Loop through the indices of s from 0 to len(s) - 1.
        - In each iteration:
          - Calculate the index for s[i] as ord(s[i]) - ord('a') and increment counts at that index.
          - Calculate the index for t[i] as ord(t[i]) - ord('a') and decrement counts at that index.
        - After the loop, iterate through the values in counts.
        - If any value is not equal to 0, return False.
        - If the loop completes without returning False, return True.

        [STEP_13_IMPLEMENTATION]
        - The code is structured with an early length check to avoid unnecessary work.
        - The single loop processes both strings in parallel, which is highly efficient.
        - ord() is a built-in Python function that returns the Unicode code point of a character. Subtracting ord('a') maps 'a'-'z' to 0-25.
        - The final scan of counts is a simple loop over 26 elements, which is extremely fast and constant time.

        [STEP_14_TEST_CASES]
        Custom test cases:
        - Test Case 1: Representative anagram
          - Input: s = "anagram", t = "nagaram"
          - Expected output: True
          - Validation: Verifies that standard anagrams with multiple repeating characters are correctly identified.
        - Test Case 2: Different lengths
          - Input: s = "ab", t = "abc"
          - Expected output: False
          - Validation: Verifies that the early length check works correctly.
        - Test Case 3: Same characters, different frequencies
          - Input: s = "aabb", t = "abbb"
          - Expected output: False
          - Validation: Verifies that frequency mismatches are caught even when the set of characters is the same.
        - Test Case 4: Single character match
          - Input: s = "a", t = "a"
          - Expected output: True
          - Validation: Verifies the smallest valid input.

        [STEP_15_TIME_COMPLEXITY_DERIVATION]
        - Let n be the length of string s (which is equal to the length of t after the length check).
        - Phase 1: Length comparison len(s) != len(t) takes O(1) time.
        - Phase 2: Initializing the counts array of size 26 takes O(26) = O(1) time.
        - Phase 3: The loop runs exactly n times. In each iteration, we perform:
          - ord(s[i]) and ord(t[i]) which are O(1) operations.
          - Array lookups and updates at the calculated indices, which are O(1) operations.
          - Thus, the loop takes O(n) time in total.
        - Phase 4: Scanning the counts array of size 26 takes O(26) = O(1) time.
        - Total time complexity: O(n) + O(1) = O(n).

        [STEP_16_SPACE_COMPLEXITY_DERIVATION]
        - The counts array is of fixed size 26, which does not depend on the input size n.
        - No other data structures are allocated.
        - The input strings are not copied or mutated.
        - Therefore, the auxiliary space complexity is O(1).
        - Canonical space: O(1).

        [STEP_17_APPROACH_TRADEOFFS]
        - Baseline (S3 - Sorting):
          - Time: O(n log n)
          - Space: O(n)
          - Advantage: Simple to implement, does not require knowing the alphabet size.
          - Disadvantage: Slower and uses more memory.
        - Hash Map (S2):
          - Time: O(n)
          - Space: O(1) (since alphabet is limited to 26 characters)
          - Advantage: More generalizable to arbitrary characters (Unicode) without changing the code structure.
          - Disadvantage: Slightly more overhead due to hash map operations compared to direct array indexing.
        - Preferred (S1 - Fixed Array):
          - Time: O(n)
          - Space: O(1)
          - Advantage: Extremely fast, minimal overhead, constant space.
          - Disadvantage: Hardcoded for lowercase English letters; requires modification if the character set changes.

        [STEP_18_INTERVIEW_COMMUNICATION]
        - Before coding: Restate the problem, clarify constraints (lowercase English letters), mention the sorting baseline, explain why counting is better, and propose the fixed-array approach.
        - While coding: Explain the length check, the mapping of characters to 0-25 using ord(), and the parallel increment/decrement logic.
        - After coding: Trace with a simple example, explain the O(n) time and O(1) space complexity.

        [INTERVIEW_SCRIPT]
        "To solve this problem, I'll first check if the two strings have different lengths. If they do, they can't be anagrams, so I'll return False immediately.
        A simple way to solve this would be to sort both strings and compare them, which would take O(n log n) time. However, we can optimize this to O(n) time by counting character frequencies.
        Since we are guaranteed that the strings only contain lowercase English letters, we can use a fixed-size array of size 26 to keep track of the character counts.
        I will iterate through both strings simultaneously. For each character in s, I'll increment its count in our array, and for each character in t, I'll decrement its count.
        If the strings are anagrams, every increment will be balanced by a decrement, leaving all counts at zero. Finally, I'll scan the array, and if any count is not zero, I'll return False. Otherwise, I'll return True."

        [PATTERN_RECOGNITION]
        - Pattern: Frequency counting with fixed-size arrays.
        - Signals: Problems involving permutations, anagrams, or character counts where the alphabet is small and fixed (e.g., lowercase English letters).
        - Common variations: Finding all anagrams in a string, group anagrams.
        - False-positive signals: If the character set is large or unrestricted (e.g., full Unicode), a fixed array of size 26 is insufficient, and a hash map should be used instead.

        [COMMON_PITFALLS]
        - Forgetting the early length check.
        - Forgetting to subtract ord('a') when indexing the array.
        - Incrementing both counters instead of incrementing for s and decrementing for t.
        - Assuming the fixed array works for any character set without adjusting the size.

        [FINAL_REVIEW_CHECKLIST]
        - Can I restate the problem?
        - Do I know the input, output, and constraints?
        - Do I know what actually needs clarification?
        - Can I explain the sorting baseline?
        - Can I identify its bottleneck?
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

        if len(s) != len(t):
            return False

        counts = [0] * 26

        for i in range(len(s)):
            counts[ord(s[i]) - ord('a')] += 1
            counts[ord(t[i]) - ord('a')] -= 1

        for val in counts:
            if val != 0:
                return False

        return True
