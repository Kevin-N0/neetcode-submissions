class Solution:
    def getConcatenation(self, nums:List[int]) -> List[int]: 

      """
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: [S1 | S2 | S3 | S4]

        @PROBLEM_DETAILS_START

        PROBLEM: Concatenation of Array
]
        URL: https://neetcode.io/problems/concatenation-of-array/solution
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


        [S1]-Iteration (Two Pass)

        INT:
        To concatenate an array with itself, we
need to create a new array that contains
all elements of the original array twice,
maintaining the same order. The
elements at indices 0 to n — 1 are
followed by the same elements at
indices n to 2n — 1.
For example, if nums = [1, 2, 3] :
• The first three elements of ans will
be nums [0] , nums [1] , nums [2]
> 11, 2, 3]
• The next three elements of ans will
also be nums [0], nums [1],
nums [2] -> [1, 2, 3]
• Result: [1, 2, 3, 1, 2, 3]


        ALGO:
        Initialize an empty result list or an array ans of size 2n, where n is the length of the input array.
Use a loop that runs twice.
Inside that loop, iterate through every element num in the input array nums.
Append num to the result list or assign it to the next available index in the result array.
Return the resulting array.



        TIME: O(...)


        Time complexity: O(n) where n is
the length of the input array. We
iterate through the array twice,
performing 2n operations.
Space complexity: O(n) if we
consider the space required for the
output array of size 2n.

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


        [S2]-Iteration (One Pass)

The problem defines the result array
ans such that ans [i] == nums [il
and ans [i + n] == nums[il for 0 <=
i < n. Instead of looping through the
input twice, we can fill both required
positions in the result array
simultaneously while iterating through
the input array just once. This utilizes
the index mapping i and i + n
directly.

        ALGO:
1. Determine the length n of the input
array.
2. Initialize a result array ans of size
2n.
3. Iterate through the input array
nums using an index i from 0 to
n - 1.
4. For each element at index i :

• Set ans [i] = nums [il .
• Set ans [i + n] = nums[il .

5. Return the resulting array.

        TIME: O(...)
• Time complexity: O(n) where n is
the length of the input array.
Although we iterate through the
input once, we still perform 2n total
writes to the output array.
• Space complexity: O(n) as we must
allocate an array of size 2n for the
output.



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

Incorrect Result Array
Size
Allocating an array of size n instead of
2n causes an index out of bounds error
when writing to the second half.

Off-by-One When Using
Index Offset
When using the one-pass approach with
ans li + n] = nums [il, forgetting that
indices are zero-based or miscalculating
the offset leads to incorrect placement
of elements in the second half.


      @CONTENT_END
      @NC250_END
      """


      # S1 CODE - Iteration (Two Pass):
      # ans = []
      # for i in range(2): 
      #    for num in nums: 
      #       ans.append(num)
      # return ans

      # S2 CODE - Iteration (One Pass)
      n = len(nums)
      ans = [0] * (2 * n)
      for i, num in enumerate(nums): 
         ans[i] = ans[i + n] = num
      return ans
        # Leave only the preferred solution uncommented and executable.






 