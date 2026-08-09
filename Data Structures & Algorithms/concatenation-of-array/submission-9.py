class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: [OPTIONAL]
        PREFERRED_SOLUTION: [OPTIONAL]

        @PROBLEM_DETAILS_START

        PROBLEM: [PASTE PROBLEM NAME]

        URL: [PASTE ORIGINAL PROBLEM URL]

        DIFFICULTY: [Easy | Medium | Hard | Unknown]

        PROBLEM DETAILS:

        [PASTE THE PROBLEM STATEMENT, EXAMPLES, CONSTRAINTS, OR OTHER
        USEFUL OFFICIAL PROBLEM INFORMATION HERE.]

        This area may be incomplete or messy.
        Markdown, copied webpage text, and formatting artifacts are allowed.

        @PROBLEM_DETAILS_END

        @CONTENT_START


        [S1]-[APPROACH NAME]

        INT:

        [Write your intuition if you have it.

        This may be:
        - incomplete
        - rough notes
        - copied or adapted from a solution guide
        - partially wrong
        - empty if you do not know yet]


        ALGO:

        [Write the algorithm steps if you have them.

        These may be incomplete or copied from a solution guide.]


        TIME: [O(...) | UNKNOWN]

        [Optional rough complexity notes or copied explanation.]


        SPACE: [O(...) | UNKNOWN]

        [Optional rough complexity notes or copied explanation.]



        [S2]-[APPROACH NAME]

        INT:

        [Optional second approach. Delete nothing if you are unsure.
        Leave this unfinished if necessary.]


        ALGO:

        [Optional.]


        TIME: [O(...) | UNKNOWN]

        SPACE: [O(...) | UNKNOWN]



        [S3]-[APPROACH NAME]

        INT:

        [Optional.]

        ALGO:

        [Optional.]

        TIME: [O(...) | UNKNOWN]

        SPACE: [O(...) | UNKNOWN]



        [S4]-[APPROACH NAME]

        INT:

        [Optional.]

        ALGO:

        [Optional.]

        TIME: [O(...) | UNKNOWN]

        SPACE: [O(...) | UNKNOWN]



        [APPROACH_COMPARISON]

        [Optional rough notes.

        You do NOT need to complete this table manually.

        Prompt 1 will rebuild the final comparison from the surviving
        approaches.]


        [COMMON_PITFALLS]

        [Optional rough notes, mistakes you made, or useful points copied
        from a solution guide.]


        [SOURCE_NOTES]

        [Optional.

        Paste any extra material here that may help Prompt 1, such as:

        - explanation from the NeetCode solution guide
        - alternate solution notes
        - complexity explanation
        - observations
        - mistakes you made
        - edge cases
        - copied snippets
        - unfinished thoughts

        This section is source material only.]


        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------
        #
        # Leave the implementation you actually want to submit active.
        #
        # It may be incomplete while you are working, but the final
        # NeetCode submission should normally contain runnable code.
        #
        # You may keep alternate attempts below as comments.
        # -----------------------------------------------------------------

        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = num
            ans[i + n] = num

        return ans

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # # S1 CODE - Iteration (Two Pass)
        # # ans = []
        # # for _ in range(2):
        # #     for num in nums:
        # #         ans.append(num)
        # # return ans