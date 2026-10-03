from collections import defaultdict, deque
from typing import List, Optional, Dict, Set, Tuple
import heapq



# =====================================================================
# PROBLEM 2: Group Anagrams
# =====================================================================

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S2

        @PROBLEM_DETAILS_START

        PROBLEM: Group Anagrams

        URL: https://neetcode.io/problems/anagram-groups/question?list=blind75

        DIFFICULTY: Medium

        PROBLEM DETAILS:

        Given an array of strings strs, group all anagrams together into
        sublists. You may return the output in any order.

        An anagram is a string that contains the exact same characters as
        another string, but the order of the characters can be different.

        Example 1:

        Input:
        strs = ["act","pots","tops","cat","stop","hat"]

        Output:
        [["hat"],["act", "cat"],["stop", "pots", "tops"]]

        Example 2:

        Input:
        strs = ["x"]

        Output:
        [["x"]]

        Example 3:

        Input:
        strs = [""]

        Output:
        [[""]]

        Constraints:

        - 1 <= strs.length <= 10000
        - 0 <= strs[i].length <= 100
        - strs[i] is made up of lowercase English letters.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Sorting

        INT:

        Anagrams become identical after their characters are sorted. Use each
        sorted string as a hash-map key and collect all original strings that
        share that key.

        ALGO:

        1. Create a map from sorted-string key to list of strings.
        2. Sort each input string's characters.
        3. Append the original string to the corresponding group.
        4. Return all grouped values.

        TIME: O(m * n log n)

        Each of m strings may require sorting up to n characters.

        SPACE: O(m * n)

        The grouping structure stores the input strings and generated keys.


        [S2]-Hash Table / Character Frequency

        INT:

        Because inputs contain only lowercase English letters, each string can
        be represented by a 26-entry character-frequency vector. Two strings
        are anagrams exactly when these vectors are equal. Convert the vector
        to a tuple so it can be used as a dictionary key.

        ALGO:

        1. Create a defaultdict(list).
        2. For each string, initialize a 26-entry zero array.
        3. Count each character at index ord(c) - ord('a').
        4. Convert the count array to a tuple.
        5. Append the string to the group for that tuple.
        6. Return the map values as a list.

        TIME: O(m * n)

        Every character is counted once.

        SPACE: O(m) auxiliary, O(m * n) including output

        The hash map stores frequency keys and grouped strings.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Sort each string and group by its sorted form.
        - Time: O(m * n log n)
        - Space: O(m * n)
        - Input modified: No
        - Main advantage: Simple normalization rule.
        - Main disadvantage: Sorting every string adds a log n factor.

        S2:

        - Approach: Group by a 26-character frequency tuple.
        - Time: O(m * n)
        - Space: O(m) auxiliary, O(m * n) including output
        - Input modified: No
        - Main advantage: Linear work in the total number of characters.
        - Main disadvantage: Relies on the lowercase-English-letter constraint.

        [COMMON_PITFALLS]

        - A list cannot be used directly as a dictionary key; convert the
          frequency array to a tuple.
        - The 26-slot frequency method assumes lowercase English letters.
        - If frequency counts are serialized manually, separators are needed
          to avoid key collisions.

        [SOURCE_NOTES]

        - Active submitted implementation uses S2.
        - The source explicitly identifies tuple(count) as the safe immutable
          hash key.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        res = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s)
        return list(res.values())

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Sorting
        #
        # res = defaultdict(list)
        # for s in strs:
        #     sortedS = ''.join(sorted(s))
        #     res[sortedS].append(s)
        # return list(res.values())