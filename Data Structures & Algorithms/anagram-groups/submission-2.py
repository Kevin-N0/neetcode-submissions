class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict
        anagram_dict = defaultdict(list)

        for s in strs: 
            sorted_s = ''.join(sorted(s))
            if sorted_s in anagram_dict: 
                anagram_dict[sorted_s].append(s)
            else: 
                anagram_dict[sorted_s] = s 
        return anagram_dict


        