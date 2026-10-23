# Mini LLM Demo Resources

## Knowledge

- [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/)
  官方主线与讲义入口。用于：确定从 tokenizer、Transformer、训练到评估的学习顺序，并在每阶段校准范围。
- [CS336 Assignment 1: Basics](https://github.com/stanford-cs336/assignment1-basics)
  官方作业的任务边界与测试导向参考。用于：核对第一阶段的目标；只参考手册和接口要求，不查看或复制他人实现。
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
  Transformer 的原始论文。用于：理解 self-attention、残差连接、位置编码和模型结构的设计动机。
- [Hugging Face Transformers: Caching](https://huggingface.co/docs/transformers/cache_explanation)
  Transformer KV cache 的框架级说明。用于：理解自回归推理中为什么缓存过去的 K/V、缓存按层保存，以及为什么训练阶段不应把它当作默认优化。
- [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/)
  子词分词与 BPE 的经典论文。用于：理解 tokenizer 的训练目标及合并规则。
- [TinyStories: How Small Can Language Models Be and Still Speak Coherent English?](https://arxiv.org/abs/2305.07759)
  小语言模型与合成故事数据的研究。用于：选择适合单卡、小模型验证的语料与预期。
- [PyTorch documentation](https://docs.pytorch.org/docs/stable/index.html)
  PyTorch 的权威 API 文档。用于：张量语义、自动微分、数据加载、profiling 与 CUDA 行为的精确查证。

## Wisdom (Communities)

- [PyTorch Forums](https://discuss.pytorch.org/)
  由 PyTorch 社区维护的技术论坛。用于：在最小可复现示例准备好后，请教 CUDA、shape、autograd 或性能异常。
- [Hugging Face Forums](https://discuss.huggingface.co/)
  实践型 NLP 社区。用于：比较小模型实验、数据集和评估选择；先描述自己的实现与观察，再吸收建议。

## 计算预算

先在 CPU 和微型语料上验证逻辑，再测量所选设备的内存与吞吐；由练习者显式设置
模型、batch size 和上下文长度。教材不预设个人设备或时间安排。
