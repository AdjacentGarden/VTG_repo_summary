# 任务定义与研究分类

Video Temporal Grounding（VTG，视频时序定位）通常指：给定一个未剪辑视频和自然语言查询，输出描述所对应的起止时间。常见名称包括 Temporal Sentence Grounding in Videos（TSGV）、Natural Language Video Localization（NLVL）、Temporal Video Grounding（TVG）和 Video Moment Retrieval（VMR）。具体论文可能采用不同任务边界，应以各自定义为准。

例如，查询“男子放下杯子后打开冰箱”，输出可以是 `[12.4, 18.7]` 秒。模型需要同时识别人物、物体、动作及其先后关系，并找到完整事件的边界。任务与名称的历史背景可参见 [TALL](https://arxiv.org/abs/1705.02101)、[MCN](https://arxiv.org/abs/1708.01641) 和 [TSGV 综述](https://arxiv.org/abs/2201.08071)。

## 任务边界

| 设置 | 输入 | 输出 | 本仓库处理方式 |
| --- | --- | --- | --- |
| 单视频时序定位 / SVMR | 指定视频＋文本 | 时间区间 | 核心范围 |
| 视频库片段检索 / VCMR | 视频库＋文本 | 视频 ID＋时间区间 | 核心范围；与单视频任务分开比较 |
| 多句 / 段落 / 多片段定位 | 多句文本或复杂查询＋视频 | 多个时间区间及对应关系 | 核心范围 |
| 在线 / 流式定位 | 视频流＋查询 | 逐步更新的时间区间 | 核心范围；须限制模型可见的未来帧 |
| 拒绝无关查询 / 开放集定位 | 视频＋可能不匹配的查询 | 区间或拒绝 | 核心范围 |
| 时序证据定位的 VideoQA | 视频＋问题 | 答案＋证据区间 | 时序证据相关扩展，标注标签 |
| Query-dependent Highlight Detection | 视频＋查询 | 片段显著性分数 | 联合 MR/HD 论文收录；独立、无查询的 HD 不系统收录 |
| Dense Video Captioning | 视频 | 区间＋事件描述 | 数据集、统一 VTG 模型相关论文收录；不覆盖整个字幕生成领域 |
| Spatio-temporal / Object Grounding | 视频＋文本 | 轨迹、框、掩码，可能附时间区间 | 纯空间 / 对象定位不计入核心索引 |
| Temporal Action Detection | 视频＋固定类别集合 | 动作类别＋时间区间 | 没有语言查询定位任务的论文不计入核心索引 |

## 从方法机制理解论文

下面是阅读组织方式，并非互斥分类。一篇论文可以同时涉及多个方向。

| 方向 | 关键问题 | 代表阅读入口 |
| --- | --- | --- |
| 候选区间匹配 / 二维时间图 | 如何覆盖不同长度的候选片段？如何利用候选之间的关系？ | CTRL、2D-TAN |
| 边界预测 / 跨模态交互 | 查询信息怎样进入视频表示？起止边界怎样直接预测？ | VSLNet、QD-DETR、BAM-DETR |
| 统一 MR/HD / 预训练 | 多种时间标注和任务能否共享模型？ | Moment-DETR、UniVTG |
| 弱监督 / 点监督 / 半监督 | 不使用完整起止时间标注时，怎样学习定位？ | SCN、Gaussian-based Contrastive Proposal Learning、D3G |
| 去偏 / 组合泛化 | 模型是否利用位置、长度或语言共现等捷径？ | Interventional Video Grounding、Compositional Temporal Grounding |
| 长视频 / 视频库 / 在线 | 如何在计算预算内找到少量相关证据？ | CONE、SnAG、ReVisionLLM、HieraMamba |
| 多模态大模型 | 怎样把视觉内容、时间位置与生成输出对齐？ | VTimeLLM、TimeChat、VTG-LLM、TRACE |
| 训练自由 / 零样本 | 预训练模型、事件分解与提示能否提供定位能力？ | TFVTG、NumPro |
| 强化学习 / 推理 | 时间重叠奖励、数据质量与推理过程各有什么作用？ | Time-R1、TimeLens、MUSEG |
| 开放世界 / 多区间 / 拒绝 | 查询可能不匹配，证据可能是多个片段，怎样预测和评测？ | OmniVTG、Learning to Refuse、TimeLens2 |

这些代表论文的具体机制和来源见 [首页论文卡片](../README.md#代表论文与方法总结)。完整索引中的自动方向标签是根据标题生成的导航提示；它们不等于对全文方法的完整判定。
