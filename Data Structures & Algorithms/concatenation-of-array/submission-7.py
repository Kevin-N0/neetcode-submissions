from typing import List


class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        """
        @NC250_START
        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S2

        @PROBLEM_DETAILS_START

        PROBLEM: Concatenation of Array
        URL: https://neetcode.io/problems/concatenation-of-array/solution
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        You are given an integer array nums of length n. Create an array ans
        of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for
        0 <= i < n (0-indexed).

        Specifically, ans is the concatenation of two nums arrays.

        Return the array ans.

        Example 1:

        Input: nums = [1,4,1,2]
        Output: [1,4,1,2,1,4,1,2]

        Example 2:

        Input: nums = [22,21,20,1]
        Output: [22,21,20,1,22,21,20,1]

        Constraints:

        1 <= nums.length <= 1000
        1 <= nums[i] <= 1000

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [STEP_1_UNDERSTAND_THE_PROBLEM]

        1. We are given an integer list nums containing n elements.

        2. We must return a new list containing nums twice in the same order.

        3. The required relationship is:
           - ans[i] = nums[i]
           - ans[i + n] = nums[i]
           for every index i from 0 through n - 1.

        4. Therefore, the first n positions of ans contain the original nums,
           and the next n positions contain another copy of nums.

        5. The returned list must contain exactly 2n elements.

        6. The main task is construction rather than searching or optimizing a
           numeric value: we must build the required output while preserving
           the original ordering.

        7. The task is simple, but indexing matters because the second copy
           begins exactly n positions after the first copy.


        [STEP_2_RESTATE_THE_PROBLEM]

        Possible spoken response:

        "I'm given an integer array nums, and I need to return a new array that
        contains all of nums followed immediately by the same elements again.
        So if nums has length n, the result should have length 2n, with each
        nums[i] appearing at positions i and i + n."


        [STEP_3_CLARIFY_AND_CONFIRM]

        1. Question:
           "Should I return a new array rather than modify nums?"

           Why it matters:
           It determines whether the implementation may reuse the input's
           storage or should construct separate output storage.

           What the statement already establishes:
           It asks us to create ans and return that array.

           Safe assumption or implementation choice:
           Construct and return a new list without modifying nums.

        2. Question:
           "Does the order need to remain exactly the same in both copies?"

           Why it matters:
           Reordering would produce an incorrect concatenation.

           What the statement already establishes:
           ans[i] == nums[i] and ans[i + n] == nums[i].

           Safe assumption or implementation choice:
           Preserve the exact original order.

        3. Question:
           "Are duplicate values handled normally?"

           Why it matters:
           We should know whether repeated values require special handling.

           What the statement already establishes:
           The result is defined by position, not by uniqueness.

           Safe assumption or implementation choice:
           Copy every element as it appears, including duplicates.

        4. The problem statement is otherwise precise, so no additional
           assumptions are needed.


        [STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]

        1. Input:
           nums: List[int]

        2. Parameter meaning:
           nums is the original integer array that must appear twice in the
           result.

        3. Output:
           List[int]

        4. Output size:
           If n = len(nums), the returned list contains exactly 2n elements.

        5. Supported constraints:
           - 1 <= nums.length <= 1000
           - 1 <= nums[i] <= 1000

        6. Duplicate behavior:
           Duplicate values are preserved exactly as they appear.

        7. Ordering:
           Both copies preserve the original ordering of nums.

        8. Mutation policy:
           The implementation does not modify nums.

        9. No-result behavior:
           Not applicable. Every valid input has a required output.

        10. Important edge cases:
            - A one-element array.
            - Arrays containing repeated values.
            - Arrays at the maximum supported length.

        11. Relevant complexity variable:
            n = len(nums).


        [STEP_5_BASELINE_APPROACH]

        Approach:
        Iteration (Two Pass)

        Core idea:
        Build an empty result list and traverse nums twice. During each pass,
        append every element to the result.

        Data structures:
        - ans: the result list.
        - Loop variables for the two passes and current value.

        Execution:

        1. Initialize ans as an empty list.

        2. Run an outer loop exactly twice.

        3. During each outer-loop iteration, scan nums from beginning to end.

        4. Append every num to ans.

        5. After two complete passes, return ans.

        Why it works:
        The first pass appends one complete copy of nums. The second pass
        appends another complete copy in the same order. Therefore, ans is
        nums followed by nums.

        Why it is a natural starting point:
        It directly translates the phrase "concatenate the array with itself"
        into two sequential traversals.

        Main limitation:
        The input is traversed twice even though the problem gives a direct
        relationship between each original index i and both output positions
        i and i + n.


        [STEP_6_BASELINE_COMPLEXITY]

        Let n = len(nums).

        Time derivation:

        1. The outer loop runs exactly 2 times.

        2. Each outer-loop iteration visits all n elements.

        3. Therefore, there are 2n list append operations.

        4. A normal list append is amortized O(1).

        5. Total work is therefore O(2n).

        6. Constant factors are removed in Big-O notation.

        Final time:
        O(n) amortized time.

        Space derivation:

        1. ans grows to contain 2n elements.

        2. That list is the required output.

        3. Apart from the output, only fixed-size loop variables are used.

        4. There is no recursion or additional growing data structure.

        5. nums is not modified.

        Final auxiliary space:
        O(1), excluding the required O(n) output.


        [STEP_7_FIND_THE_BOTTLENECK]

        1. Repeated work:
           The baseline performs two complete traversals of nums.

        2. Why this is repeated:
           During the first pass it writes the first copy, and during the
           second pass it writes the second copy.

        3. How often it occurs:
           Every input element is visited twice.

        4. Information we already have:
           For an element at index i, the problem directly tells us both
           destination positions:
           - i
           - i + n

        5. What could improve:
           Instead of using separate passes for the two copies, we can process
           nums[i] once and fill both required positions immediately.

        6. Important complexity observation:
           The baseline is already O(n), so this optimization does not improve
           the asymptotic time complexity. It removes an unnecessary second
           traversal and maps more directly to the problem's index definition.


        [STEP_8_OPTIMIZATION_BRIDGE]

        1. The repeated work to avoid is the second full scan of nums.

        2. For each index i, we already know that nums[i] belongs in two places:
           ans[i] and ans[i + n].

        3. We can therefore allocate the entire 2n-sized output first.

        4. During one traversal, we use the current index i to update both
           positions.

        5. This replaces two separate traversals with one traversal containing
           two constant-time assignments per element.

        6. The tradeoff is that we must preallocate ans and carefully calculate
           the i + n offset.

        7. This tradeoff is acceptable because the output must contain 2n
           elements anyway, and the direct index mapping is easy to verify.


        [STEP_9_PREFERRED_APPROACH]

        Approach:
        Iteration (One Pass)

        Central idea:
        Allocate the final result list first. While visiting each element of
        nums once, place that element into both positions required by the
        problem.

        Pattern:
        Direct index mapping.

        Direct index mapping means that we use a known relationship between an
        input index and its destination indices instead of discovering those
        positions through additional searching or traversals.

        Important variables:

        - n:
          The length of nums.

        - ans:
          The result list with 2n positions.

        - i:
          The current index in nums.

        - num:
          The value nums[i].

        Algorithm:

        1. Set n = len(nums).

        2. Allocate ans with 2n positions:
           ans = [0] * (2 * n)

        3. Iterate through nums using enumerate(nums), which provides both i
           and num.

        4. For each element, assign:
           ans[i] = num

        5. In the same iteration, assign:
           ans[i + n] = num

        6. Continue until every element of nums has been processed.

        7. Return ans.

        Mutation behavior:
        nums is not modified.

        Main advantage:
        Each input element is visited once, and both required output positions
        are filled immediately.

        Main tradeoff:
        The implementation requires correct use of the i + n offset and
        preallocation of the result list.


        [STEP_10_CORRECTNESS_REASONING]

        Proof style:
        Exhaustive coverage with a maintained condition.

        A maintained condition is a fact that remains true after each processed
        input element.

        Claim:
        After processing index i, the algorithm has correctly assigned nums[i]
        to both required positions ans[i] and ans[i + n].

        Why the claim is true:

        1. During the iteration for index i, num equals nums[i].

        2. The statement:
           ans[i] = ans[i + n] = num
           writes that same value to both required positions.

        3. Therefore:
           ans[i] == nums[i]
           and
           ans[i + n] == nums[i].

        Why previously processed values remain correct:

        4. Every index i has a unique first-half position i and unique
           second-half position i + n.

        5. Later iterations use different destination indices, so they do not
           overwrite the positions already assigned for earlier indices.

        Why no required position is missed:

        6. enumerate(nums) processes every valid input index from 0 through
           n - 1 exactly once.

        7. Therefore, every position from 0 through n - 1 is filled in the
           first half, and every position from n through 2n - 1 is filled in
           the second half.

        Why termination gives the required result:

        8. Once all n input indices are processed, every position in ans
           satisfies the required relationship.

        9. Therefore, ans is exactly nums followed by nums.


        [STEP_11_EXAMPLE_TRACE]

        Official example:

        Input:
        nums = [1, 4, 1, 2]

        Expected output:
        [1, 4, 1, 2, 1, 4, 1, 2]

        Initial state:

        n = 4

        ans = [0, 0, 0, 0, 0, 0, 0, 0]

        Iteration 1:

        i = 0
        num = 1

        Write:
        ans[0] = 1
        ans[0 + 4] = ans[4] = 1

        ans:
        [1, 0, 0, 0, 1, 0, 0, 0]

        Iteration 2:

        i = 1
        num = 4

        Write:
        ans[1] = 4
        ans[1 + 4] = ans[5] = 4

        ans:
        [1, 4, 0, 0, 1, 4, 0, 0]

        Iteration 3:

        i = 2
        num = 1

        Write:
        ans[2] = 1
        ans[2 + 4] = ans[6] = 1

        ans:
        [1, 4, 1, 0, 1, 4, 1, 0]

        Iteration 4:

        i = 3
        num = 2

        Write:
        ans[3] = 2
        ans[3 + 4] = ans[7] = 2

        ans:
        [1, 4, 1, 2, 1, 4, 1, 2]

        Return:
        [1, 4, 1, 2, 1, 4, 1, 2]

        This matches the expected output.


        [STEP_12_CODE_PLAN]

        1. Import List for the supplied type annotation.

        2. Preserve the required Solution class and getConcatenation method.

        3. Compute:
           n = len(nums)

        4. Allocate:
           ans = [0] * (2 * n)

        5. Traverse nums with:
           for i, num in enumerate(nums)

           This gives both the current index and value.

        6. During each iteration, write the current value to both required
           positions:
           ans[i] = ans[i + n] = num

        7. Do not modify nums.

        8. After the loop completes, return ans.

        9. No helper functions, recursion, early returns, or special boundary
           handling are required.


        [STEP_13_IMPLEMENTATION]

        1. The first line of the method computes n so the second-half offset is
           available throughout the loop.

        2. The result list is preallocated to exactly 2n positions.

        3. enumerate(nums) keeps the code aligned with the problem's index-based
           definition because we need both i and nums[i].

        4. The chained assignment:

           ans[i] = ans[i + n] = num

           assigns the same current value to both required result positions.

        5. Each output position is assigned exactly once.

        6. There are no early returns because every input element must be
           processed.

        7. nums is only read, so the input is not mutated.


        [STEP_14_TEST_CASES]

        Test 1:
        Purpose:
        Representative official example.

        Input:
        nums = [1, 4, 1, 2]

        Expected output:
        [1, 4, 1, 2, 1, 4, 1, 2]

        What it validates:
        General ordering, repeated values, and correct placement in both
        halves.

        Test 2:
        Purpose:
        Second official example.

        Input:
        nums = [22, 21, 20, 1]

        Expected output:
        [22, 21, 20, 1, 22, 21, 20, 1]

        What it validates:
        Correct copying of several distinct values.

        Test 3:
        Purpose:
        Smallest allowed input length.

        Input:
        nums = [7]

        Expected output:
        [7, 7]

        What it validates:
        The i + n offset works correctly when n = 1.

        Test 4:
        Purpose:
        Repeated values.

        Input:
        nums = [5, 5, 5]

        Expected output:
        [5, 5, 5, 5, 5, 5]

        What it validates:
        Duplicate values are copied by position without special handling.

        Test 5:
        Purpose:
        Verify exact ordering.

        Input:
        nums = [3, 1, 2]

        Expected output:
        [3, 1, 2, 3, 1, 2]

        What it validates:
        The second half starts at index n and preserves the original sequence.


        [STEP_15_TIME_COMPLEXITY_DERIVATION]

        Let:
        n = len(nums)

        Phase 1: Determine the input length.

        - len(nums) is O(1) for a Python list.

        Phase 2: Allocate the result.

        - [0] * (2 * n) constructs a list containing 2n elements.
        - Constructing that list requires O(2n) = O(n) time.

        Phase 3: Fill the result.

        - enumerate(nums) processes n elements.
        - Each iteration performs two indexed list assignments.
        - Each indexed assignment is O(1).
        - Therefore, the loop performs n * O(1) work = O(n).

        Combine the sequential phases:

        O(1) + O(n) + O(n) = O(n)

        The constant factor from creating and writing 2n positions does not
        change the Big-O result.

        Final time complexity:
        O(n) worst-case time.

        Interview-ready statement:

        "The time complexity is O(n) because allocating the 2n-element output
        is linear and then I make one linear pass through nums, doing constant
        work per element."


        [STEP_16_SPACE_COMPLEXITY_DERIVATION]

        Let:
        n = len(nums)

        Fixed-size variables:

        - n
        - i
        - num

        These require O(1) auxiliary space.

        Growing structures:

        - ans contains exactly 2n elements.
        - Therefore, the required output occupies O(n) space.

        Recursion:

        - None.
        - Recursion-stack space is not applicable.

        Temporary growing storage:

        - None.

        Input mutation:

        - nums is not modified.

        Output-space treatment:

        - ans is required by the problem, so when reporting auxiliary space we
          exclude it.

        Final auxiliary-space complexity:
        O(1)

        Required output space:
        O(n)

        Interview-ready statement:

        "The algorithm uses O(1) auxiliary space because, excluding the required
        2n-element output array, it only keeps a few fixed-size variables. The
        output itself uses O(n) space."


        [STEP_17_APPROACH_TRADEOFFS]

        Baseline: Iteration (Two Pass)

        Main idea:
        Traverse nums twice and append each element to ans.

        Time:
        O(n) amortized.

        Auxiliary space:
        O(1), excluding the O(n) output.

        Advantage:
        Very simple and directly represents nums followed by nums.

        Disadvantage:
        Visits every input element twice.

        Preferred: Iteration (One Pass)

        Main idea:
        Preallocate ans and write nums[i] into positions i and i + n during the
        same iteration.

        Time:
        O(n) worst-case.

        Auxiliary space:
        O(1), excluding the O(n) output.

        Advantage:
        Uses one traversal and directly follows the index relationship provided
        by the problem.

        Disadvantage:
        Requires preallocation and careful use of the i + n offset.

        Why choose the preferred approach:

        1. It removes the baseline's second traversal.

        2. It makes explicit use of the relationship stated in the problem.

        3. It keeps the same optimal asymptotic O(n) time because constructing
           a 2n-element result inherently requires linear work.

        Memory tradeoff:
        Both approaches require an O(n) output and only O(1) auxiliary space.

        Mutation tradeoff:
        Neither approach needs to modify nums.

        Interview readability:
        The one-pass version clearly demonstrates that each nums[i] maps to
        exactly two known result positions.

        When the baseline is still acceptable:
        The two-pass approach remains correct, linear, and easy to explain. If
        simplicity is the main goal, it is a perfectly reasonable solution.


        [STEP_18_INTERVIEW_COMMUNICATION]

        BEFORE CODING:

        1. Restate the requirement:
           "I need to return nums followed by another copy of nums."

        2. Confirm the important behavior:
           "I'll return a new array and preserve the exact input order."

        3. Introduce the baseline:
           "A simple approach is to traverse the array twice and append every
           element during each pass."

        4. State its complexity:
           "That is still O(n), with O(1) auxiliary space excluding the
           required result."

        5. Identify the repeated work:
           "We scan nums twice even though each input index already tells us
           both output positions."

        6. Introduce the preferred approach:
           "I can allocate the 2n result up front and, in one pass, write each
           nums[i] to i and i + n."

        WHILE CODING:

        1. Explain n:
           "I'll store the input length because it is the offset for the second
           copy."

        2. Explain ans:
           "I'll allocate exactly 2n positions."

        3. Explain the key update:
           "For each index i, I put the same value at i and i + n."

        4. Verify the boundary:
           "When i = n - 1, i + n = 2n - 1, which is the final valid index."

        5. Keep communication focused on meaningful decisions rather than
           narrating every line of Python syntax.

        AFTER CODING:

        1. Trace a small example.

        2. Explain why every input index fills exactly two required positions.

        3. Derive the O(n) time from output allocation plus one linear loop.

        4. State O(1) auxiliary space and O(n) required output space.

        5. Mention the central tradeoff:
           The one-pass version avoids a second traversal but requires direct
           index placement.


        [INTERVIEW_SCRIPT]

        "We're given an integer array nums, and we need to return a new array
        containing nums followed by the same elements again in the same order.
        If nums has length n, each nums[i] should appear at both ans[i] and
        ans[i + n].

        A straightforward solution would be to create an empty result list,
        loop through nums twice, and append every value. That is already O(n)
        time because two linear passes are still linear, and it uses O(1)
        auxiliary space excluding the output.

        The repeated part is that we're scanning nums twice. Since the problem
        directly gives the mapping from input index i to output indices i and
        i + n, I can instead allocate the full 2n-sized result first and fill
        both locations during one pass.

        I'll compute n, create ans with 2n positions, then enumerate nums. For
        each i and num, I'll assign num to ans[i] and ans[i + n]. After the
        loop, every position in both halves has been filled, so I return ans.

        For example, with [1, 2, 3], n is 3. At i = 0 I write 1 to positions
        0 and 3, at i = 1 I write 2 to positions 1 and 4, and at i = 2 I write
        3 to positions 2 and 5. That gives [1, 2, 3, 1, 2, 3].

        Allocating the output is O(n), and the loop is another O(n), so the
        total time is O(n). Excluding the required output, I only use a few
        variables, so auxiliary space is O(1). The main tradeoff is that the
        direct one-pass version needs careful indexing, while the two-pass
        append version is slightly more straightforward."


        [PATTERN_RECOGNITION]

        Main pattern:
        Direct index mapping into a preallocated output array.

        Statement signals:

        1. The problem explicitly defines output positions using formulas such
           as:
           ans[i]
           ans[i + n]

        2. The final output size is known before processing begins.

        3. Every input element has predetermined destination positions.

        Why these signals suggest the technique:

        - If destination indices can be calculated directly, there is no need
          to search for where an element belongs.
        - If the output size is known, preallocating the result allows direct
          indexed assignment.

        Common data structure:
        A list with its final required size allocated in advance.

        Common variations:

        1. Copying values into multiple fixed regions of an output array.

        2. Rearranging values when the destination index can be calculated
           directly.

        3. Building repeated blocks where each input index maps to a predictable
           output offset.

        Questions to ask when recognizing this pattern:

        1. "Is the final output size known?"

        2. "Can I compute each destination position directly from i?"

        3. "Does every input element map to one or more fixed output indices?"

        4. "Can I fill multiple required positions during the same traversal?"

        False-positive signals:

        - Merely having an array does not imply that direct index mapping is the
          correct technique.
        - If the destination depends on values discovered later, a simple
          formula such as i + n may not exist.
        - If elements must be searched, sorted, grouped, or matched based on
          their values, direct placement alone may not solve the problem.

        Neighboring patterns:

        - Two-pass array construction:
          Similar because it also builds a new array, but it may perform
          separate phases rather than filling multiple known destinations at
          once.

        - In-place rearrangement:
          Also uses indices, but it modifies existing storage. This problem
          requires a larger 2n-sized result, so a separate output array is the
          natural structure.


        [COMMON_PITFALLS]

        UNDERSTANDING AND COMMUNICATION:

        1. Restating the task as merely "duplicate every number."
           That wording can be ambiguous because the required result is two
           complete copies of nums in sequence.

        2. Forgetting the ordering requirement.
           Both halves must preserve the original order.

        3. Skipping the baseline entirely.
           The two-pass approach is useful because it establishes a simple
           correct solution before discussing the one-pass refinement.

        4. Claiming that the one-pass version improves O(n) to something
           asymptotically faster.
           Both approaches are O(n). The preferred version removes a traversal,
           not the linear lower bound imposed by constructing the output.

        5. Giving O(n) without deriving it.
           The result allocation itself is linear, and the loop is also linear.

        IMPLEMENTATION:

        6. Allocating only n positions.
           The result requires 2n positions.

        7. Using the wrong second-half index.
           The correct destination is i + n.

        8. Off-by-one reasoning at the upper boundary.
           For i = n - 1, the second position is:
           (n - 1) + n = 2n - 1,
           which is the final valid index.

        9. Accidentally changing the input.
           This implementation only reads nums and writes to ans.

        10. Treating duplicate values specially.
            Duplicates require no special handling because placement is based
            on index.

        COMPLEXITY:

        11. Multiplying sequential phases.
            Output allocation and the loop happen sequentially, so their costs
            add:
            O(n) + O(n) = O(n).

        12. Saying the one-pass implementation performs only n output writes.
            It performs two assignments for each of n input elements, giving
            2n writes, which still simplifies to O(n).

        13. Calling total space O(1) without explaining output treatment.
            Auxiliary space is O(1), but the required output contains 2n
            elements and therefore uses O(n) space.


        [FINAL_REVIEW_CHECKLIST]

        1. Can I explain that the result is nums followed by nums?

        2. Do I know that the returned array has exactly 2n elements?

        3. Can I state the relationship ans[i] = nums[i] and
           ans[i + n] = nums[i]?

        4. Can I explain the simple two-pass baseline?

        5. Can I derive why the baseline is still O(n)?

        6. Can I identify the repeated second traversal?

        7. Can I explain how the direct i and i + n mapping removes that
           traversal?

        8. Can I describe what n, ans, i, and num mean?

        9. Can I explain why every required result position is filled exactly
           once?

        10. Can I trace a small example by hand?

        11. Can I handle the one-element and repeated-value cases?

        12. Can I derive the preferred O(n) time instead of merely memorizing
            it?

        13. Can I explain O(1) auxiliary space versus O(n) required output
            space?

        14. Can I state the tradeoff between two-pass appending and one-pass
            direct placement?

        15. Can I explain and write the preferred implementation naturally
            without copying it?

        @CONTENT_END

        @NC250_END
        """

        n = len(nums)
        ans = [0] * (2 * n)

        for i, num in enumerate(nums):
            ans[i] = ans[i + n] = num

        return ans