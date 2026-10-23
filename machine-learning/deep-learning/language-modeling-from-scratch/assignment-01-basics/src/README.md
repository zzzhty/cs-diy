# 源码布局

按职责拆分实现，避免把训练、数据和模型逻辑堆叠在单个 notebook 中。建议逐步创建以下模块：

- tokenizer.py：词表训练、编码、解码与持久化。
- data.py：语料读取、数据划分、批采样。
- model.py：Transformer 配置、注意力、MLP、Block 和语言模型。
- optim.py：AdamW 与学习率调度。
- train.py：训练入口、检查点、日志和恢复。
- evaluate.py：loss/perplexity 与文本生成评估。

先保持接口小且显式；当一个模块拥有稳定测试后再抽取公共工具。
