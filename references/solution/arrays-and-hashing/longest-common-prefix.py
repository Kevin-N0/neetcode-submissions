from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        """
        @NC250_START

        TYPE: SOLUTION_REFERENCE
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

        [S1]-[Horizontal Scanning]

        INT:
        Find the longest common prefix of the first two strings, then use that prefix to find the common prefix with the third string, and so on. If at any point the prefix becomes empty, we can return immediately.

        ALGO:
        1. If the input list `strs` is empty, return an empty string.
        2. Initialize `prefix` as the first string `strs[0]`.
        3. Iterate through the remaining strings in `strs` from index 1 to the end.
        4. For each string, compare characters with `prefix` up to the minimum length of both.
        5. Update `prefix` to be the common prefix found.
        6. If `prefix` becomes empty, return `""`.
        7. Return `prefix` after checking all strings.

        TIME: O(n * m) where n is the number of strings and m is the average length of the strings. In the worst case, we compare all characters of all strings.
        SPACE: O(1) auxiliary space, as we only store the prefix and indices.

        [S2]-[Vertical Scanning]

        INT:
        Compare characters of all strings column by column (vertically). We check the first character of all strings, then the second character, and so on. This allows us to terminate early as soon as a mismatch is found or we reach the end of any string.

        ALGO:
        1. If the input list `strs` is empty, return an empty string.
        2. Take the first string `strs[0]` as the base word.
        3. Iterate through each character index `i` of the base word.
        4. For each index, iterate through all strings in `strs`.
        5. If the current string's length is equal to `i` (meaning we reached its end) or the character at index `i` does not match the base word's character at index `i`, return the substring of the base word from index 0 to `i`.
        6. If the loop completes without any mismatch, return the entire base word.

        TIME: O(n * m) where n is the number of strings and m is the length of the shortest string. In the worst case, we scan all characters of all strings.
        SPACE: O(1) auxiliary space, as we only use indices for comparison.

        [S3]-[Sorting]

        INT:
        By sorting the list of strings lexicographically, the most different strings will be placed at the first and last positions of the sorted array. Therefore, the longest common prefix of the entire array must be the common prefix between the first and the last strings.

        ALGO:
        1. If the input list `strs` has only 1 string, return it.
        2. Sort the list of strings lexicographically.
        3. Retrieve the first string `first_str` and the last string `last_str` from the sorted list.
        4. Find the minimum length between `first_str` and `last_str`.
        5. Iterate through the characters of both strings up to the minimum length.
        6. If a mismatch is found at index `i`, return the substring of `first_str` from index 0 to `i`.
        7. If no mismatch is found, return the prefix up to the minimum length (which is `first_str` itself or a prefix of it).

        TIME: O(n * m * log n) where n is the number of strings and m is the maximum length of a string. Sorting n strings of length m takes O(m * n log n) time because string comparison takes O(m) time.
        SPACE: O(n * m) auxiliary space to store the sorted copy of the strings.

        [APPROACH_COMPARISON]
        - Approach: S1
          Time: O(n * m)
          Time qualification: n is the number of strings, m is the average length of the strings
          Space: O(1)
          Input modified: No
          Main advantage: Simple horizontal scanning logic
          Main disadvantage: May perform redundant comparisons if the prefix is long but mismatch occurs late

        - Approach: S2
          Time: O(n * m)
          Time qualification: n is the number of strings, m is the length of the shortest string
          Space: O(1)
          Input modified: No
          Main advantage: Early termination on mismatch, optimal for most cases
          Main disadvantage: Requires nested loops over all strings for each character index

        - Approach: S3
          Time: O(n * m * log n)
          Time qualification: n is the number of strings, m is the maximum length of a string
          Space: O(n * m)
          Input modified: No
          Main advantage: Only compares two strings (first and last) after sorting
          Main disadvantage: Sorting all strings is less efficient than linear scanning

        [COMMON_PITFALLS]
        - Empty input list: If the input list is empty, accessing `strs[0]` will raise an IndexError. Always check if the list is empty first (though constraints say `strs.length >= 1`).
        - Out of bounds index: In vertical scanning, we must ensure we do not access an index beyond the length of any string. Checking `len(s) == i` prevents this.
        - Modifying the input: Sorting the input list modifies the original list in-place if using `strs.sort()`, or creates a sorted copy with `sorted(strs)`. Be aware of whether in-place mutation is acceptable.
        - Single string input: If the input list contains only one string, the common prefix is the string itself. The algorithm should handle this case correctly.

        @CONTENT_END

        @NC250_END
        """
        # # S1 - Horizontal Scanning
        # if not strs:
        #     return ""
        # prefix = strs[0]
        # for word_idx in range(1, len(strs)):
        #     j = 0 
        #     while j < min(len(prefix), len(strs[word_idx])):
        #         if strs[word_idx][j] != prefix[j]: 
        #             break 
        #         j += 1
        #     prefix = prefix[:j]
        # return prefix 

        # # S2 - Vertical Scanning 
        # if not strs:
        #     return ""
        # base_word = strs[0]
        # for i in range(len(base_word)): 
        #     for s in strs: 
        #         if len(s) == i or s[i] != base_word[i]:
        #             return s[:i]
        # return base_word

        # S3 - Sorting 
        if len(strs) == 1: 
            return strs[0]
        
        strs = sorted(strs)
        first_str, last_str = strs[0], strs[-1]
        min_len_str = min(len(first_str), len(last_str))

        for i in range(min_len_str):
            if first_str[i] != last_str[i]: 
                return first_str[:i]
        return first_str
