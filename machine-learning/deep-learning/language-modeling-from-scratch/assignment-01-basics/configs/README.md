# 配置

将每个正式实验的可变参数保存为独立配置文件，例如：

~~~text
tiny-stories-debug.yaml
tiny-stories-baseline.yaml
~~~

配置至少包含数据版本、tokenizer 参数、模型尺寸、优化器参数、训练步数、随机种子和评估间隔。不要在配置中保存密钥、本地绝对路径或大模型权重路径。
