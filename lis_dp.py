"""
最长上升子序列（LIS, Longest Increasing Subsequence）

定义
----
给定整数序列 nums，找出一个最长的子序列，使得其中元素严格递增。
子序列不必连续，但必须保持原相对顺序。

本文件实现 O(n²) 动态规划，并附带测试与 dp 数组含义说明。
"""

from typing import List, Tuple


def length_of_lis(nums: List[int]) -> int:
    """
    返回最长严格上升子序列的长度。

    时间复杂度: O(n²)
    空间复杂度: O(n)

    dp 数组含义
    ------------
    dp[i] = 以 nums[i] 结尾的最长严格上升子序列的长度。

    为什么必须“以 nums[i] 结尾”？
    因为子序列是否能再接上 nums[j]（j > i），只取决于“当前这条链的最后一个数”
    是否小于 nums[j]。把状态钉在结尾下标上，转移才是确定的。

    状态转移
    --------
    初始化: dp[i] = 1
        （任何一个单独元素都是长度为 1 的上升子序列）

    对每个 i，枚举所有 j in [0, i):
        若 nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)
        含义: 把 nums[i] 接到“以 nums[j] 结尾”的那条上升链后面。

    答案
    ----
    max(dp)，因为全局最长链不一定以最后一个元素结尾。
    """
    n = len(nums)
    if n == 0:
        return 0

    # dp[i]: 以 nums[i] 结尾的 LIS 长度
    dp = [1] * n

    for i in range(n):
        for j in range(i):
            # 只有严格小于才能接到 nums[i] 前面
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_with_trace(nums: List[int]) -> Tuple[int, List[int], List[int]]:
    """
    在 length_of_lis 基础上记录前驱，复原一条具体的 LIS。

    返回:
        (最长长度, 一条 LIS, 完整的 dp 数组)

    prev[i] 含义
    ------------
    prev[i] = 构成 dp[i] 时，nums[i] 所接上的那个下标 j；
    若 dp[i] == 1（单独成链），则 prev[i] = -1。
    """
    n = len(nums)
    if n == 0:
        return 0, [], []

    dp = [1] * n
    prev = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 从 dp 最大的下标往回走，得到一条 LIS（逆序再翻转）
    end = max(range(n), key=lambda i: dp[i])
    seq = []
    while end != -1:
        seq.append(nums[end])
        end = prev[end]
    seq.reverse()

    return dp[max(range(n), key=lambda i: dp[i])], seq, dp


def explain_dp_example(nums: List[int]) -> None:
    """打印一道例题的 dp 演变，便于对照注释理解。"""
    n = len(nums)
    dp = [1] * n
    print(f"nums = {nums}")
    print("dp[i] = 以 nums[i] 结尾的 LIS 长度\n")

    for i in range(n):
        choices = []
        for j in range(i):
            if nums[j] < nums[i]:
                choices.append(f"接在 nums[{j}]={nums[j]} 后 -> {dp[j]}+1={dp[j] + 1}")
                dp[i] = max(dp[i], dp[j] + 1)
        extra = ("；候选: " + "; ".join(choices)) if choices else "；前面没有更小的数，保持 1"
        print(f"i={i}, nums[i]={nums[i]}, dp[{i}]={dp[i]}{extra}")

    print(f"\n完整 dp = {dp}")
    print(f"LIS 长度 = max(dp) = {max(dp) if dp else 0}")


def _run_tests() -> None:
    # (输入, 期望长度)
    cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),  # 例如 2,3,7,101 或 2,3,7,18
        ([0, 1, 0, 3, 2, 3], 4),            # 0,1,2,3
        ([7, 7, 7, 7], 1),                  # 严格递增，相等不能接
        ([], 0),
        ([5], 1),
        ([1, 2, 3, 4], 4),
        ([4, 3, 2, 1], 1),
        ([3, 1, 2], 2),
        ([1, 3, 2, 4], 3),
    ]

    for nums, expected in cases:
        got = length_of_lis(nums)
        assert got == expected, f"length_of_lis({nums}) = {got}, expected {expected}"
        length, seq, dp = lis_with_trace(nums)
        assert length == expected
        assert len(dp) == len(nums)
        if nums:
            assert max(dp) == expected
            # 复原出的序列必须是严格递增、且是原数组的子序列
            assert all(seq[k] < seq[k + 1] for k in range(len(seq) - 1))
            assert len(seq) == expected
            it = iter(nums)
            assert all(x in it for x in seq), f"{seq} is not a subsequence of {nums}"

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
    print("\n--- dp 数组逐步推演示例 ---")
    explain_dp_example([10, 9, 2, 5, 3, 7, 101, 18])
