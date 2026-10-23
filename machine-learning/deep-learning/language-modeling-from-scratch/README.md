# 从零实现语言模型

这个学习轨道以 [Stanford CS336：Language Modeling from Scratch](https://cs336.stanford.edu/) 为主线，从数据表示、模型结构、训练到评估，独立实现一个小型自回归语言模型。

课程材料用于学习目标和理论参考；这里的代码必须自行实现，不复制课程作业的实现或解答。每个阶段都应先建立正确性证据，再追求训练速度或模型规模。

## 学习地图

| 阶段 | 主题 | 可交付成果 |
| --- | --- | --- |
| 01 | Basics | tokenizer、Transformer、优化器、训练循环与最小语言模型 |
| 02 | Systems | 性能剖析、内存分析和 GPU 算子优化 |
| 03 | Scaling | 参数、数据与计算量的缩放实验 |
| 04 | Data | 语料清洗、过滤、去重与数据混合 |
| 05 | Post-training | 监督微调、偏好优化与推理强化学习 |

当前只启动第一阶段；后续阶段在前一阶段具备可复现基线后再创建。

## 当前项目

- [assignment-01-basics/](assignment-01-basics/)：从 tokenizer 到训练与评估的端到端最小实现。

## 教学工作区

- [MISSION.md](MISSION.md)：通用小型语言模型练习的目标与范围。
- [RESOURCES.md](RESOURCES.md)：后续课程与实现所依赖的可信资料。
- [lessons/](lessons/)：短小、可交互的学习单元。
- [reference/](reference/)：适合快速复习和打印的核心概念与项目清单。

## 远程浏览

从仓库根目录运行以下命令：

~~~bash
scripts/serve-web.sh --port 8000
~~~

随后使用以下形式的 URL 打开课程首页：

~~~text
http://<server-ip>:8000/deep-learning/language-modeling-from-scratch/
~~~

课程页、参考页和共享资源都使用相对 HTTP 路径，因此可在远程浏览器中正常导航。

## 工作原则

- 优先在 CPU 和极小数据集上验证正确性，再使用 GPU 训练。
- 每次可比较的实验都记录随机种子、代码版本、数据版本、配置和结果。
- 原始数据、模型权重和训练产物不提交到 Git；在实验记录中保留来源与生成方法。
- 先写能证明行为的测试，例如可逆编码、因果掩码和小数据过拟合。
