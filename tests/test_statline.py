"""统计核心、渲染与 CLI 端到端测试。"""

import contextlib
import io
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

from statline import histogram, percentile, summarize
from statline.cli import main
from statline.core.render import render_histogram, render_summary


class PercentileTest(unittest.TestCase):
    def test_known_values(self):
        values = [10, 20, 30]
        self.assertEqual(percentile(values, 0), 10.0)
        self.assertEqual(percentile(values, 50), 20.0)
        self.assertEqual(percentile(values, 100), 30.0)

    def test_linear_interpolation(self):
        values = [1, 2, 3, 4]
        self.assertAlmostEqual(percentile(values, 25), 1.75)
        self.assertAlmostEqual(percentile(values, 75), 3.25)
        self.assertAlmostEqual(percentile(values, 90), 3.7)

    def test_single_value(self):
        self.assertEqual(percentile([42], 50), 42.0)
        self.assertEqual(percentile([42], 0), 42.0)

    def test_unsorted_input_ok(self):
        self.assertEqual(percentile([30, 10, 20], 50), 20.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            percentile([], 50)
        with self.assertRaises(ValueError):
            percentile([1], 150)


class SummarizeTest(unittest.TestCase):
    def test_known_sample(self):
        stats = summarize([1, 2, 3, 4])
        self.assertEqual(stats["count"], 4)
        self.assertEqual(stats["sum"], 10.0)
        self.assertEqual(stats["min"], 1.0)
        self.assertEqual(stats["max"], 4.0)
        self.assertEqual(stats["mean"], 2.5)
        self.assertEqual(stats["median"], 2.5)
        # 样本标准差(除以 n-1):sqrt(5/3) ≈ 1.2910
        self.assertAlmostEqual(stats["std"], math.sqrt(5 / 3), places=10)
        self.assertAlmostEqual(stats["p25"], 1.75)
        self.assertAlmostEqual(stats["p75"], 3.25)
        self.assertAlmostEqual(stats["p90"], 3.7)

    def test_single_value(self):
        stats = summarize([7])
        self.assertEqual(stats["count"], 1)
        self.assertEqual(stats["std"], 0.0)
        self.assertEqual(stats["mean"], 7.0)
        self.assertEqual(stats["median"], 7.0)

    def test_constant(self):
        stats = summarize([5, 5, 5])
        self.assertEqual(stats["std"], 0.0)
        self.assertEqual(stats["mean"], 5.0)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            summarize([])


class HistogramTest(unittest.TestCase):
    def test_counts_sum_to_total(self):
        values = [1, 2, 2, 3, 9, 10]
        buckets = histogram(values, bins=3)
        self.assertEqual(sum(count for _, _, count in buckets), len(values))
        self.assertEqual(len(buckets), 3)

    def test_bin_edges_cover_min_max(self):
        buckets = histogram([0, 5, 10], bins=2)
        self.assertAlmostEqual(buckets[0][0], 0)
        self.assertAlmostEqual(buckets[-1][1], 10)

    def test_constant_single_bucket(self):
        buckets = histogram([7, 7, 7], bins=5)
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0][2], 3)

    def test_validation(self):
        with self.assertRaises(ValueError):
            histogram([])
        with self.assertRaises(ValueError):
            histogram([1], bins=0)


class RenderTest(unittest.TestCase):
    def test_summary_lines(self):
        out = render_summary(summarize([1, 2, 3, 4]))
        self.assertIn("均值", out)
        self.assertIn("2.5", out)
        self.assertIn("P90", out)
        self.assertIn("3.7", out)

    def test_histogram_bars(self):
        out = render_histogram(histogram([1, 1, 2], bins=2))
        self.assertIn("█", out)
        self.assertIn("(66.7%)", out)


class CliTest(unittest.TestCase):
    def run_cli(self, *args, stdin=""):
        backup = sys.stdin
        stdout, stderr = io.StringIO(), io.StringIO()
        sys.stdin = io.StringIO(stdin)
        try:
            with contextlib.redirect_stdout(stdout), \
                    contextlib.redirect_stderr(stderr):
                code = main(list(args))
        finally:
            sys.stdin = backup
        return code, stdout.getvalue(), stderr.getvalue()

    def test_summary_from_stdin(self):
        code, out, err = self.run_cli(stdin="12\n98\n45\n67")
        self.assertEqual(code, 0, err)
        self.assertIn("样本数", out)
        self.assertIn("中位数", out)
        self.assertIn("█", out)  # 默认带直方图

    def test_json(self):
        code, out, _ = self.run_cli("--json", stdin="1\n2\n3\n4")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["mean"], 2.5)
        self.assertAlmostEqual(data["p25"], 1.75)
        self.assertIn("histogram", data)

    def test_no_hist(self):
        code, out, _ = self.run_cli("--no-hist", stdin="1\n2")
        self.assertEqual(code, 0)
        self.assertNotIn("█", out)

    def test_comma_and_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.csv"
            path.write_text("1,2\n3,4", encoding="utf-8")
            code, out, _ = self.run_cli(str(path), "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["count"], 4)  # 逗号当空白拆分

    def test_bad_number_exit_code(self):
        code, _, err = self.run_cli(stdin="12\nabc\n45")
        self.assertEqual(code, 1)
        self.assertIn("不是数字", err)

    def test_empty_stdin(self):
        code, _, err = self.run_cli()
        self.assertEqual(code, 1)
        self.assertIn("不能为空", err)

    def test_bins_guard(self):
        code, _, err = self.run_cli("--bins", "0", stdin="1")
        self.assertEqual(code, 1)
        self.assertIn("至少为 1", err)


if __name__ == "__main__":
    unittest.main()
