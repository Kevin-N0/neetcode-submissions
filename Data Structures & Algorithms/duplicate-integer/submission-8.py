class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        """
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: [CATEGORY_OR_UNKNOWN]
        PREFERRED_SOLUTION: [ S3 ]

        @PROBLEM_DETAILS_START

        PROBLEM: [Contains Duplicate]
        DIFFICULTY: [Easy]

        PROBLEM DETAILS:

        Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

        Example 1:

        Input: nums = [1, 2, 3, 3]

        Output: true

        Example 2:

        Input: nums = [1, 2, 3, 4]

        Output: false
        Constraints:

        0 <= nums.length <= 10^5
        -10^9 <= nums[i] <= 10^9


        @PROBLEM_DETAILS_END
        @CONTENT_START


        [S1]-[BRUTE FORCE]

        INT:
        1. Check every pair of elements & return true if any pair has equal values 
        2. Most intuitive b/c compares all possible pairs 
        3. Least efficient since it examines every combination 

        ALGO:
        1. Iterate through array using 2 nested loops to check all possible pairs of 
        distint indices 
        2. If any pair has same value, return True 
        3. If all pairs are checked and no duplicates are found, return False 

        TIME: O(...)

        1. Let n be [DEFINE THE MAIN INPUT-SIZE VARIABLE].
        2. Let m, k, h, V, E, or another variable be
           [DEFINE ONLY IF NEEDED].
        3. The main operation or operations are [IDENTIFY THE WORK].
        4. These operations occur [STATE HOW MANY TIMES].
        5. Each operation costs [STATE THE COST].
        6. The costs are [NESTED, SEQUENTIAL, RECURSIVE, OR OTHERWISE
           COMBINED], so they are [MULTIPLIED, ADDED, OR EXPRESSED WITH
           A RECURRENCE].
        7. After simplifying, the dominant term is O(...).
        8. Therefore, the [worst-case | expected | average-case | amortized |
           best-case] time complexity is O(...).

        SPACE: O(...)

        1. The algorithm uses [IDENTIFY VARIABLES AND EXTRA DATA STRUCTURES].
        2. The largest growing structure can contain [STATE THE MAXIMUM SIZE].
        3. Additional storage such as copied input, sorting storage,
           memoization, visited state, queues, stacks, heaps, or tables uses
           [O(...) | Not applicable].
        4. The recursion stack uses [O(...) | Not applicable].
        5. The remaining fixed variables use O(1) space.
        6. Required output space is [O(...) | excluded | Not applicable].
        7. The input is [modified | not modified].
        8. Therefore, the auxiliary-space complexity is O(...).


        [S2]-[SORTING]

        INT:
        1. If we sort array, any duplicate values will appear next to each other
        2. Sorting groups identical elements together 
        3. Check adjacent positions to detect duplicates & Single linear scan after sorting 

        ALGO:
        1. Sort array in non-decreasing order
        2. Iterate through array starting from index 1
        3. Compare curreent vs. previous element 
        4. If both elements are equal, return True 
        5. If loop finishes without finding equal neighbors, return False 

        TIME: O(...)

        1. Let n be [DEFINE THE MAIN INPUT-SIZE VARIABLE].
        2. Let m, k, h, V, E, or another variable be
           [DEFINE ONLY IF NEEDED].
        3. The main operation or operations are [IDENTIFY THE WORK].
        4. These operations occur [STATE HOW MANY TIMES].
        5. Each operation costs [STATE THE COST].
        6. The costs are [NESTED, SEQUENTIAL, RECURSIVE, OR OTHERWISE
           COMBINED], so they are [MULTIPLIED, ADDED, OR EXPRESSED WITH
           A RECURRENCE].
        7. After simplifying, the dominant term is O(...).
        8. Therefore, the [worst-case | expected | average-case | amortized |
           best-case] time complexity is O(...).

        SPACE: O(...)

        1. The algorithm uses [IDENTIFY VARIABLES AND EXTRA DATA STRUCTURES].
        2. The largest growing structure can contain [STATE THE MAXIMUM SIZE].
        3. Additional storage such as copied input, sorting storage,
           memoization, visited state, queues, stacks, heaps, or tables uses
           [O(...) | Not applicable].
        4. The recursion stack uses [O(...) | Not applicable].
        5. The remaining fixed variables use O(1) space.
        6. Required output space is [O(...) | excluded | Not applicable].
        7. The input is [modified | not modified].
        8. Therefore, the auxiliary-space complexity is O(...).


        [S3]-[HASHING]

        INT:
        1. Hash set to keep tracke of values already encountered 
        2. Iterate through array --> Check if current value is already prsent in set 
        3. [EXPLAIN THE MAIN BENEFIT, LIMITATION, OR TRADEOFF]

        ALGO:
        1. Initialize empty hash set to store seen values 
        2. Iterate through each number in the array 
        3. For each number
        - if in set, return true because duplicate is found
        - otherwise add to set 
        4. If loop finishes without finding any duplicates, return False 

        TIME: O(...)

        1. Let n be [DEFINE THE MAIN INPUT-SIZE VARIABLE].
        2. Let m, k, h, V, E, or another variable be
           [DEFINE ONLY IF NEEDED].
        3. The main operation or operations are [IDENTIFY THE WORK].
        4. These operations occur [STATE HOW MANY TIMES].
        5. Each operation costs [STATE THE COST].
        6. The costs are [NESTED, SEQUENTIAL, RECURSIVE, OR OTHERWISE
           COMBINED], so they are [MULTIPLIED, ADDED, OR EXPRESSED WITH
           A RECURRENCE].
        7. After simplifying, the dominant term is O(...).
        8. Therefore, the [worst-case | expected | average-case | amortized |
           best-case] time complexity is O(...).

        SPACE: O(...)

        1. The algorithm uses [IDENTIFY VARIABLES AND EXTRA DATA STRUCTURES].
        2. The largest growing structure can contain [STATE THE MAXIMUM SIZE].
        3. Additional storage such as copied input, sorting storage,
           memoization, visited state, queues, stacks, heaps, or tables uses
           [O(...) | Not applicable].
        4. The recursion stack uses [O(...) | Not applicable].
        5. The remaining fixed variables use O(1) space.
        6. Required output space is [O(...) | excluded | Not applicable].
        7. The input is [modified | not modified].
        8. Therefore, the auxiliary-space complexity is O(...).


        [S4]-[OPTIONAL APPROACH NAME]

        INT:
        1. [EXPLAIN THE CENTRAL IDEA]
        2. [EXPLAIN WHY THE IDEA WORKS]
        3. [EXPLAIN THE MAIN BENEFIT, LIMITATION, OR TRADEOFF]

        ALGO:
        1. [DESCRIBE THE INITIAL STATE OR SETUP]
        2. [DESCRIBE THE MAIN PROCESS]
        3. [DESCRIBE THE IMPORTANT CONDITION OR DECISION]
        4. [DESCRIBE HOW THE STATE CHANGES]
        5. [DESCRIBE HOW THE PROCESS CONTINUES]
        6. [DESCRIBE THE RETURN VALUE OR FINAL RESULT]

        TIME: O(...)

        1. Let n be [DEFINE THE MAIN INPUT-SIZE VARIABLE].
        2. Let m, k, h, V, E, or another variable be
           [DEFINE ONLY IF NEEDED].
        3. The main operation or operations are [IDENTIFY THE WORK].
        4. These operations occur [STATE HOW MANY TIMES].
        5. Each operation costs [STATE THE COST].
        6. The costs are [NESTED, SEQUENTIAL, RECURSIVE, OR OTHERWISE
           COMBINED], so they are [MULTIPLIED, ADDED, OR EXPRESSED WITH
           A RECURRENCE].
        7. After simplifying, the dominant term is O(...).
        8. Therefore, the [worst-case | expected | average-case | amortized |
           best-case] time complexity is O(...).

        SPACE: O(...)

        1. The algorithm uses [IDENTIFY VARIABLES AND EXTRA DATA STRUCTURES].
        2. The largest growing structure can contain [STATE THE MAXIMUM SIZE].
        3. Additional storage such as copied input, sorting storage,
           memoization, visited state, queues, stacks, heaps, or tables uses
           [O(...) | Not applicable].
        4. The recursion stack uses [O(...) | Not applicable].
        5. The remaining fixed variables use O(1) space.
        6. Required output space is [O(...) | excluded | Not applicable].
        7. The input is [modified | not modified].
        8. Therefore, the auxiliary-space complexity is O(...).


        [APPROACH_COMPARISON]

        S1:
        - Approach:
        - Time:
        - Time qualification:
        - Space:
        - Input modified: [Yes | No]
        - Main advantage:
        - Main disadvantage:

        S2:
        - Approach:
        - Time:
        - Time qualification:
        - Space:
        - Input modified: [Yes | No]
        - Main advantage:
        - Main disadvantage:

        S3:
        - Approach:
        - Time:
        - Time qualification:
        - Space:
        - Input modified: [Yes | No]
        - Main advantage:
        - Main disadvantage:

        S4:
        - Approach:
        - Time:
        - Time qualification:
        - Space:
        - Input modified: [Yes | No]
        - Main advantage:
        - Main disadvantage:


        [COMMON_PITFALLS]

        1. [PROBLEM-SPECIFIC MISTAKE]
        2. [PROBLEM-SPECIFIC MISTAKE]
        3. [PROBLEM-SPECIFIC MISTAKE]
        4. [OPTIONAL PROBLEM-SPECIFIC MISTAKE]


        @CONTENT_END
        @NC250_END
        """

        # S1 CODE - [Brute Force]:
        # [PASTE OR WRITE THE S1 IMPLEMENTATION HERE]
        # for i in range(len(nums)): 
        #     for j in range(i+1, len(nums)):
        #         if nums[i] == nums[j]: 
        #             return True
        # return False 
                

        # S2 CODE - [Sorting]:
        # nums.sort()
        # for i in range(1, len(nums)): 
        #     if nums[i] == nums[i - 0]: 
        #         return True
        # return False
        

        # S3 CODE - [Hashing]:
        seen = set()
        for num in nums: 
            if num in seen: 
                return True
            seen.add(num)
        return False 


        # S4 CODE - [OPTIONAL APPROACH NAME]:
        # [PASTE OR WRITE THE S4 IMPLEMENTATION HERE]

        # Leave only the preferred solution uncommented and executable.
        



