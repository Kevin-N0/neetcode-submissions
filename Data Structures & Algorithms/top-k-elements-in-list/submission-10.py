# =====================================================================
# PROBLEM 3: Top K Frequent Elements
# =====================================================================

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing / Bucket Sort / Heap
        PREFERRED_SOLUTION: S3

        @PROBLEM_DETAILS_START

        PROBLEM: Top K Frequent Elements

        URL: https://neetcode.io/problems/top-k-elements-in-list/question?list=blind75

        DIFFICULTY: Medium

        PROBLEM DETAILS:

        Given an integer array nums and an integer k, return the k most
        frequent elements within the array.

        The test cases are generated such that the answer is always unique.

        You may return the output in any order.

        Example 1:

        Input:
        nums = [1,2,2,3,3,3], k = 2

        Output:
        [2,3]

        Example 2:

        Input:
        nums = [7,7], k = 1

        Output:
        [7]

        Constraints:

        - 1 <= nums.length <= 10^4
        - -1000 <= nums[i] <= 1000
        - 1 <= k <= number of distinct elements in nums.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-Sorting

        INT:

        Count each number, convert the frequency map into [frequency, number]
        pairs, sort those pairs, and repeatedly take the largest frequencies.

        ALGO:

        1. Build a frequency map.
        2. Build [count, number] pairs.
        3. Sort the pairs.
        4. Pop from the end until k values have been collected.

        TIME: O(n log n)

        Sorting the frequency pairs dominates.

        SPACE: O(n)

        The frequency map and pair list may both grow linearly.


        [S2]-Min-Heap

        INT:

        Maintain a min-heap of at most k (frequency, number) pairs. Whenever
        the heap grows past k, remove the smallest frequency. The remaining
        heap contains the k most frequent elements.

        ALGO:

        1. Count all frequencies.
        2. Push each (frequency, number) pair into a min-heap.
        3. If heap size exceeds k, pop once.
        4. Pop k elements from the heap and collect their numbers.

        TIME: O(n log k)

        Each distinct value may cause a heap push/pop bounded by heap size k.

        SPACE: O(n + k)

        The count map is O(n) and the heap holds at most k entries.


        [S3]-Bucket Sort

        INT:

        No number can appear more than n times, so use frequency as a direct
        bucket index. Place each number into the bucket matching its count,
        then scan buckets from highest frequency to lowest until k values have
        been collected.

        ALGO:

        1. Count each number's occurrences.
        2. Create len(nums) + 1 empty frequency buckets.
        3. Put every distinct number into freq[count].
        4. Scan the buckets from high frequency to low.
        5. Append values until the result contains k entries.

        TIME: O(n)

        Counting, bucket construction, and reverse bucket scanning are linear.

        SPACE: O(n)

        The frequency map and bucket array use linear space.

        [APPROACH_COMPARISON]

        S1:

        - Approach: Frequency count plus sorting.
        - Time: O(n log n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Straightforward.
        - Main disadvantage: Sorts when full ordering is unnecessary.

        S2:

        - Approach: Frequency count plus size-k min-heap.
        - Time: O(n log k)
        - Space: O(n + k)
        - Input modified: No
        - Main advantage: Keeps only k candidates in the heap.
        - Main disadvantage: Heap operations add a log k factor.

        S3:

        - Approach: Frequency-indexed buckets.
        - Time: O(n)
        - Space: O(n)
        - Input modified: No
        - Main advantage: Linear time.
        - Main disadvantage: Allocates n + 1 buckets.

        [COMMON_PITFALLS]

        - For the bounded top-k heap strategy, use a min-heap so the smallest
          retained frequency can be removed efficiently.
        - Equal frequencies can appear even though the final answer is unique;
          output order is not required.
        - Allocate len(nums) + 1 buckets because a value can appear n times.

        [SOURCE_NOTES]

        - Active submitted implementation uses S3.

        @CONTENT_END
        @NC250_RAW_END
        """

        # -----------------------------------------------------------------
        # YOUR SUBMITTED / PREFERRED CODE
        # -----------------------------------------------------------------

        count = {}
        freq = [[] for i in range(len(nums) + 1)]

        for num in nums:
            count[num] = 1 + count.get(num, 0)
        for num, cnt in count.items():
            freq[cnt].append(num)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res

        # -----------------------------------------------------------------
        # OPTIONAL ALTERNATE / OLD ATTEMPTS
        # -----------------------------------------------------------------
        #
        # S1 CODE - Sorting
        #
        # count = {}
        # for num in nums:
        #     count[num] = 1 + count.get(num, 0)
        #
        # arr = []
        # for num, cnt in count.items():
        #     arr.append([cnt, num])
        # arr.sort()
        #
        # res = []
        # while len(res) < k:
        #     res.append(arr.pop()[1])
        # return res
        #
        #
        # S2 CODE - Min-Heap
        #
        # count = {}
        # for num in nums:
        #     count[num] = 1 + count.get(num, 0)
        #
        # heap = []
        # for num in count.keys():
        #     heapq.heappush(heap, (count[num], num))
        #     if len(heap) > k:
        #         heapq.heappop(heap)
        #
        # res = []
        # for i in range(k):
        #     res.append(heapq.heappop(heap)[1])
        # return res