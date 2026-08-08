class Solution:
    def getConcatenation(self, nums:List[int]) -> List[int]: 
        """
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: [CATEGORY_OR_UNKNOWN]
        PREFERRED_SOLUTION: [S1 | S2 | S3 | S4]

        @PROBLEM_DETAILS_START

        PROBLEM: [Concatenation of Array]
        DIFFICULTY: [Easy]

        PROBLEM DETAILS:
    
        You are given an integer array nums of length n. Create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for 0 <= i < n (0-indexed).

        Specifically, ans is the concatenation of two nums arrays.

        Return the array ans.

        Example 1:

        Input: nums = [1,4,1,2]

        Output: [1,4,1,2,1,4,1,2]
        Example 2:

        Input: nums = [22,21,20,1]

        Output: [22,21,20,1,22,21,20,1]
        Constraints:

        1 <= nums.length <= 1000.
        1 <= nums[i] <= 1000



        @PROBLEM_DETAILS_END
        @CONTENT_START


        [S1]-[APPROACH NAME]

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


        [S2]-[APPROACH NAME]

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


        [S3]-[APPROACH NAME]

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

        # S1 CODE - [Iteration (Two Pass)]:
        ans = []
        for i in range(2):
            for num in nums:  
                ans.append(num)
        return ans 

        # S2 CODE - [Iteration (One Pass)]:
        # [PASTE OR WRITE THE S2 IMPLEMENTATION HERE]

        # S3 CODE - [APPROACH NAME]:
        # [PASTE OR WRITE THE S3 IMPLEMENTATION HERE]

        # S4 CODE - [OPTIONAL APPROACH NAME]:
        # [PASTE OR WRITE THE S4 IMPLEMENTATION HERE]

        # Leave only the preferred solution uncommented and executable.
        raise NotImplementedError
 