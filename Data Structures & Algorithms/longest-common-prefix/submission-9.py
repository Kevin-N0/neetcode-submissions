class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # 1. Horizontal Scan: O(N * L), O(1)
        # prefix = strs[0]
        # for i in range(len(strs)):
        #     j = 0 
        #     while j < min(len(prefix), len(strs[i])):
        #         if prefix[j] != strs[i][j]: 
        #             break
        #         j += 1
        #     prefix = prefix[:j]
        # return prefix 



        # 2. Vertical Scan: O(N * L), O(1)
        base_str = strs[0]
        for i in range(len(base_str)):
            for s in strs:
                if i == len(s) or s[i] != base_str[i]:
                    return s[:i]
        return base_str




        # 3. Sorting: O(L * N log N), O()
