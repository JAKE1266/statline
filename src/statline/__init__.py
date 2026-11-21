"""statline —— 零依赖的统计摘要与直方图命令行工具。

::

    from statline import histogram, percentile, summarize

    summarize([1, 2, 3, 4])
"""

from statline.core.render import render_histogram, render_summary
from statline.core.stats import histogram, percentile, summarize

__version__ = "1.0.0"

__all__ = ["histogram", "percentile", "render_histogram", "render_summary",
           "summarize", "__version__"]
