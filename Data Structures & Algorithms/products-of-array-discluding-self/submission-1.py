# =====================================================================
# PROBLEM 5: Products of Array Except Self
# =====================================================================

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing / Prefix & Suffix Products
        PREFERRED_SOLUTION: S4

        @PROBLEM_DETAILS_START

        PROBLEM: Products of Array Except Self

        URL: https://neetcode.io/problems/products-of-array-discluding-self/question?list=blind75

        DIFFICULTY: Medium

        PROBLEM DETAILS:

        Given an integer array nums, return an array output where output[i] is
        the product of all the elements of nums except nums[i].

        Each product is guaranteed to fit in a 32-bit integer.

        Follow-up:
        Could you solve it in O(n) time without using the division operation?

        Example 1:

        Input:
        nums = [1,2,4,6]

        Output:
        [48,24,12,8]

        Example 2:

        Input:
        nums = [-1,0,1,2,3]

        Output:
        [0,-6,0,0,0]

        Constraints:

        - 2 <= nums.length <= 100,000
        - -30 <= nums[i] <= 30
        - The product of any prefix or suffix of nums is guaranteed to fit in
          a 32-bit integer.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Brute Force

        INT:

        For every output index, multiply every input element except the one at
        that index. This is direct but repeats almost the same multiplication
        work for every position.

        ALGO:

        1. Create a result array.
        2. For each i, initialize prod = 1.
        3. Scan every j.
        4. Multiply nums[j] when j != i.
        5. Store prod at res[i].

        TIME: O(n^2)

        Every index causes another full scan.

        SPACE: O(1) extra, O(n) output

        Only the result array grows with n.


        [S2]-Division

        INT:

        Multiply all non-zero values and count zeros. With no zeros, divide the
        total product by nums[i]. With one zero, only the zero position gets
        the non-zero product. With two or more zeros, every answer is zero.

        ALGO:

        1. Compute the product of non-zero numbers and count zeros.
        2. If there are more than one zero, return all zeros.
        3. If there is one zero, place the non-zero product only at the zero
           index.
        4. Otherwise use total_product // nums[i].

        TIME: O(n)

        The input is scanned a constant number of times.

        SPACE: O(1) extra, O(n) output

        Only constant state is used beyond the returned array.


        [S3]-Prefix & Suffix Arrays

        INT:

        Build pref[i] as the product strictly to the left of i and suff[i] as
        the product strictly to the right. Their product is the answer for i.

        ALGO:

        1. Create pref, suff, and res arrays.
        2. Set pref[0] = 1 and suff[n - 1] = 1.
        3. Fill pref from left to right.
        4. Fill suff from right to left.
        5. Set res[i] = pref[i] * suff[i].

        TIME: O(n)

        Three linear passes are used.

        SPACE: O(n)

        Separate prefix and suffix arrays are allocated.


        [S4]-Prefix & Suffix (Optimal)

        INT:

        Reuse the result array instead of storing separate prefix and suffix
        arrays. First write the product of everything to the left into each
        res[i]. Then sweep right-to-left with a running postfix product and
        multiply it into res[i].

        ALGO:

        1. Initialize res to all ones.
        2. Sweep left-to-right with prefix = 1.
        3. Store prefix in res[i], then multiply prefix by nums[i].
        4. Sweep right-to-left with postfix = 1.
        5. Multiply res[i] by postfix, then multiply postfix by nums[i].
        6. Return res.

        TIME: O(n)

        Two linear passes are performed.

        SPACE: O(1) extra, O(n) output

        Only prefix and postfix scalars are used beyond the returned array.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Recompute every product independently.
        - Time: O(n^2)
        - Space: O(1) extra
        - Input modified: No
        - Main advantage: Direct translation of the definition.
        - Main disadvantage: Quadratic runtime.

        S2:

        - Approach: Total non-zero product plus zero counting.
        - Time: O(n)
        - Space: O(1) extra
        - Input modified: No
        - Main advantage: Linear time with constant extra space.
        - Main disadvantage: Uses division, contrary to the follow-up.

        S3:

        - Approach: Explicit prefix and suffix arrays.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Avoids division and handles zeros naturally.
        - Main disadvantage: Uses two auxiliary arrays.

        S4:

        - Approach: Running prefix and postfix products in the output array.
        - Time: O(n)
        - Space: O(1) extra
        - Input modified: No
        - Main advantage: Meets the O(n), no-division follow-up with constant
          auxiliary space.
        - Main disadvantage: Requires careful pass ordering.

        [COMMON_PITFALLS]

        - Division requires special handling for zero values.
        - Prefix and suffix values must exclude nums[i] itself.
        - In fixed-width integer languages, product overflow must be considered;
          the source constraints guarantee the relevant products fit.

        [SOURCE_NOTES]

        - Active submitted implementation uses S4.
        - Output-array space is not counted as auxiliary space for the optimal
          method.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        res = [1] * (len(nums))

        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *= nums[i]
        postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        return res

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Brute Force
        #
        # n = len(nums)
        # res = [0] * n
        #
        # for i in range(n):
        #     prod = 1
        #     for j in range(n):
        #         if i == j:
        #             continue
        #         prod *= nums[j]
        #
        #     res[i] = prod
        # return res
        #
        #
        # S2 CODE - Division
        #
        # prod, zero_cnt = 1, 0
        # for num in nums:
        #     if num:
        #         prod *= num
        #     else:
        #         zero_cnt +=  1
        # if zero_cnt > 1: return [0] * len(nums)
        #
        # res = [0] * len(nums)
        # for i, c in enumerate(nums):
        #     if zero_cnt: res[i] = 0 if c else prod
        #     else: res[i] = prod // c
        # return res
        #
        #
        # S3 CODE - Prefix & Suffix Arrays
        #
        # n = len(nums)
        # res = [0] * n
        # pref = [0] * n
        # suff = [0] * n
        #
        # pref[0] = suff[n - 1] = 1
        # for i in range(1, n):
        #     pref[i] = nums[i - 1] * pref[i - 1]
        # for i in range(n - 2, -1, -1):
        #     suff[i] = nums[i + 1] * suff[i + 1]
        # for i in range(n):
        #     res[i] = pref[i] * suff[i]
        # return res
