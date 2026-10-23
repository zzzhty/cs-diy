# REST API 练习

通过一个通用图像分类示例学习 HTTP 与 REST。练习从请求和响应开始，再实现端点、
错误处理和离线测试。例子不依赖任何已有工作项目或生产服务。

| 阶段 | 主题 | 交付物 |
| --- | --- | --- |
| 01 | HTTP 消息、方法、状态码 | 标注过的合成报文 |
| 02 | 最小 Python 服务 | 健康检查与假分类响应 |
| 03 | 端点与错误设计 | 输入限制及错误码 |
| 04 | 自动化测试与文档 | 离线用例和 OpenAPI |

目标见 [MISSION.md](MISSION.md)，参考资料见 [RESOURCES.md](RESOURCES.md)，
第一课在 [HTTP 请求与响应](lessons/0001-http-request-response-with-curl.html)。
个人笔记与学习进度保存在仓库外，不作为公开教材导入。

从仓库根目录运行 `scripts/serve-web.sh --port 8000`，再访问
`http://<server-ip>:8000/web-development/rest-api/lessons/0001-http-request-response-with-curl.html`。
服务只发布精确文件清单，默认监听 `0.0.0.0`；仅用于可信网络，访问仍受现有网络策略限制。
图像、模型权重和 `.env` 不入库，例子只使用合成输入和显式配置的地址。
