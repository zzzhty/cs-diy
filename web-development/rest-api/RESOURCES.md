# REST API Resources

## Knowledge

- [MDN：HTTP 概述](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Overview)
  HTTP 的权威中文入门。用于：请求/响应模型、方法、头部、状态码的第一参考。
- [MDN：HTTP 消息](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Messages)
  请求与响应报文的逐段解剖图。用于：看懂 curl -v 输出的每一段。
- [MDN：HTTP 状态码](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)
  状态码全集。用于：4xx/5xx 排障时查语义。
- [FastAPI 官方文档（中文）](https://fastapi.tiangolo.com/zh/)
  Python Web 框架的官方资料，用于端点实现与 OpenAPI 文档。
- [Full Stack open 中文版 part 3](https://fullstackopen.com/zh/part3)
  REST API 概念、测试与错误处理思路。用于：概念主线；实现为 Node.js，只取设计思想不抄代码。
- [Requests 文档](https://requests.readthedocs.io/en/latest/)
  Python HTTP 客户端。用于：从本地脚本调用检测 API、写自动化测试。
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
  HTTP 语义的最终规范。用于：方法语义、状态码含义有争议时的仲裁。

- [RFC 9112 §2.1: HTTP/1.1 Message Format](https://www.rfc-editor.org/rfc/rfc9112.html#section-2.1)
  HTTP/1.1 起始行、头部与消息体的格式；消息体可包含二进制数据。

## Wisdom (Communities)

- [FastAPI GitHub Discussions](https://github.com/fastapi/fastapi/discussions)
  框架作者维护的问答社区。用于：异步推理、上传处理、性能问题的实践建议。
- [Stack Overflow](https://stackoverflow.com/questions/tagged/http+rest)
  通用 HTTP/REST 问答。用于：报文与状态码语义的边界问题；提问时附上最小可复现的 curl 命令。

## 练习准备

- 独立编写最小示例，明确公开许可；不导入现有业务项目代码。
- 用合成输入和假响应建立接口测试，再按需要选择 Python 框架。
