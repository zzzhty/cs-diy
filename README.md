# CS 自学仓库

这是一个按领域组织的个人自学仓库，目前聚焦 Web 开发与机器学习两个方向。每个专题独立可运行、便于复盘，目标是逐步积累可复用的实现与学习记录。个人笔记、学习进度和实验日志保存在仓库外。领域划分与课程推荐以 [csdiy.wiki](https://csdiy.wiki/)（CS自学指南）为校准参考。

## 目录

| 目录 | 内容 |
| --- | --- |
| [`web-development/`](web-development/) | Web 开发：前端（HTML/CSS/JS、React）与 REST API 项目 |
| [`machine-learning/`](machine-learning/) | 机器学习：经典算法到从零实现语言模型（保留领域目录结构） |
| [`shared/`](shared/) | 跨领域可复用的工具与模板 |
| [`assets/`](assets/) | 跨轨道共享的课程页面组件（样式与练习组件） |
| [`scripts/`](scripts/) | 辅助脚本，如静态网页的远程访问服务 |

## 专题组织约定

每个学习轨道（track）是一个独立的教学工作区，成熟范例见 [`machine-learning/deep-learning/language-modeling-from-scratch/`](machine-learning/deep-learning/language-modeling-from-scratch/)：

```text
my-track/
├── MISSION.md          # 学习使命：Why、成功标准、约束、范围外
├── RESOURCES.md        # 可信资料与社区清单
├── lessons/            # 短小可交互的学习单元（HTML，编号递增）
├── reference/          # 适合快速复习与打印的速查文档（HTML）
├── assets/             # 轨道专属页面组件（可选；通用组件用根级 assets/）
└── project-dir/        # 动手项目：README、notes、src、tests
```

纯动手的小专题可只用项目模板：`README + notes + src + tests`（机器学习方向沿用 `notebooks/`），README 至少记录学习目标、资源来源、环境依赖、运行命令与结论。轨道的 README 另需给出学习地图和当前项目清单。

## 建议的学习顺序

1. `web-development/frontend/`：HTML/CSS/JS 基础，再进入 React（Full Stack open part 1–2）
2. `web-development/rest-api/`：通用图像分类 API 练习——先补 HTTP 基础（MDN + curl），再独立实现最小示例（Full Stack open part 3 作概念参考）
3. `machine-learning/` 与 Web 方向并行推进；需要深入 React 工程实践时再进 CS571

顺序不是硬约束，可按兴趣和项目需要调整。

## 开始一个新专题

1. 在对应领域下新建专题目录，领域本身没有的先建领域目录并写 `README.md`。
2. 先写该专题的 `README.md`，明确目标、资源和验收标准。
3. 使用固定随机种子（如适用），并记录环境与依赖版本。
4. 可复用代码沉淀到 `shared/`，领域专属工具放在领域目录内（如 `machine-learning/shared/`）。

## 远程访问静态课件

当通过远程会话学习时，使用以下命令将仓库内的静态网页绑定到所有网络接口：

~~~bash
scripts/serve-web.sh --port 8000
~~~

然后从可达的局域网或 VPN IP 打开相应页面，例如：

~~~text
http://<server-ip>:8000/machine-learning/deep-learning/language-modeling-from-scratch/
~~~

该脚本默认绑定到 0.0.0.0，不依赖图形桌面或 file URL。端口是否能从外部访问仍取决于主机防火墙、VPN 或 SSH 转发配置。

### 发布边界与验证

服务需要 POSIX 系统和 Python 3，仅发布 `scripts/web-files.txt` 中逐个列出的课件 HTML、CSS、JavaScript，以及课件链接必需的已审阅 Markdown。新增课件或资源时，审阅后把精确路径加入此清单；不要加入目录、通配符、私密笔记或生成目录。

目录浏览已关闭。`.git`、`.env`、未列出的文件、`NOTES.md`、学习记录、模型和输出目录不会发布。符号链接（包括父目录）会使启动失败；服务在启动时读取安全文件快照，运行期间不读取仓库，修改课件后需重启。白名单内容本身会向所有能连接端口的人公开，启动前仍需检查其中没有敏感内容。

服务没有身份认证或 TLS，只用于可信局域网/VPN 的课件浏览，不应直接暴露到互联网。默认仍为 `0.0.0.0:8000`；只需本机访问时可以显式传入 `--host 127.0.0.1`。现有防火墙、VPN、SSH 转发策略仍然有效。

验证（Python 3；练习组件测试另需 Node.js，无第三方依赖）：

~~~bash
python3 -m unittest discover -s tests -v
node tests/test_lesson.js
~~~

测试使用临时仓库副本和本机临时端口，覆盖两个入口的 HTTP 响应、课件相对链接、私密路径拒绝、编码穿越、符号链接，以及练习答错后重试。练习答错时不会提前标出正确选项，答对后锁定当前题目；刷新页面可重新练习。两份组件保留各自默认反馈文案，以同一回归测试防止行为漂移。

## 说明

本仓库以学习和练习为目的。不要提交敏感信息、模型权重或体积过大的生成文件；数据集与外部资源优先记录来源和获取方式。`machine-learning/` 由原独立仓库合并而来，保留其内部结构与 `.gitignore`。Web 方向涉及 `.env` 等本地配置时一律不提交，密钥与 token 只放环境变量。
