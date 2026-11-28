# 更新日志

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式,
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.1] - 2026-11-28

### 修复
- 移除内嵌 cjktable 对应的 Git 运行时依赖,安装不再需要访问 GitHub
- 将内嵌 cjktable 移入 `statline._vendor`,避免与其他发行包共享或覆盖顶级包
- CI 改为先构建 wheel/sdist,再在仓库外安装真实 wheel 后运行测试与冒烟,
  不再依赖步骤级 `PYTHONPATH`,修复 `src` 布局下冒烟阶段找不到模块的问题
- 固定 Ubuntu 24.04 与 macOS 15 Intel runner,避免 `*-latest` 镜像漂移导致
  Python 3.9 不可用
- CLI 启动时将标准流统一为 UTF-8,旧编码控制台不再因中文标签或提示崩溃

### 新增
- 已安装发行包冒烟:校验版本、元数据、私有 vendor、模块入口、控制台入口与管道统计
- `MANIFEST.in` 将 CHANGELOG 与测试脚本纳入 sdist
- 旧编码环境回归测试,测试总数达 23 项
- CI 扩展为构建 + 三系统 × Python 3.9/3.10/3.12/3.13,共 13 个作业

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
