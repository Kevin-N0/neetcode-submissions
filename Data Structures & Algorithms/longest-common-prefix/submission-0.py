class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # Horizontal Scanning
        # Time: O(n * m) <-- O(n~len of shortest str) + O(m~num of strings)
        # Space: 
        # Feedback: 
        # prefix = strs[0]
        # for i in range(1, len(strs)): 
        #     j = 0 
        #     while j < min(len(prefix), len(strs[i])): 
        #         if prefix[j] != strs[i][j]: 
        #             break 
        #         j += 1 
        #         prefix = prefix[:j]
        # return prefix


        # Vertical Scanning 
        base_word = strs[0]
        for i in range(len(base_word)): 
            for s in strs: 
                if len(s) == i or s[i] != base_word[i]:
                    return s[:i]
        return base_word





        # Sorting 