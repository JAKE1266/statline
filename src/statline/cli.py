"""statline 命令行入口。

::

    echo -e "12\\n98\\n45\\n67" | statline
    statline data.csv --bins 15 --json
    statline response_times.log --no-hist
"""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .core.render import render_histogram, render_summary
from .core.stats import histogram, summarize


def _configure_standard_streams() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def _parse_numbers(text: str) -> list:
    tokens = text.replace(",", " ").split()
    values = []
    for index, token in enumerate(tokens, start=1):
        try:
            values.append(float(token))
        except ValueError as exc:
            raise ValueError(f"第 {index} 个值不是数字:{token!r}") from exc
    return values


def cmd_summary(args) -> int:
    if args.file:
        from pathlib import Path

        file = Path(args.file)
        if not file.is_file():
            raise FileNotFoundError(f"文件不存在:{file}")
        text = file.read_text(encoding="utf-8-sig")
    else:
        text = sys.stdin.read()

    values = _parse_numbers(text)
    summary = summarize(values)

    if args.json:
        payload = {key: round(value, 6) if isinstance(value, float) else value
                   for key, value in summary.items()}
        if not args.no_hist:
            payload["histogram"] = [
                {"lo": round(start, 6), "hi": round(end, 6), "count": count}
                for start, end, count in histogram(values, bins=args.bins)]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(render_summary(summary))
    if not args.no_hist:
        print()
        print(render_histogram(histogram(values, bins=args.bins)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="statline",
        description="statline —— 零运行时依赖的统计摘要命令行工具:"
                    "min/max/均值/中位数/标准差/百分位 + 文本直方图",
    )
    parser.add_argument("--version", action="version", version=f"statline {__version__}")
    parser.add_argument("file", nargs="?", default=None,
                        help="数据文件(每行/每空白分隔一个数字;缺省读标准输入)")
    parser.add_argument("--bins", type=int, default=10, help="直方图分桶数(默认 10)")
    parser.add_argument("--no-hist", action="store_true", help="不输出直方图")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    return parser


def main(argv=None) -> int:
    _configure_standard_streams()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.bins < 1:
        print("错误:--bins 至少为 1", file=sys.stderr)
        return 1
    try:
        return cmd_summary(args)
    except KeyboardInterrupt:
        print("\n已取消。")
        return 130
    except BrokenPipeError:
        return 0
    except (ValueError, TypeError, OSError) as exc:
        print(f"错误:{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
