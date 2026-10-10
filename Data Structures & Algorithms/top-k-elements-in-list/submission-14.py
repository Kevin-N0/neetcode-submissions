class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        
        # ----------------------------------------------------------------------
        # 1. BRUTE FORCE IMPLEMENTATION
        # ----------------------------------------------------------------------
        count = {}
        for num in nums:
            count[num] = 1 + count.get(num, 0)
        arr = []
        for num, cnt in count.items():
            arr.append([cnt, num])
        arr.sort()
        res = []
        while len(res) < k:
            res.append(arr.pop()[1])
        return res
        # ----------------------------------------------------------------------
        # 2. OPTIMAL IMPLEMENTATION
        # ----------------------------------------------------------------------
        

"""
================================================================================
COMPLEXITY & MATHEMATICAL ACCOUNTING
================================================================================
VARIABLE DEFINITIONS:
  - <VAR_1> (e.g., n) = <DEFINITION_1> (e.g., length of input array)
  - <VAR_2> (e.g., m) = <DEFINITION_2> (e.g., number of strings / distinct keys)
--------------------------------------------------------------------------------

1. BRUTE FORCE (BASELINE)
--------------------------------------------------------------------------------
1a. Time Complexity: O(<FINAL_TIME_BOUND>)
    • Formula / Unsimplified Sum:
      = <OUTER_FACTOR> X (<STEP_A> + <STEP_B> + <STEP_C>)
      = <EXPANDED_POLYNOMIAL_OR_SUM>
      = O(<FINAL_TIME_BOUND>)
    • Dominance & Collapse:
      <EXPLANATION_OF_WHY_DOMINANT_TERM_GROWS_FASTER_AND_LOWER_TERMS_DROP>

1b. Time Summed Breakdown:
    X <OUTER_ITERATIONS>: <DESCRIPTION_OF_OUTER_LOOP>
      + <STEP_A_COST> (<EXPLANATION_OF_INNER_OPERATION_A>)
      + <STEP_B_COST> (<EXPLANATION_OF_INNER_OPERATION_B>)
      + <STEP_C_COST> (<EXPLANATION_OF_LOOKUP_OR_CONTAINER_MUTATION>)

1c. Space Complexity: O(<FINAL_SPACE_BOUND>)
    • Unsimplified Sum:
      = <AUXILIARY_COST> (working mem) + <STACK_COST> (scalars) + <OUTPUT_COST> (results)
      = <RAW_SPACE_EXPRESSION>
      = O(<FINAL_SPACE_BOUND>)
    • Dominance & Collapse:
      <EXPLANATION_OF_WHICH_CONTAINER_SCALES_WITH_INPUT>

1d. Space Summed Breakdown:
    - Auxiliary Space (Working Memory): <CONTAINER_NAME> holds up to <X> items -> O(<...>)
    - Input / Fixed Space (Stack): Scalar tracking registers (<VARS>) -> O(1)
    - Output Space: Returned container holding <Y> elements -> O(<...>)


--------------------------------------------------------------------------------
2. OPTIMAL (INTERVIEW TARGET)
--------------------------------------------------------------------------------
2a. Time Complexity: O(<FINAL_TIME_BOUND>)
    • Formula / Unsimplified Sum:
      = <OUTER_FACTOR> X (<STEP_A> + <STEP_B>) + <NON_NESTED_PASS>
      = <EXPANDED_SUM>
      = O(<FINAL_TIME_BOUND>)
    • Dominance & Collapse:
      <EXPLANATION_OF_HOW_BOTTLENECK_WAS_REMOVED_AND_WHY_IT_COLLAPSES>

2b. Time Summed Breakdown:
    X <OUTER_ITERATIONS>: <DESCRIPTION_OF_EFFICIENT_PASS>
      + <STEP_A_COST> (<EXPLANATION_OF_INSTANT_LOOKUP_OR_TRANSFORMATION>)
      + <STEP_B_COST> (<EXPLANATION_OF_UPDATE_STEP>)
    + <OPTIONAL_CLEANUP_OR_POST_PASS_COST> (<EXPLANATION>)

2c. Space Complexity: O(<FINAL_SPACE_BOUND>)
    • Unsimplified Sum:
      = <AUXILIARY_COST> (working mem) + <STACK_COST> (scalars) + <OUTPUT_COST> (results)
      = <RAW_SPACE_EXPRESSION>
      = O(<FINAL_SPACE_BOUND>)
    • Dominance & Collapse:
      <EXPLANATION_OF_TOTAL_VS_AUXILIARY_BOUNDS>

2d. Space Summed Breakdown:
    - Auxiliary Space (Working Memory): <CONTAINER_NAME> holds up to <X> items -> O(<...>)
    - Input / Fixed Space (Stack): Fixed pointer / state trackers (<VARS>) -> O(1)
    - Output Space: Returned structure containing <Y> elements -> O(<...>)
"""