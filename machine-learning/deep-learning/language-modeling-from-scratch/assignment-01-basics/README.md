# 第一阶段：Basics

目标是独立做出一个可训练、可评估的小型自回归 Transformer 语言模型。这一阶段对应 CS336 的 tokenizer、模型结构、优化器和最小模型训练主线，但实现和实验记录由本仓库独立维护。

## 前置基础

在开始实现前，先完成 [两周 LLM 入门基础](../foundations/index.html)。它假定你已有深度学习基础，并补齐 token、下一个 token 预测、交叉熵、perplexity、QKV、因果注意力和 KV cache。KV cache 先作为推理概念学习；首个训练基线不需要依赖它。

## 交付物

1. 可训练的子词 tokenizer，并提供编码/解码测试。
2. 带因果注意力掩码的 Decoder-only Transformer。
3. 参数更新正确的 AdamW 优化器及学习率调度接口。
4. 可恢复的训练循环：数据划分、随机种子、检查点和日志。
5. 留出集交叉熵与 perplexity 评估，以及一组定性生成样例。

## 推荐实现顺序

1. **环境与基线**：固定 Python/PyTorch 版本、随机种子和一个极小文本语料；记录字符级或均匀分布基线。
2. **Tokenizer**：实现训练、encode、decode 和保存/加载；先用小语料做往返与确定性测试。
3. **数据批处理**：实现 token 序列切块、输入/目标右移和批采样；确认没有跨训练/验证集泄漏。
4. **模型**：依次完成 embedding、位置编码、RMSNorm/LayerNorm、注意力、MLP、残差连接和语言模型头。
5. **优化与训练**：实现 AdamW、梯度裁剪、学习率调度、检查点恢复和训练日志。
6. **评估**：在固定验证集上报告 loss/perplexity；保存固定 prompt 的生成结果，便于横向比较。

## 完成标准

- tokenizer 的 encode/decode 往返、特殊 token 和序列化行为均有测试。
- 模型输出形状正确，且未来 token 的变化不会影响此前位置的 logits。
- 优化器的单步更新与已知小例子一致。
- 模型能在极小数据集上明显过拟合，证明训练链路可用。
- 固定 seed 与配置可重复得到同量级的验证指标。
- 每次正式训练均有对应的实验记录，使用 [实验模板](experiments/experiment-template.md)。

## 目录

~~~text
assignment-01-basics/
├── configs/       # 可提交的训练配置
├── experiments/   # 实验记录，不提交权重与大型日志
├── notebooks/     # 推导、可视化和一次性探索
├── src/           # 独立实现
└── tests/         # 正确性与回归测试
~~~

开始编码前，先从 tests/ 定义第一个可观察行为，再在 src/ 实现最小版本。

## 配套学习材料

- [两周 LLM 入门基础](../foundations/index.html)
- [第 1 课：下一个 token 与微型过拟合验证](../lessons/0001-next-token-and-overfit.html)
- [第 2 课：QKV、因果注意力与 KV cache](../lessons/0002-qkv-attention-and-kv-cache.html)
- [核心语言模型速查](../reference/core-language-modeling.html)
- [QKV 与 KV cache 速查](../reference/qkv-and-kv-cache.html)
- [Mini LLM 练习清单](../reference/mini-llm-demo-contract.html)
