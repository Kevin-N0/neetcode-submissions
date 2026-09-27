class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: Fixed Array Frequency Count

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

        Since the problem guarantees that s and t contain only lowercase
        English letters, there are only 26 possible characters.

        Use one fixed-size array of 26 counters to track the difference between
        the character frequencies in s and t.

        First, if the strings have different lengths, they cannot be anagrams.
        Anagrams must contain the same total number of characters because every
        character must appear the same number of times in both strings.

        Then process both strings together.

        For each character from s, increment its corresponding counter.

        For each character from t, decrement its corresponding counter.

        If the two strings contain exactly the same frequency of every
        lowercase letter, every increment caused by s will be canceled by a
        corresponding decrement caused by t.

        Therefore, after processing both strings, every value in the counts
        array should be zero.

        If any counter is nonzero, one of the characters appeared a different
        number of times, so the strings are not anagrams.


        ALGO:

        1. Compare the lengths of s and t.
        2. If their lengths are different, return False.
        3. Create an array counts containing 26 zeros.
        4. Iterate through every index in s and t.
        5. Convert s[i] into an index from 0 through 25 using:
           ord(s[i]) - ord('a').
        6. Increment that position in counts.
        7. Convert t[i] into an index from 0 through 25 using:
           ord(t[i]) - ord('a').
        8. Decrement that position in counts.
        9. Scan the 26 values in counts.
        10. If any value is not zero, return False.
        11. If every value is zero, return True.


        TIME: O(n + m)

        Let:

        n = len(s)
        m = len(t)

        The initial length comparison is constant time.

        If the lengths differ, the algorithm immediately returns False.

        Otherwise, s and t have the same length and the main loop processes
        each position once.

        Processing the characters therefore requires linear time.

        The final scan always checks exactly 26 counters:

        O(26) = O(1)

        Therefore the total runtime can be written as:

        O(n + m)

        Since valid candidates must have n = m after the length check, this can
        also be simplified to O(n).


        SPACE: O(1)

        The counts array always contains exactly 26 integers because the
        problem guarantees that the strings contain only lowercase English
        letters.

        The size of this array does not grow as s or t become larger.

        Therefore the auxiliary space complexity is O(1).



        [S2]-[Hash Map Counter]

        INT:

        Instead of using fixed array positions for the 26 lowercase letters,
        build a frequency map for each string.

        The key is the character and the value is the number of times that
        character appears.

        First, if the strings have different lengths, return False because they
        cannot contain identical character frequencies.

        Then process both strings and build countS and countT.

        After all characters have been counted, the strings are anagrams if and
        only if the two dictionaries are equal.

        Dictionary equality verifies that both mappings contain the same keys
        with the same associated counts.


        ALGO:

        1. Compare the lengths of s and t.
        2. If their lengths are different, return False.
        3. Create empty dictionaries countS and countT.
        4. Iterate through every index in the strings.
        5. Increment the frequency of s[i] in countS.
        6. Increment the frequency of t[i] in countT.
        7. Compare countS and countT.
        8. Return whether the two dictionaries are equal.


        TIME: O(n + m)

        Every character in the strings is processed once while constructing the
        frequency dictionaries.

        Dictionary lookups and updates are expected O(1).

        Comparing the two dictionaries requires checking their stored entries.

        Therefore the expected total runtime is O(n + m).

        Since the length check guarantees n = m before the main work begins,
        this can also be simplified to O(n).


        SPACE: O(1)

        The problem guarantees that s and t contain only lowercase English
        letters.

        Therefore each dictionary can contain at most 26 distinct keys.

        Since 26 is a fixed constant independent of the input length, the
        auxiliary space is O(1).

        If the alphabet were not fixed, this approach would instead generally
        be described as O(k), where k is the number of distinct characters.



        [S3]-[Sorting]

        INT:

        Anagrams contain exactly the same characters with exactly the same
        frequencies.

        Sorting both strings places their characters into a canonical order.

        Therefore, if s and t are anagrams, their sorted representations will
        be identical.

        If their sorted representations are different, then at least one
        character or character frequency differs.


        ALGO:

        1. Compare the lengths of s and t.
        2. If their lengths are different, return False.
        3. Sort the characters in s.
        4. Sort the characters in t.
        5. Compare the two sorted results.
        6. Return whether they are equal.


        TIME: O(n log n + m log m)

        Sorting s requires:

        O(n log n)

        Sorting t requires:

        O(m log m)

        Comparing the two sorted sequences requires linear time.

        Therefore:

        O(n log n + m log m)

        Since anagrams must have equal-length strings, when n = m this can also
        be simplified to:

        O(n log n)


        SPACE: O(n + m)

        In this Python implementation, sorted(s) and sorted(t) each create a
        new list containing the characters from the corresponding string.

        The resulting lists require space proportional to the sizes of s and t.

        Therefore the auxiliary space for this implementation is O(n + m).

        Some sorting algorithms in other languages or implementations may have
        different auxiliary-space characteristics, which is why sorting space
        is sometimes described differently.



        [APPROACH_COMPARISON]

        S1:

        - Approach: Use one fixed array of 26 counters and track the frequency
          difference between s and t.
        - Time: O(n + m), or O(n) after equal-length validation.
        - Space: O(1)
        - Input modified: No
        - Main advantage: Uses constant auxiliary space and only one small
          frequency structure.
        - Main disadvantage: Relies on the problem's guarantee that all
          characters are lowercase English letters.

        S2:

        - Approach: Build separate character-frequency dictionaries for s and t
          and compare them.
        - Time: O(n + m) expected.
        - Space: O(1) because the problem limits the alphabet to 26 lowercase
          English letters.
        - Input modified: No
        - Main advantage: Frequency counting is explicit and does not require
          manual character-to-array-index conversion.
        - Main disadvantage: Uses hash-map machinery and two separate frequency
          structures when the alphabet is already known and fixed.

        S3:

        - Approach: Sort both strings and compare the sorted results.
        - Time: O(n log n + m log m)
        - Space: O(n + m) for Python's sorted() results.
        - Input modified: No
        - Main advantage: Very concise and directly converts anagram checking
          into an equality comparison.
        - Main disadvantage: Sorting is asymptotically slower than direct
          frequency counting.



        [COMMON_PITFALLS]

        - Forgetting to check whether s and t have different lengths before
          doing additional work.
        - Forgetting that anagrams require both the same characters and the
          same frequency of each character.
        - Incrementing both strings' counters in the fixed-array approach
          instead of incrementing for s and decrementing for t.
        - Using ord(s[i]) directly as an array index instead of subtracting
          ord('a').
        - Creating an incorrectly sized frequency array instead of one with 26
          positions for the lowercase English alphabet.
        - Returning True before checking that every frequency-difference value
          has returned to zero.
        - Forgetting to use a default count such as 0 when a dictionary key has
          not appeared before.
        - Comparing only the keys of countS and countT instead of their complete
          character-to-frequency mappings.
        - Claiming the hash-map approach requires O(n) space for this specific
          problem without accounting for the constraint that there are only 26
          possible lowercase characters.
        - Claiming Python's sorted() version uses O(1) auxiliary space even
          though sorted() creates new lists.
        - Assuming the fixed-array approach works unchanged for arbitrary
          Unicode characters or a larger unrestricted alphabet.



        [SOURCE_NOTES]

        The active submitted implementation uses the fixed-array frequency-count
        approach.

        The problem guarantees that:

        - 1 <= s.length, t.length <= 5 * 10^4
        - s and t contain only lowercase English letters.

        The lowercase-English-letter constraint is important because it makes
        the fixed array of 26 counters sufficient for representing every
        possible character.

        The active implementation increments the counter corresponding to each
        character in s and decrements the counter corresponding to each
        character in t.

        If the strings are anagrams, the frequency contribution from s and t
        cancels out for every character and the final counts array contains
        only zeros.

        The active approach is labeled:

        - Time: O(n + m)
        - Space: O(1)

        A hash-map frequency-counter approach is included as an alternative.

        Because this problem restricts the alphabet to 26 lowercase English
        letters, the dictionaries can contain at most 26 distinct keys.
        Therefore the source's O(1) space classification is appropriate for
        this specific problem.

        The hash-map approach is labeled:

        - Time: O(n + m)
        - Space: O(1)

        A sorting-based approach is also included.

        The sorting approach is labeled:

        - Time: O(n log n + m log m)
        - Space: O(1) or O(n + m)

        For the actual Python implementation shown below, sorted() creates new
        lists, so O(n + m) auxiliary space is the appropriate implementation-
        specific description.

        The submitted / preferred implementation is S1: Fixed Array Frequency
        Count.

        Prompt 1 may reconcile remaining wording and documentation details while
        preserving the actual implementations and problem constraints.

        @CONTENT_END
        @NC250_RAW_END
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