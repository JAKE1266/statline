# statline

> 零依赖的统计摘要:管道丢一串数字进来,得到 min/max/均值/中位数/标准差/百分位 + 直方图。
> 与同系列 [termplot](https://github.com/JAKE1266/termplot) 是天生搭档。

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-cjktable%20%28self--built%29-blue)
![Tests](https://img.shields.io/badge/tests-22%20passing-success)

## ✨ 特性

- 📊 **完整摘要**:样本数 / 总和 / 最小 / 最大 / 均值 / 中位数 / 样本标准差 / P25·P75·P90
- 📐 **百分位 = 线性插值法**(与 numpy 默认一致),结果可与主流工具对齐
- 📊 **文本直方图**:等宽分桶、左闭右开(末桶含最大值)、条形 + 占比;
  常量数据自动退化为单桶
- 🚰 **管道友好**:`命令 | statline`;也支持文件,空白与逗号分隔自适应
- 🖥 对齐排版来自同系列微库 [cjktable](https://github.com/JAKE1266/cjktable)
- 🧪 **22 个单元测试**;GitHub Actions 三系统 × 三 Python 版本 CI

## 📦 安装

```bash
git clone https://github.com/JAKE1266/statline.git
cd statline
python -m statline --help      # 克隆即用

pip install .                  # 或安装为命令(获得 statline 命令)
```

## 🚀 快速上手

```bash
printf '12\n98\n45\n67' | statline
statline response_times.log --bins 15
statline data.csv --json
```

### 效果预览

```
样本数     15
最小值     9
最大值     98
均值       53.8667
中位数     56
标准差     29.3546
P25        30.5
P75        75.5
P90        92.2
总和       808

[         9, 26.8      ) ████████████████████████████████ 3 (20.0%)
[      26.8, 44.6      ) ████████████████████████████████ 3 (20.0%)
[      44.6, 62.4      ) ████████████████████████████████ 3 (20.0%)
[      62.4, 80.2      ) ████████████████████████████████ 3 (20.0%)
[      80.2, 98        ) ████████████████████████████████ 3 (20.0%)
```

## ❓ 常见问题

**Q: 标准差是样本标准差还是总体标准差?**
样本标准差(除以 n-1);只有一个样本时为 0。与 `statistics.stdev` 一致。

**Q: 中位数和 P50 一样吗?**
一样——中位数就是线性插值法下的第 50 百分位。

**Q: 数字从哪来?**
文件或标准输入;空白、换行、逗号分隔均可;非法数字报错并给出序号。

**Q: 想发布到 PyPI?**
`statline` 是占位名,发布前请在 `pyproject.toml` 换一个未被占用的名字。

## 📁 项目结构

```
statline/
├── .github/workflows/ci.yml   # CI:三系统 × Python 3.9-3.13
├── src/statline/
│   ├── core/
│   │   ├── stats.py           # 汇总 / 百分位 / 直方图分桶(纯函数)
│   │   └── render.py          # 摘要与直方图渲染(排版来自 cjktable)
│   └── cli.py                 # 命令行入口
├── tests/                     # 22 个单元测试
└── pyproject.toml
```

## 🧪 开发与测试

```bash
PYTHONPATH="src;../cjktable/src" python -m unittest discover -s tests -v
```

## 🗺 路线图

- [ ] `--col N` 支持多列 CSV 的指定列
- [ ] `--out-md` Markdown 报告
- [ ] 与 termplot 联动的组合示例文档

## 📄 许可证

[MIT](LICENSE) —— 可自由使用、修改与分发。

---

*同系列项目:[PyToolBox](https://github.com/JAKE1266/py-toolbox) 多功能工具箱 · [CashBook](https://github.com/JAKE1266/cashbook) 命令行记账本 · [gitdash](https://github.com/JAKE1266/gitdash) Git 终端仪表盘 · [DevBox](https://github.com/JAKE1266/devbox) 前端开发工具箱 · [csvq](https://github.com/JAKE1266/csvq) SQL 查 CSV · [cjktable](https://github.com/JAKE1266/cjktable) CJK 排版微库 · [duviz](https://github.com/JAKE1266/duviz) 磁盘占用可视化 · [httpoke](https://github.com/JAKE1266/httpoke) HTTP 调试工具 · [mdown](https://github.com/JAKE1266/mdown) Markdown→HTML · [msite](https://github.com/JAKE1266/msite) 静态文档站 · [crony](https://github.com/JAKE1266/crony) cron 表达式解析 · [pomo](https://github.com/JAKE1266/pomo) 番茄钟 · [termplot](https://github.com/JAKE1266/termplot) 终端数据图表 · [filewatch](https://github.com/JAKE1266/filewatch) 目录变更监控 · [packpeek](https://github.com/JAKE1266/packpeek) 压缩包检查与安全解压 · [difftool](https://github.com/JAKE1266/difftool) 文本差异 · [wordfreq](https://github.com/JAKE1266/wordfreq) 词频统计*
