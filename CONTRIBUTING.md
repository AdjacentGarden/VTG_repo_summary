# 贡献指南

欢迎补充遗漏论文、修复链接、纠正发表信息或提交中文方法总结。

## 收录要求

- 与语言查询的视频时间区间定位直接相关，或明确提出其数据集、评测、综述、时序证据任务。
- CCF A/B 主索引按第七版目录（2026）标注；会议仅收正式 Full / Regular paper。Findings、Workshop、Short、Demo、Companion 和预印本进入补充或待核实列表。
- 提供论文原始页面、出版社 DOI、官方会议录或 OpenReview 的正式录用记录。第三方列表可用于发现，不能单独证明发表状态。
- conference 与 journal 的不同发表版本可以并存，但同一版本的 arXiv 和正式论文应合并，避免重复计数。
- 代码链接优先使用论文或作者项目声明的资源；没有找到时留空，不填猜测路径。
- 不添加无法比较的排行榜数字，不把作者报告的 SOTA 当成跨协议结论。

## 推荐提交格式

```text
标题：
会议 / 期刊与年份：
论文或 DOI 链接：
正式发表证据：
代码 / 项目链接（可选）：
方向与任务设置：
中文方法简介（可选，注明依据）：
版本关系（可选）：
```

## 维护数据和生成索引

`data/papers.json` 是主索引的唯一数据源，`data/supplementary.json` 保存补充资源。`papers/` 下的 Markdown、CSV、BibTeX 和统计由脚本生成。

```bash
python3 scripts/build_catalog.py
python3 scripts/validate.py
python3 scripts/build_catalog.py --check
```

更新论文时同步 `docs/coverage.md` 中的检索日期、范围和未决事项。请查看已有记录保持字段一致；`tag_basis` 区分标题导航标签和经摘要核实的人工分类。`source_urls` 应包含支撑发表记录的来源。
