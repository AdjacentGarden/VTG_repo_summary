# 阅读路线

## 初次进入 VTG

1. **理解任务**：阅读 TALL / CTRL 和 MCN，区分“视频中是什么”与“在何时发生”，了解 Charades-STA、DiDeMo 的任务形成。
2. **理解经典建模**：对比 2D-TAN 的候选区间二维图与 VSLNet 的 span prediction。阅读时画出输入、视频和文本交互、定位头、训练监督。
3. **理解现代基线**：阅读 QVHighlights / Moment-DETR，再看 QD-DETR、UniVTG、BAM-DETR，分析 query conditioning、联合 MR/HD 和边界表示。
4. **理解评测**：先明确 evaluator、视觉特征和数据划分，再比较论文中的数字。见 [评测文档](evaluation.md)。

## 选择专题继续阅读

| 兴趣 | 阅读顺序 | 阅读时追问 |
| --- | --- | --- |
| 降低标注成本 | 弱监督早期方法 → Gaussian-based Contrastive Proposal Learning → D3G / 点监督 → 弱监督大模型方法 | 训练到底能看到什么？伪标签是否包含额外标注或模型先验？ |
| 泛化与去偏 | Interventional Video Grounding → Compositional Temporal Grounding → 去偏 / OOD 论文索引 | 是否同时测试位置偏置、长度偏置和语言组合变化？ |
| 长视频与部署 | CONE → SnAG → ReVisionLLM → HieraMamba → 在线 VTG | 全视频是否真正进入模型？粗阶段漏检后是否可以恢复？ |
| 视频大模型 | VTimeLLM → TimeChat / LITA → VTG-LLM → TRACE / TimeSuite | 时间由绝对秒数、相对 token、帧编号还是连续 head 表达？ |
| 训练自由 | Zero-shot NLVL → TFVTG → NumPro | 对基础模型的依赖、提示和推理调用开销是什么？ |
| 强化学习 | Time-R1 → TimeLens → MUSEG | 格式奖励、重叠奖励、数据筛选与推理分别贡献多少？ |
| 开放世界与可靠性 | Open-set VMR → Learning to Refuse → OmniVTG → TimeLens2 | 目标不存在时是否拒绝？多个片段如何匹配和评估？ |

## 读一篇论文时可以记录的六个问题

- 输入：视频特征还是原始帧？能否访问音频、ASR 或字幕？
- 任务：SVMR、VCMR、单句、多句、多段、在线、负查询，还是时序证据 VideoQA？
- 监督：使用哪些标签、哪些额外数据、怎样生成伪标签？
- 机制：新增模块或训练策略解决哪一个可观察的失败案例？
- 证据：哪些消融真正隔离了机制、数据和 backbone 的贡献？
- 复现：是否发布代码、数据准备步骤、checkpoint 和 evaluator？

完整论文可按 [年份](../papers/by-year.md)、[会议与期刊](../papers/by-venue.md) 或 [方向](../papers/by-topic.md) 检索。路线是编者的阅读组织建议，不代表论文质量或录用概率排名。
