# 检索范围、来源与覆盖说明

检索与元数据核对截至 **2026-10-05**。目标是尽可能覆盖 CCF A/B 会议和期刊的 VTG 相关论文，采用“广泛发现 → 标题／摘要范围筛选 → 正式出版元数据核对 → 去重及版本关联”的流程。当前统计见 [stats.json](../data/stats.json)。

## 主索引的范围

- 语言查询的单视频时序定位，包括 TSGV、TVG、NLVL、VMR 等名称。
- 视频库片段检索、多句／段落、多区间、在线／流式、弱监督／低标注、去偏与泛化。
- 将 VTG 作为明确任务的视频大模型、强化学习和训练自由方法。
- 直接相关的数据集、benchmark、评测和综述。TACoS 原始数据论文作为 2013 年的历史资源保留，现代核心方法主要从 2017 年开始。
- 明确使用时间证据的视频问答，单独标为 `scope=temporal_evidence_qa`；数据与预训练资源也可标为 `dataset` / `pretraining`。

纯空间／对象框／轨迹定位、没有语言查询的动作检测、整段视频检索、视频生成、一般视频问答和独立高亮检测不系统收录。某些跨任务论文经原始介绍确认具有 VTG 或时间证据任务后纳入，因此收录范围并非仅靠标题关键词判定。

## CCF 分级依据

使用 **第七版中国计算机学会推荐国际学术会议和期刊目录（2026 正式版）**。来源为 [CCF 目录入口](https://www.ccf.org.cn/Academic_Evaluation/By_category/)、[丽水学院科研处发布页](https://kyc.lsu.edu.cn/2026/0518/c1772a367789/page.htm) 与其托管的 [正式目录 PDF](https://kyc.lsu.edu.cn/_upload/article/files/20/77/2cbaa3754eb9aff9ed74cafed8ff/23a8de02-594c-445f-b084-69b0193c05b3.pdf)。

本次核对采用正式 PDF 的会议／期刊表；机器可读分类辅助参考 [2026 目录转写](https://github.com/haozhou-wong/ccf-recommended-list-2026-markdown)。本仓库仅保存使用到的 venue 映射，见 [venues.json](../data/venues.json)。

ICLR、TMM 按此版标为 A，IJCAI 按此版标为 B。所有年份统一采用这一版，因此历史论文的标签可能不同于其发表当年的 CCF 版本。ACM Computing Surveys 未在所采用的目录中列出；其 VTG 综述保留在补充索引，不赋予主索引 CCF 等级。

分级是 **venue 分级**，不能单独证明某篇论文属于 Full/Regular。已核实的 Findings、Workshop、Short、Demo、Companion、Doctoral Symposium 不计入主索引。出版社只提供主会议录元数据、但本次没有逐篇阅读议程确认类型的记录，使用 `main_proceedings_format_not_individually_audited`；后续若确认其属于特殊类型，应移入补充。

## 检索过程与检索式

| 来源 | 本次实际使用方式 | 能支持的判断 |
| --- | --- | --- |
| [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | 16 组标题查询，每组获取最多 1000 条；额外按发现标题查询，并按 DOI 补充页码及出版日期 | 出版社注册的标题、作者、DOI、刊物／会议录和日期；不自动支持全文方法结论 |
| [CVF Open Access](https://openaccess.thecvf.com/menu) | 搜索 CVPR 2017–2026、ICCV 2017/2019/2021/2023/2025 官方索引；打开匹配论文页，另补 ECCV 原始条目 | 正式会议、年份、标题、作者、摘要 |
| [PMLR](https://proceedings.mlr.press/) | 核查 ICML 2024、2025、2026 官方卷的候选与逐篇条目 | 正式会议录与摘要，弥补 Crossref 登记空缺 |
| [ICLR Proceedings](https://proceedings.iclr.cc/) | 搜索 2024–2026 官方索引，并核对 Conference 条目 | 正式主会发表，避免只凭 arXiv / 项目录用声明 |
| [NeurIPS Proceedings](https://proceedings.neurips.cc/) | 核查 Moment-DETR、SCDM、SeViLA 等核心条目 | 会议年份、Main Conference Track 和原始摘要 |
| [ACL Anthology](https://aclanthology.org/) | 核查 ACL / NAACL / COLING / TACL 和 Findings 边界，补无 DOI 条目 | 正式论文、作者、主会与 Findings 区分 |
| [arXiv](https://arxiv.org/) | 核查代表论文预印本、摘要、首发时间和资源链接 | 预印本存在及内容；不单独证明正式录用 |
| 作者 GitHub / 项目页 | 检查代表论文的 README 标题或原论文给出的资源链接 | 代码入口与论文对应关系；未实际复现全部代码 |

Crossref `query.title` 的 16 组检索式为：

```text
temporal grounding
video moment retrieval
video moment localization
temporal sentence localization
natural language video localization
language grounding videos
video corpus moment retrieval
temporal video grounding
temporal language localization
language guided activity localization
sentence localization videos
query based localization video
video paragraph grounding
moment grounding
natural language temporal localization
video temporal localization
```

发现阶段交叉参考以下综述与公开列表，随后用原始发表记录确认：

- [Temporal Sentence Grounding in Videos: A Survey and Future Directions](https://arxiv.org/abs/2201.08071)
- [A Survey on Video Temporal Grounding with Multimodal Large Language Model](https://arxiv.org/abs/2508.10922)
- [Soldelli/Awesome-Temporal-Language-Grounding-in-Videos](https://github.com/Soldelli/Awesome-Temporal-Language-Grounding-in-Videos)
- [Tangkfan/Awesome-Temporal-Video-Grounding](https://github.com/Tangkfan/Awesome-Temporal-Video-Grounding)
- [iLearn-Lab/TPAMI26-Awesome-MLLMs-for-Video-Temporal-Grounding](https://github.com/iLearn-Lab/TPAMI26-Awesome-MLLMs-for-Video-Temporal-Grounding)
- [NeverMoreLCH/Awesome-Video-Grounding](https://github.com/NeverMoreLCH/Awesome-Video-Grounding)

## 去重、年份与核验层次

**同一发表版本**优先按 DOI 去重，无 DOI 时按标题、venue 与年份合并。arXiv 与正式论文链接保存在一个条目中。标题发生明显变化时人工补充 `title_aliases`，如 QVHighlights / Moment-DETR 和 CG-DETR。TimeZero / Time-R1 的同一更新预印本以最终正式版本组织，不重复按方法别名计数。

**不同发表版本**保留独立记录，精确同标题的会议版／期刊版用 `related_record_ids` 关联；标题改变的扩展版尚未全部建立关系。因此“条目数”不等于独立算法数量。

**年份**：会议使用正式会议年；期刊默认使用元数据最早公开日期（early access / online first 可早于卷期年）。`publication_dates` 保留原始注册日期。若元数据仅有年份／月份，则按其公开精度处理；截止日期后的记录不纳入。

**摘要与标签**：代表方法的中文总结依据链接的摘要或原始项目介绍独立撰写；没有阅读全文并做逐篇质量打分。标题生成的方向标签标为 `title`，经摘要核实的标为 `abstract_reviewed`。论文卡片是阅读入口，不能作为充分的实验结论或全文评审。

**代码**：有链接表示已核对标题对应关系或原论文资源入口，不表示已运行、复现或检查完整开源情况。空链接表示本次未核实，不能解读为没有公开代码。

## 已知覆盖缺口

1. **不能保证穷尽**。Crossref 的单组检索最多取 1000 条，登记缺失、标题缩写或无关键术语的论文可能遗漏；缺 DOI 的 ACL / Springer / PMLR 工作也需要持续补充。
2. **官方逐届扫描不均衡**。本次完整获取了上述 CVPR / ICCV 索引及近三年 ICLR / ICML 索引；其他会议、ECCV 与期刊主要依靠 Crossref、列表和定向核查，尚未逐届遍历全部卷期。较早文献和非典型标题仍可能漏收。
3. **DBLP API 受反爬页面限制**，本次未完成 DBLP 全量交叉检索；CCF 站点部分访问受保护，改用已注明的正式 PDF 镜像。未将受限页面当作已读取证据。
4. **出版类型仍需完善**。已依据主办方议程／录用列表排除 SIGIR Short Paper 与 ACM MM Doctoral Symposium 示例，但未逐篇核对每条会议记录的 Full/Regular 类别。
5. **2026 年仍在更新**。只有截止日之前能找到的正式来源进入主索引；新预印本或只有作者录用声明的条目暂存补充。
6. **任务邻域不完全**。纯空间定位、通用视频问答和稠密字幕生成不全量覆盖；包含时间证据的交叉任务需要阅读原文判断是否应补入。

修正或新增记录时，请给出原始证据并更新元数据，再运行生成与校验脚本。这个仓库通过可追溯来源和明确边界提高覆盖，欢迎贡献遗漏。
