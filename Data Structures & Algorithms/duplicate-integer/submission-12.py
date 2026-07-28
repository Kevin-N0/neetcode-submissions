from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        """
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S3

        @PROBLEM_DETAILS_START

        PROBLEM: Contains Duplicate
        URL: https://neetcode.io/problems/duplicate-integer/question?list=neetcode250
        DIFFICULTY: Easy

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
        1. Check every pair of elements and return True if any pair has equal values.
        2. Comparing every pair guarantees that any duplicate will eventually be found.
        3. This is the most direct approach, but it is the least efficient because it examines every possible pair in the worst case.

        ALGO:
        1. Iterate through the array with an outer loop over each index i.
        2. For each i, use an inner loop starting at i + 1 so that every pair of distinct indices is checked once.
        3. If nums[i] equals nums[j], return True immediately.
        4. If all pairs are checked without finding equal values, return False.

        TIME: O(n^2)

        1. Let n be the number of elements in nums.
        2. No additional input-size variable is needed.
        3. The main operation is comparing nums[i] with nums[j].
        4. In the worst case, the nested loops perform n(n - 1) / 2 comparisons.
        5. Each comparison costs O(1).
        6. The dependent nested-loop costs are multiplied, producing O(n^2) total work.
        7. After simplifying, the dominant term is O(n^2).
        8. Therefore, the worst-case time complexity is O(n^2).

        SPACE: O(1)

        1. The algorithm uses only the loop indices i and j.
        2. No data structure grows with the input.
        3. Additional copied input, sorting storage, memoization, or visited state is not applicable.
        4. The recursion stack is not applicable.
        5. The remaining fixed variables use O(1) space.
        6. Required output space is O(1).
        7. The input is not modified.
        8. Therefore, the auxiliary-space complexity is O(1).


        [S2]-[SORTING]

        INT:
        1. Sort the array so that equal values appear next to each other.
        2. If a duplicate exists, at least one pair of adjacent elements in the sorted array must be equal.
        3. The adjacent scan is simple and uses no separate collection, but sorting modifies the input and may require additional internal workspace.

        ALGO:
        1. Sort nums in non-decreasing order in place.
        2. Iterate through the array starting from index 1.
        3. Compare the current element with the previous element.
        4. If nums[i] equals nums[i - 1], return True.
        5. If the loop finishes without finding equal neighbors, return False.

        TIME: O(n log n)

        1. Let n be the number of elements in nums.
        2. No additional input-size variable is needed.
        3. The main operations are sorting the array and scanning adjacent elements.
        4. Python sorting processes n elements in O(n log n) worst-case time, and the scan performs at most n - 1 comparisons.
        5. Each adjacent comparison costs O(1).
        6. The phases are sequential, so their costs are added: O(n log n) + O(n).
        7. After simplifying, the dominant term is O(n log n).
        8. Therefore, the worst-case time complexity is O(n log n).

        SPACE: O(n)

        1. The algorithm uses Python's in-place list sort and a loop index.
        2. Python's sorting implementation can use temporary storage proportional to n in the worst case.
        3. Sorting workspace uses O(n) worst-case auxiliary space; no copied input or other growing structure is created explicitly.
        4. The recursion stack is not applicable to the submitted code.
        5. The remaining fixed variables use O(1) space.
        6. Required output space is O(1).
        7. The input is modified.
        8. Therefore, the worst-case auxiliary-space complexity is O(n).


        [S3]-[HASH SET]

        INT:
        1. Use a hash set to keep track of values already encountered.
        2. While scanning the array, a value already in the set must have appeared earlier, so finding it again proves that a duplicate exists.
        3. This provides expected linear time without modifying the input, but the set may store up to every distinct value.

        ALGO:
        1. Initialize an empty hash set named seen.
        2. Iterate through each number in nums.
        3. If the current number is already in seen, return True because a duplicate has been found.
        4. Otherwise, add the current number to seen.
        5. If the loop finishes without finding a duplicate, return False.

        TIME: O(n)

        1. Let n be the number of elements in nums.
        2. No additional input-size variable is needed.
        3. The main operations are hash-set membership checks and insertions.
        4. Each element is processed at most once, producing at most n membership checks and n insertions.
        5. Each set membership check and insertion costs expected O(1).
        6. The sequential operations across n elements combine to expected O(n) total work.
        7. After simplifying, the dominant term is O(n).
        8. Therefore, the expected time complexity is O(n); pathological hash collisions can produce O(n^2) worst-case time.

        SPACE: O(n)

        1. The algorithm uses a hash set named seen and a loop variable.
        2. The set can contain up to n distinct values when no duplicate is found.
        3. The visited-state set uses O(n) auxiliary space; copied input, sorting storage, and memoization are not applicable.
        4. The recursion stack is not applicable.
        5. The remaining fixed variables use O(1) space.
        6. Required output space is O(1).
        7. The input is not modified.
        8. Therefore, the auxiliary-space complexity is O(n).


        [APPROACH_COMPARISON]

        S1:
        - Approach: Brute Force
        - Time: O(n^2)
        - Time qualification: Worst-case
        - Space: O(1)
        - Input modified: No
        - Main advantage: Uses constant auxiliary space and directly checks every possible pair.
        - Main disadvantage: Performs quadratic work when no duplicate is found or the duplicate appears late.

        S2:
        - Approach: Sorting
        - Time: O(n log n)
        - Time qualification: Worst-case
        - Space: O(n)
        - Input modified: Yes
        - Main advantage: After sorting, duplicates can be detected with one simple adjacent scan.
        - Main disadvantage: Modifies the input and is slower than hashing in expected time.

        S3:
        - Approach: Hash Set
        - Time: O(n)
        - Time qualification: Expected
        - Space: O(n)
        - Input modified: No
        - Main advantage: Detects duplicates in expected linear time without changing the input.
        - Main disadvantage: Requires additional space proportional to the number of distinct values.


        [COMMON_PITFALLS]

        1. In the sorting approach, comparing nums[i] with nums[i] instead of nums[i - 1] makes the condition always true.
        2. Starting the sorting scan at index 0 and accessing nums[i - 1] can accidentally compare the first element with the last element.
        3. Adding a number to the hash set before checking membership causes every number to appear duplicated immediately.
        4. Claiming guaranteed O(1) set operations instead of expected O(1) ignores pathological hash-collision behavior.
        5. Forgetting that nums.sort() modifies the original input can create an unintended side effect.

        @CONTENT_END
        @NC250_END
        """

        # S1 CODE - [Brute Force]:
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] == nums[j]:
        #             return True
        # return False

        # S2 CODE - [Sorting]:
        # nums.sort()
        # for i in range(1, len(nums)):
        #     if nums[i] == nums[i - 1]:
        #         return True
        # return False

        # S3 CODE - [Hash Set]:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False