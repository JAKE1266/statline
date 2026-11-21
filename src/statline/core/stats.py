"""统计计算(纯函数):汇总、百分位(线性插值法)、等宽直方图分桶。"""

from __future__ import annotations

import math


def percentile(values: list, p: float) -> float:
    """线性插值百分位(与 numpy 默认 ``linear`` 法一致)。``p`` 取 0-100。"""
    if not values:
        raise ValueError("values 不能为空")
    if not 0 <= p <= 100:
        raise ValueError(f"百分位必须在 0-100:{p}")
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * p / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def summarize(values: list) -> dict:
    """单变量摘要:n / 总和 / 最小 / 最大 / 均值 / 中位数 / 样本标准差 / P25·P75·P90。"""
    if not values:
        raise ValueError("values 不能为空")
    numbers = [float(v) for v in values]
    count = len(numbers)
    mean = sum(numbers) / count
    if count > 1:
        variance = sum((v - mean) ** 2 for v in numbers) / (count - 1)
        std = math.sqrt(variance)
    else:
        std = 0.0
    return {
        "count": count,
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": mean,
        "median": percentile(numbers, 50),
        "std": std,
        "p25": percentile(numbers, 25),
        "p75": percentile(numbers, 75),
        "p90": percentile(numbers, 90),
    }


def histogram(values: list, bins: int = 10) -> list:
    """等宽直方图分桶,返回 ``[(区间下界, 区间上界, 数量), ...]``。

    区间左闭右开,最后一桶闭区间(最大值计入)。``values`` 全相等时
    退化为单桶。``bins`` 至少为 1。
    """
    if not values:
        raise ValueError("values 不能为空")
    if bins < 1:
        raise ValueError(f"bins 至少为 1:{bins}")
    numbers = [float(v) for v in values]
    lo, hi = min(numbers), max(numbers)
    if lo == hi:  # 常量数据:单桶
        return [(lo, hi, len(numbers))]
    width = (hi - lo) / bins
    buckets = [0] * bins
    for value in numbers:
        index = int((value - lo) / width)
        if index >= bins:  # 最大值落入最后一桶
            index = bins - 1
        buckets[index] += 1
    result = []
    for index, count in enumerate(buckets):
        start = lo + index * width
        end = start + width if index < bins - 1 else hi
        result.append((start, end, count))
    return result
