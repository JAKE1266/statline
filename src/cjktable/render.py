"""高层渲染:CJK 对齐表格与横向条形图。"""

from __future__ import annotations

from cjktable.core import _display_width as _width
from cjktable.core import pad, truncate

_COLUMN_GAP = "  "


def _is_numeric_column(cells: list) -> bool:
    """忽略空串后,整列都能转成数字即视为数值列(自动右对齐)。"""
    non_empty = [c for c in cells if c != ""]
    if not non_empty:
        return False
    for cell in non_empty:
        try:
            float(cell)
        except ValueError:
            return False
    return True


def table(headers, rows, *, aligns=None, max_col_width: int = 32,
          null_text: str = "") -> str:
    """渲染 CJK 对齐表格。

    :param headers: 表头列表
    :param rows: 二维数据;``None`` 单元格显示为 ``null_text``
    :param aligns: 每列 ``left`` / ``right`` / ``center``;缺省自动判断
        (整列可解析为数字 → 右对齐,否则左对齐)
    :param max_col_width: 单元格最大显示宽度,超出自动截断加省略号
    :param null_text: ``None`` 单元格的占位文本
    """
    headers = [str(h) for h in headers]
    ncols = len(headers)
    cells = []
    for row in rows:
        row = [null_text if cell is None else str(cell) for cell in row]
        if len(row) < ncols:
            row += [""] * (ncols - len(row))
        cells.append([truncate(cell, max_col_width) for cell in row[:ncols]])

    if aligns is None:
        aligns = []
        for i in range(ncols):
            column = [row[i] for row in cells]
            aligns.append("right" if _is_numeric_column(column) else "left")
    if len(aligns) != ncols:
        raise ValueError(f"aligns 数量({len(aligns)})与列数({ncols})不一致")

    widths = [_width(h) for h in headers]
    for row in cells:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], _width(cell))

    lines = [_COLUMN_GAP.join(pad(h, widths[i], aligns[i]) for i, h in enumerate(headers)),
             _COLUMN_GAP.join("-" * widths[i] for i in range(ncols))]
    for row in cells:
        lines.append(_COLUMN_GAP.join(pad(cell, widths[i], aligns[i])
                                      for i, cell in enumerate(row)))
    return "\n".join(lines)


def bars(items, width: int = 32) -> str:
    """横向条形图:``items`` 为 ``(标签, 数值)`` 列表,长度按最大值归一化。

    负值按 0 处理;返回多行字符串,数值按 ``int`` / ``float(:g)`` 展示。
    """
    if not items:
        return "(no data)"
    largest = max((value for _, value in items), default=0) or 1
    lines = []
    for label, value in items:
        value = max(0.0, float(value))
        blocks = round(value / largest * width) if value else 0
        note = f"{value:g}"
        lines.append(f"{pad(truncate(str(label), 14), 16)} {'█' * blocks} {note}")
    return "\n".join(lines)
