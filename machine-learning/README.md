# 机器学习算法练习

这是一个用于学习、实现和比较机器学习算法的个人仓库。内容按学习范式与算法类型组织，目标是让每个实验都能独立运行、便于复盘，并逐步积累可复用的实现。

## 目录

| 目录 | 内容 |
| --- | --- |
| [`supervised-learning/`](supervised-learning/) | 有监督学习：分类与回归 |
| [`unsupervised-learning/`](unsupervised-learning/) | 无监督学习：聚类、降维与关联规则 |
| [`reinforcement-learning/`](reinforcement-learning/) | 强化学习：价值学习、策略学习与环境交互 |
| [`deep-learning/`](deep-learning/) | 深度学习：神经网络基础、常见架构与从零实现语言模型 |
| [`shared/`](shared/) | 可复用的数据处理、评估、可视化工具 |
| [`datasets/`](datasets/) | 数据集说明与获取方式；大型原始数据不提交到仓库 |

## 实验组织约定

每个具体算法建议使用独立目录，例如 `supervised-learning/classification/logistic-regression/`：

```text
logistic-regression/
├── README.md       # 问题、公式、运行方法和结论
├── notebooks/      # 探索与推导
├── src/            # 可复用实现
└── tests/          # 基础正确性测试（按需添加）
```

每个实验的 README 至少记录：学习目标、数据集来源、依赖、运行命令、评价指标，以及结果与反思。

## 建议的学习顺序

1. 线性回归、逻辑回归、k 近邻、朴素贝叶斯、决策树
2. 支持向量机、集成方法、聚类、主成分分析
3. 模型评估、特征工程和超参数优化
4. 神经网络、卷积网络、序列模型与强化学习

## 开始一个新实验

1. 在对应分类下新建算法目录。
2. 先写该实验的 `README.md`，明确目标和数据。
3. 使用固定随机种子，并记录环境与依赖版本。
4. 将可复用代码沉淀到 `shared/`，避免复制粘贴。

## 远程访问静态课件

当通过远程 Codex 会话学习时，使用以下命令将仓库内的静态网页绑定到所有网络接口：

~~~bash
scripts/serve-web.sh --port 8000
~~~

然后从可达的局域网或 VPN IP 打开相应页面，例如：

~~~text
http://<server-ip>:8000/deep-learning/language-modeling-from-scratch/
~~~

该脚本默认绑定到 0.0.0.0，不依赖图形桌面或 file URL。端口是否能从外部访问仍取决于主机防火墙、VPN 或 SSH 转发配置。

本目录内的 `scripts/serve-web.sh` 复用根级安全课件服务，并保留上述 `/deep-learning/...` URL。它使用根级 `scripts/web-files.txt` 中 `machine-learning/` 下的精确条目；不会发布其他文件或列出目录。更改课件后需重启。服务需 POSIX/Python 3，仅用于可信网络，无认证或 TLS；安全边界和测试命令见[仓库根 README](../README.md)。

## 说明

本仓库以学习和练习为目的。数据集请优先记录来源和下载方式；不要提交敏感信息、模型权重或体积过大的生成文件。
