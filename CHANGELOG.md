# 更新日志

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式,
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-11-21

### 新增
- 统计摘要:样本数 / 总和 / 最小 / 最大 / 均值 / 中位数 / 样本标准差 / P25·P75·P90
- 百分位采用线性插值法(与 numpy 默认 ``linear`` 一致)
- 文本直方图:等宽分桶、左闭右开(末桶含最大值)、条形 + 数量 + 占比;
  常量数据自动退化为单桶
- 数据输入:文件或标准输入;空白与逗号分隔自适应;非法数字报错带序号
- `--bins` 分桶数、`--no-hist` 只看摘要、`--json` 结构化输出
- 渲染对齐复用同系列微库 cjktable
- 22 个单元测试;GitHub Actions 三系统 × 三 Python 版本 CI
