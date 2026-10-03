# =====================================================================
# PROBLEM 4: Encode and Decode Strings
# =====================================================================

class Solution:
    def encode(self, strs: List[str]) -> str:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing / String Encoding
        PREFERRED_SOLUTION: S2

        @PROBLEM_DETAILS_START

        PROBLEM: Encode and Decode Strings

        URL: https://neetcode.io/problems/string-encode-and-decode/question?list=blind75

        DIFFICULTY: Medium

        PROBLEM DETAILS:

        Design an algorithm to encode a list of strings to a string. The
        encoded string is then sent over the network and is decoded back to
        the original list of strings.

        Machine 1 (sender) has the function:

        String encode(List<String> strs) {
            // ... your code
            return encoded_string;
        }

        Machine 2 (receiver) has the function:

        List<String> decode(String encoded_string) {
            // ... your code
            return decoded_strs;
        }

        decoded_strs in Machine 2 should be the same as the input strs in
        Machine 1.

        Implement the encode and decode methods.

        Example 1:

        Input:
        strs = ["Hello","World"]

        Output:
        ["Hello","World"]

        Explanation:
        The encoded string is transmitted from Machine 1 to Machine 2 and
        decoded back into the original list.

        Example 2:

        Input:
        strs = [""]

        Output:
        [""]

        Constraints:

        - 0 <= strs.length < 100
        - 0 <= strs[i].length < 200
        - strs[i] contains any possible characters out of 256 valid ASCII
          characters.

        Follow up:
        Could you write a generalized algorithm to work on any possible set of
        characters?

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Encoding & Decoding

        INT:

        Store all string lengths first, separated by commas, terminate the
        length section with '#', and then append the string payloads. During
        decoding, parse the recorded lengths and use them to slice exact
        string boundaries.

        ALGO:

        Encoding:
        1. Return "" for an empty input list.
        2. Record every string length.
        3. Write each length followed by ','.
        4. Append '#'.
        5. Append all original strings.

        Decoding:
        1. Return [] for an empty encoded string.
        2. Parse lengths until '#'.
        3. Starting after '#', extract exactly each recorded number of
           characters.

        TIME: O(m + n)

        Each character and each length entry is processed linearly.

        SPACE: O(m + n)

        The encoded/decoded output plus recorded sizes require linear space.


        [S2]-Encoding & Decoding (Optimal)

        INT:

        Prefix each string directly as length#string. During decoding, read
        digits until '#', convert them to the string length, then consume
        exactly that many characters. Because boundaries come from lengths,
        delimiter characters inside the original content are harmless.

        ALGO:

        Encoding:
        1. For every string, append its decimal length.
        2. Append '#'.
        3. Append the string itself.
        4. Join all parts.

        Decoding:
        1. Start at i = 0.
        2. Move j until '#'.
        3. Parse s[i:j] as the length.
        4. Move i after '#'.
        5. Slice the next length characters.
        6. Repeat until the encoded string is exhausted.

        TIME: O(m + n)

        Each encoded character is written/read a constant number of times.

        SPACE: O(m + n)

        The constructed encoded string or decoded output is linear in the
        total content size.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Separate length header followed by concatenated payload.
        - Time: O(m + n)
        - Space: O(m + n)
        - Input modified: No
        - Main advantage: Explicitly separates metadata from payload.
        - Main disadvantage: Requires a separate sizes section and extra
          parsing state.

        S2:

        - Approach: Repeated length#string segments.
        - Time: O(m + n)
        - Space: O(m + n)
        - Input modified: No
        - Main advantage: Simple streaming-style format with unambiguous
          boundaries.
        - Main disadvantage: Decoder must correctly parse multi-digit lengths.

        [COMMON_PITFALLS]

        - A plain delimiter alone is unsafe because that delimiter may appear
          in the original strings.
        - Preserve the distinction between [] and [""].
        - Parse the full numeric prefix, not just one digit.

        [SOURCE_NOTES]

        - Active submitted implementation uses S2.
        - Length-prefixing makes the content itself irrelevant to boundary
          detection.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        res = []
        for s in strs:
            res.append(str(len(s)))
            res.append("#")
            res.append(s)
        return "".join(res)

    def decode(self, s: str) -> List[str]:
        res = []
        i = 0

        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            i = j + 1
            j = i + length
            res.append(s[i:j])
            i = j

        return res

    # -----------------------------------------------------------------
    # OPTIONAL ALTERNATE / OLD ATTEMPTS
    # -----------------------------------------------------------------
    #
    # S1 CODE - Encoding & Decoding
    #
    # def encode_s1(self, strs: List[str]) -> str:
    #     if not strs:
    #         return ""
    #     sizes, res = [], []
    #     for s in strs:
    #         sizes.append(len(s))
    #     for sz in sizes:
    #         res.append(str(sz))
    #         res.append(',')
    #     res.append('#')
    #     res.extend(strs)
    #     return ''.join(res)
    #
    # def decode_s1(self, s: str) -> List[str]:
    #     if not s:
    #         return []
    #     sizes, res, i = [], [], 0
    #     while s[i] != '#':
    #         j = i
    #         while s[j] != ',':
    #             j += 1
    #         sizes.append(int(s[i:j]))
    #         i = j + 1
    #     i += 1
    #     for sz in sizes:
    #         res.append(s[i:i + sz])
    #         i += sz
    #     return res
