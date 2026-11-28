"""宽度计算与文本排版原语。

宽度规则(近似 ``wcwidth``,覆盖绝大多数日常场景):

- 组合符号(Mn/Me)、格式字符(Cf,含零宽空格/ZWJ/BOM)、控制字符(Cc)→ **0**
- East Asian Width 为 W(宽)或 F(全角)→ **2**
- 常见 emoji(符号类、码位 ≥ U+1F000)→ **2**
- 其余 → **1**

已知局限:ZWJ 组合 emoji(如家庭 emoji)按成员宽度简单累加,可能与个别终端
渲染有出入;需要像素级精确请使用 ``wcwidth``。
"""

from __future__ import annotations

import unicodedata

_ZEROWIDTH = frozenset("\u200b\u2060")

_ALIGN_CHOICES = ("left", "right", "center")


def char_width(ch: str) -> int:
    """单个字符的终端显示宽度(0 / 1 / 2)。"""
    if not isinstance(ch, str) or len(ch) != 1:
        raise ValueError(f"char_width 只接受单个字符,得到:{ch!r}")
    if ch in _ZEROWIDTH:
        return 0
    if unicodedata.category(ch) in ("Mn", "Me", "Cf", "Cc"):
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    if unicodedata.category(ch) == "So" and ord(ch) >= 0x1F000:
        return 2  # 常见 emoji 在等宽终端按 2 列渲染
    return 1


def _display_width(text: str) -> int:
    """内部实现:字符串显示宽度(避免与 pad/truncate 的 width 参数重名)。"""
    return sum(char_width(ch) for ch in text)


def width(text: str) -> int:
    """字符串的终端显示宽度(逐字符累加)。"""
    if not isinstance(text, str):
        raise TypeError(f"text 必须是字符串,得到:{type(text).__name__}")
    return _display_width(text)


def pad(text: str, width: int, align: str = "left") -> str:
    """按显示宽度补空格。

    超宽的 ``text`` 原样返回(不截断);需要先截断请配合 :func:`truncate`。
    ``align`` 支持 ``left`` / ``right`` / ``center``。
    """
    if align not in _ALIGN_CHOICES:
        raise ValueError(f"align 只支持 {'/'.join(_ALIGN_CHOICES)},得到:{align!r}")
    if width < 0:
        width = 0
    gap = max(0, width - _display_width(text))
    if align == "left":
        return text + " " * gap
    if align == "right":
        return " " * gap + text
    left = gap // 2
    return " " * left + text + " " * (gap - left)


def truncate(text: str, width: int, ellipsis: str = "…") -> str:
    """按显示宽度截断,预留省略号空间。

    - 放得下时原样返回;
    - 放不下时在预算内逐字符取用,末尾加 ``ellipsis``;
    - 一个字符都放不下时返回省略号本身(若省略号也放不下则返回空串)。
    """
    if width <= 0:
        return ""
    if _display_width(text) <= width:
        return text
    ell_width = _display_width(ellipsis)
    avail = width - ell_width
    out, used = [], 0
    for ch in text:
        w = char_width(ch)
        if used + w > avail:
            break
        out.append(ch)
        used += w
    if not out:
        return ellipsis if ell_width <= width else ""
    return "".join(out) + ellipsis
