"""渲染:统计摘要与直方图(对齐借助同系列微库 cjktable)。"""

from __future__ import annotations

from statline._vendor.cjktable import pad

_LABEL_WIDTH = 10


def _fmt(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def render_summary(summary: dict) -> str:
    """统计摘要 → 对齐文本行。"""
    labels = (("count", "样本数"), ("min", "最小值"), ("max", "最大值"),
              ("mean", "均值"), ("median", "中位数"), ("std", "标准差"),
              ("p25", "P25"), ("p75", "P75"), ("p90", "P90"), ("sum", "总和"))
    lines = []
    for key, label in labels:
        value = summary[key]
        lines.append(f"{pad(label, _LABEL_WIDTH)} {_fmt(value)}")
    return "\n".join(lines)


def render_histogram(buckets: list) -> str:
    """直方图分桶 → 条形 + 数量 + 占比。"""
    total = sum(count for _, _, count in buckets) or 1
    largest = max(count for _, _, count in buckets) or 1
    lines = []
    for start, end, count in buckets:
        blocks = max(1, round(count / largest * 32)) if count else 0
        bar = "█" * blocks
        note = f"{count} ({count / total * 100:.1f}%)"
        lines.append(f"[{_fmt(start):>10}, {_fmt(end):<10}) {bar} {note}")
    return "\n".join(lines)
