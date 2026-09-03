class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # 1. Horizontal Scan: O(), O()
        prefix = strs[0]

        for i in range(1, len(strs)): 
            j = 0 
            while j < min(len(prefix), len(strs[i])):
                if prefix[j] != strs[i][j]:
                    break
                j += 1
            prefix = prefix[:j]
        return prefix




        # 2. Vertical Scan: O(), O()


        

        # 3. Sorting: O(), O()
