# 数据字段与维护口径

主索引为 [papers.json](../data/papers.json)，补充为 [supplementary.json](../data/supplementary.json)。所有索引可通过 Python 标准库脚本重新生成。

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定记录标识；DOI / 原始 URL 的摘要值。可作 BibTeX key 与年份页锚点 |
| `title` | 正式标题；少量数学／HTML 标记作导航规范化，原值可留在 `publisher_title` |
| `title_aliases` | 已核实的预印本或旧标题别名，可选 |
| `authors` | 作者列表；保留来源提供的姓名顺序／格式 |
| `year` | 会议年；期刊以最早公开元数据年份为主，详见覆盖说明 |
| `venue` / `publication_type` | 会议／期刊简称；`conference` 或 `journal` |
| `ccf_grade` | 按 2026 年第七版统一赋予的 A / B venue 等级 |
| `paper_url` / `doi` / `arxiv_url` | 原始论文页、DOI、同版本预印本；未核实项留空 |
| `code_url` / `code_status` | 原论文或作者仓库入口及核验依据；空值不表示没有开源 |
| `tags` / `tag_basis` | 可多选的方向导航；`title` 为标题推断，`abstract_reviewed` 为摘要核实 |
| `scope` | `core`、`dataset`、`pretraining` 或 `temporal_evidence_qa` |
| `summary_zh` | 原创中文阅读摘要；多数非卡片条目为空 |
| `display_name` / `card_group` | 首页卡片的短名称与组织类别，可选 |
| `source_urls` / `source_kind` | 支撑标题、发表与资源链接的可追溯来源，不是全文已读标记 |
| `publication_dates` | 原始 Crossref 公开、在线或印刷日期，数组精度可为年／月／日 |
| `pages` / `article_number` | 有来源时保留页码或文章号，不猜测 |
| `format_status` | `journal_article`、`official_main_proceedings` 或 `main_proceedings_format_not_individually_audited`；最后一项尚未逐篇确认 Full/Regular |
| `related_record_ids` | 同标题的不同发表版本；关联不是全文扩展关系已经审定的保证 |
| `checked_at` | 本次元数据／链接对应关系核对日期 |

补充记录使用 `status` 和 `exclusion_reason` 说明预印本、Findings、Short 或范围外发表等情况；明确出版类型时保存 `eligibility_source`。主索引之外的 venue 不强行赋予 CCF A/B 等级。

`references.bib` 使用简称 venue 和来源作者名，不伪造卷号、期号或出版地。正式投稿引用时可进一步从对应出版社下载完整 BibTeX 核对。

CSV 为 UTF-8；多作者、多标签和多来源用 ` ; ` 分隔。总数按主 JSON 条目计算，各方向可以重叠；补充记录不计入主索引。详见 [覆盖说明](coverage.md)。
