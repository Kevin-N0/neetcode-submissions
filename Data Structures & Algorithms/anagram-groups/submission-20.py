class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            sorted_s = ''.join(sorted(s))
            res[sorted_s].append(s)
        return list(res.values())
        # 1. Brute Force
        # Time: 
        # Space: 

        # 2. Optimal: 
        # Time: 
        # Space: 

        
        """
        1. Brute Force 
        m strings, n length of string
            1a. Total Time: O(m * n log n)
                = m X (n log n + n + 1) 
                = m * n log n + m * n + m
                = O(m * n log n)
                When n grows, (m * n log n) grows faster than (m * n); dropping lower order terms. 
        
            1b. Time Summed:
                X m: loop through all m strings
                X n: 
                + n log n (sorting strings: max length n, takes n log n comparisons)
                + n (steps to construct sorted string)
                + 1 (steps on avg. for hash lookup & list append)
                    
        1b. Space: O(m * n)
            b1. Total Space: O(m * n)
            
            
            b2. Space Summed: 
            - Auxiliary Space (Working Mem.)

            

        """
