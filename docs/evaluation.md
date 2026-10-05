# 评测指标与复现注意事项

## 常用指标

对预测区间 $P=[p_s,p_e]$ 和真实区间 $G=[g_s,g_e]$，连续时间区间的 temporal IoU 为：

$$
\operatorname{tIoU}(P,G)=\frac{\max(0,\min(p_e,g_e)-\max(p_s,g_s))}{\max(p_e,g_e)-\min(p_s,g_s)}.
$$

上式适用于两个合法且非零长度的区间。无效、反向或零长度区间如何处理，须遵循目标 benchmark 的官方 evaluator。

| 指标 | 含义 | 注意事项 |
| --- | --- | --- |
| R@K, IoU=τ / R@K@τ | 每个查询的前 K 个预测中，是否至少有一个达到 tIoU 阈值 τ | 比较时 K、τ、split 和多标注处理方式必须一致 |
| mIoU | 对查询的预测与标注计算 IoU，再汇总 | Top-1、best-of-K、多真实区间的处理可能不同，不能只看名称 |
| MR mAP | 按区间置信度排名，计算不同 IoU 阈值下 AP，再取均值 | 不等于 R@1；要注明阈值集合及匹配规则 |
| HD mAP / HIT@1 | 衡量显著性排序或最高分片段是否为高亮 | 属于 Highlight Detection 指标，不可与 MR mAP 混用 |
| VCMR Recall | 预测视频和时间区间同时匹配的检索指标 | 检索库大小、视频召回及定位召回需要一起说明 |
| 拒绝 / 相关性指标 | 判断查询是否有有效目标 | 需要与定位指标一起报告，避免“全部拒绝”或“全部给区间” |

单段定位可从 [VSLNet](https://aclanthology.org/2020.acl-main.585/) 理解；联合 MR/HD 的多区间指标参见 [QVHighlights / Moment-DETR](https://github.com/jayleicn/moment_detr)；视频库设置参见 [TVR](https://github.com/jayleicn/TVRetrieval)。多区间集合评测不能简单套用单区间公式，应以论文和 evaluator 为准。

## 比较论文结果时记录什么

1. **数据版本和划分**：Charades-STA、ActivityNet Captions、QVHighlights 原版与重新标注版分别记录。不得混用 legacy 与 TimeLens-Bench 的结果。
2. **视觉表示**：C3D、I3D、CLIP、SlowFast、InternVideo、原始帧等输入条件分别说明；音频、ASR、字幕和辅助 caption 也属于输入条件。
3. **监督来源**：完整边界、单点、视频级匹配、自动伪标注、SFT、RL、额外预训练数据应注明。目标数据集上 zero-shot 与“整个系统从未训练”不同。
4. **时间采样**：输入帧数、FPS、片段步长、时间窗口、长视频裁剪、时长归一化与秒数转换必须明确。
5. **推理过程**：模型参数量、单次 / 迭代调用、候选数、API 模型版本、工具次数、token 和耗时影响公平性。
6. **评测代码**：官方 evaluator 的版本、预测格式、排序、NMS、无效时间戳处理及随机种子需保存。
7. **开放集 / 在线**：负查询构造、拒绝阈值的选择集、流式模型对未来帧的访问权限不能省略。

[TimeLens](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_TimeLens_Rethinking_Video_Temporal_Grounding_with_Multimodal_LLMs_CVPR_2026_paper.html) 讨论标注质量对评测的影响；[Moment of Untruth](https://openaccess.thecvf.com/content/WACV2025/html/Flanagan_Moment_of_Untruth_Dealing_with_Negative_Queries_in_Video_Moment_WACV_2025_paper.html) 和 [Learning to Refuse](https://openaccess.thecvf.com/content/CVPR2026/html/Lee_Learning_to_Refuse_Refusal-Aware_Reinforcement_Fine-Tuning_for_Hard-Irrelevant_Queries_in_CVPR_2026_paper.html) 提供负查询设置。WACV 资源作为补充收录，不计入本仓库的 CCF A/B 主索引。

本仓库暂不制作跨协议的统一性能排行榜。已有论文报告的数值应在输入、监督、数据版本和 evaluator 一致时比较。
