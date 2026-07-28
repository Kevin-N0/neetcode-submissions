class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict
        #anagram_dict = defaultdict(list)
        #for s in strs: 
        #    sorted_s = ''.join(sorted(s))
        #    anagram_dict[sorted_s].append(s)
        #return anagram_dict.values()

        anagram_dict = defaultdict(list)
        
        for s in strs: 
            counts = [0] * 26
            for c in s: 
                counts[ord(c) - ord('a')] += 1 
            anagram_dict[tuple(counts)].append(s)
        return anagram_dict.values()
            


        