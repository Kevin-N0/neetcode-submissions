class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # Horizontal Scanning
        # Time: O(n * m) <-- O(n~len of shortest str) + O(m~num of strings)
        # Space: 
        # Feedback: 
        # prefix = strs[0]
        # for word_idx in range(1, len(strs)):
        #     j = 0 
        #     while j < min(len(prefix), len(strs[word_idx])):
        #         if strs[word_idx][j] != prefix[j]: 
        #             break 
        #         j += 1
        #     prefix = prefix[:j]
        # return prefix 

        # Vertical Scanning 
        # Time: O(n * m) <-- O(n~len of shortest str) + O(m~num of strs)
        # Space: O(1)
        # base_word = strs[0]
        # for i in range(len(base_word)): 
        #     for s in strs: 
        #         if len(s) == i or s[i] != base_word[i]:
        #             return s[:i]
        # return base_word

        # Sorting 
        if len(strs) == 1: 
            return strs[0]
        
        strs = sorted(strs)
        first_str, last_str = strs[0], strs[-1]
        min_len_str = min(len(first_str), len(last_str))

        for i in range(min_len_str):
            if first_str[i] != last_str[i]: 
                return first_str[:i]
        return first_str










