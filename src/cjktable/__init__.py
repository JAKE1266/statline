"""cjktable —— CJK 感知的终端表格与文本排版微库。

让含中文/日文/韩文与 emoji 的文本在等宽终端里真正对齐::

    from cjktable import table, bars, width, pad, truncate

    print(table(
        ["商品", "数量", "单价"],
        [["键盘", 99, 514.32], ["显示器", 7, 1299]],
    ))
"""

from cjktable.core import char_width, pad, truncate, width
from cjktable.render import bars, table

__version__ = "0.1.0"

__all__ = [
    "bars",
    "char_width",
    "pad",
    "table",
    "truncate",
    "width",
    "__version__",
]
