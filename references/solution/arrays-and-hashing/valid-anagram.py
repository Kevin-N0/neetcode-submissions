class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        @NC250_START

        TYPE: SOLUTION_REFERENCE
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

        [S1]-[Fixed Array Frequency Count]

        INT:
        Since the problem guarantees that s and t contain only lowercase English letters, there are only 26 possible characters. We can use a fixed-size array of 26 counters to track the difference between the character frequencies in s and t.
        First, if the strings have different lengths, they cannot be anagrams, so we can immediately return False.
        Otherwise, we process both strings together. For each character from s, we increment its corresponding counter. For each character from t, we decrement its corresponding counter.
        If the two strings contain exactly the same frequency of every lowercase letter, every increment caused by s will be canceled by a corresponding decrement caused by t. Therefore, after processing both strings, every value in the counts array should be zero. If any counter is nonzero, the strings are not anagrams.

        ALGO:
        1. Compare the lengths of s and t. If they are different, return False.
        2. Create an array counts containing 26 zeros.
        3. Iterate through every index i from 0 to len(s) - 1.
        4. Convert s[i] into an index from 0 through 25 using ord(s[i]) - ord('a') and increment that position in counts.
        5. Convert t[i] into an index from 0 through 25 using ord(t[i]) - ord('a') and decrement that position in counts.
        6. Scan the 26 values in counts. If any value is not zero, return False.
        7. If every value is zero, return True.

        TIME: O(n)
        - n: length of string s (which equals the length of t after validation).
        - Comparing lengths takes O(1) time.
        - The main loop runs n times, performing O(1) array updates per iteration.
        - Scanning the counts array takes O(26) = O(1) time.
        - Total time complexity is O(n).

        SPACE: O(1)
        - The counts array always contains exactly 26 integers because the problem guarantees that the strings contain only lowercase English letters.
        - The size of this array does not grow as s or t become larger.
        - Auxiliary space complexity is O(1).

        [S2]-[Hash Map Counter]

        INT:
        Instead of using fixed array positions, we can build a frequency map for each string. The key is the character and the value is the number of times that character appears.
        First, if the strings have different lengths, return False.
        Then, process both strings and build countS and countT.
        After all characters have been counted, the strings are anagrams if and only if the two dictionaries are equal. Dictionary equality verifies that both mappings contain the same keys with the same associated counts.

        ALGO:
        1. Compare the lengths of s and t. If they are different, return False.
        2. Create empty dictionaries countS and countT.
        3. Iterate through every index in the strings.
        4. Increment the frequency of s[i] in countS.
        5. Increment the frequency of t[i] in countT.
        6. Compare countS and countT.
        7. Return whether the two dictionaries are equal.

        TIME: O(n)
        - n: length of string s (which equals the length of t after validation).
        - Every character in the strings is processed once while constructing the frequency dictionaries.
        - Dictionary lookups and updates are expected O(1).
        - Comparing the two dictionaries requires checking their stored entries, which is bounded by the size of the alphabet.
        - Total expected time complexity is O(n).

        SPACE: O(1)
        - The problem guarantees that s and t contain only lowercase English letters.
        - Therefore, each dictionary can contain at most 26 distinct keys.
        - Since 26 is a fixed constant independent of the input length, the auxiliary space is O(1).

        [S3]-[Sorting]

        INT:
        Anagrams contain exactly the same characters with exactly the same frequencies. Sorting both strings places their characters into a canonical order.
        Therefore, if s and t are anagrams, their sorted representations will be identical. If their sorted representations are different, then at least one character or character frequency differs.

        ALGO:
        1. Compare the lengths of s and t. If they are different, return False.
        2. Sort the characters in s.
        3. Sort the characters in t.
        4. Compare the two sorted results.
        5. Return whether they are equal.

        TIME: O(n log n)
        - n: length of string s (which equals the length of t after validation).
        - Sorting s requires O(n log n) time.
        - Sorting t requires O(n log n) time.
        - Comparing the two sorted sequences of length n requires O(n) time.
        - Total time complexity is O(n log n).

        SPACE: O(n)
        - In Python, sorted(s) and sorted(t) each create a new list containing the characters from the corresponding string.
        - The resulting lists require space proportional to the sizes of s and t.
        - Therefore, the auxiliary space is O(n).

        [APPROACH_COMPARISON]

        - Approach: S1
          Time: O(n)
          Time qualification: Linear scan of both strings.
          Space: O(1)
          Input modified: No
          Main advantage: Uses constant auxiliary space and only one small frequency structure.
          Main disadvantage: Relies on the problem's guarantee that all characters are lowercase English letters.

        - Approach: S2
          Time: O(n)
          Time qualification: Expected linear time for dictionary construction and comparison.
          Space: O(1)
          Input modified: No
          Main advantage: Frequency counting is explicit and does not require manual character-to-array-index conversion.
          Main disadvantage: Uses hash-map machinery and two separate frequency structures when the alphabet is already known and fixed.

        - Approach: S3
          Time: O(n log n)
          Time qualification: Dominated by sorting both strings.
          Space: O(n)
          Input modified: No
          Main advantage: Very concise and directly converts anagram checking into an equality comparison.
          Main disadvantage: Sorting is asymptotically slower than direct frequency counting and requires linear auxiliary space in Python.

        [COMMON_PITFALLS]
        - Forgetting to check whether s and t have different lengths before doing additional work.
        - Forgetting that anagrams require both the same characters and the same frequency of each character.
        - Incrementing both strings' counters in the fixed-array approach instead of incrementing for s and decrementing for t.
        - Using ord(s[i]) directly as an array index instead of subtracting ord('a').
        - Creating an incorrectly sized frequency array instead of one with 26 positions for the lowercase English alphabet.
        - Returning True before checking that every frequency-difference value has returned to zero.
        - Forgetting to use a default count such as 0 when a dictionary key has not appeared before.
        - Comparing only the keys of countS and countT instead of their complete character-to-frequency mappings.
        - Claiming the hash-map approach requires O(n) space for this specific problem without accounting for the constraint that there are only 26 possible lowercase characters.
        - Claiming Python's sorted() version uses O(1) auxiliary space even though sorted() creates new lists.
        - Assuming the fixed-array approach works unchanged for arbitrary Unicode characters or a larger unrestricted alphabet.

        @CONTENT_END

        @NC250_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

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

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S2 CODE - Hash Map Counter
        #
        # if len(s) != len(t):
        #     return False
        #
        # countS, countT = {}, {}
        #
        # for i in range(len(s)):
        #     countS[s[i]] = 1 + countS.get(s[i], 0)
        #     countT[t[i]] = 1 + countT.get(t[i], 0)
        #
        # return countS == countT
        #
        #
        # S3 CODE - Sorting
        #
        # if len(s) != len(t):
        #     return False
        #
        # return sorted(s) == sorted(t)
