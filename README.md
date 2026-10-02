# AI 视频竞品研究站

37 家竞品的行业工作台与独立 HTML 研究页。公开数据来自已核验本地采集快照：流量为 2026-08，官网为 2026-10-02；当前没有实时 X 连接。

## 本地运行

只需 Python 3.9+，无第三方依赖，无 Bun/npm 安装。

```sh
python3 scripts/ingest_x.py
python3 scripts/build.py
python3 scripts/test_site.py
python3 -m http.server 8770 --directory public
```

访问 http://localhost:8770 。也可直接打开 public/index.html；独立页正文已预渲染，图表需要 JavaScript。源码模块低于 500 行。public 为生成产物，应修改 src、scripts 和 data 后重建。

## 结构

- `data/snapshot.json`：白名单公开研究数据，不含原始网页全文与 API 凭据。
- `data/editorial.json`：每家公司独立研究重点、自身实验和后续跟踪事项。
- `data/accounts.json`：稳定产品 ID 到 X 账号映射，初始来自用户提供清单，接入前核对官方身份。
- `data/inbox/*.jsonl`：机器人提交的原帖观察。
- `data/x-posts.json`：经校验合并后的帖子及最近 100 次互动快照。
- `scripts/research.py`：派生指标和关键词词面分类。
- `scripts/company_page.py`：独立研究页；`build.py`：完整站点构建。
- `public/competitors/<product_id>/index.html`：37 个稳定分享地址。
- `public/data/companies/<product_id>.json`：单公司可下载数据。

## Grok BOT 数据契约

每行一个 JSON 对象，只接受这些字段：

| 字段 | 要求 |
| --- | --- |
| product_id | accounts.json 中的稳定 ID |
| post_id | X 状态 ID，数字字符串 |
| author_handle | 不含 @，必须匹配该产品映射 |
| url | https://x.com/作者/status/帖子ID；不得带跟踪参数 |
| published_at | 原帖发布时间，UTC ISO-8601，以 Z 结尾 |
| collected_at | 互动计数采集时间，UTC ISO-8601，以 Z 结尾 |
| text | 原帖正文，非空，最多 30,000 字符；不要将模型总结冒充原帖 |
| metrics | likes/reposts/replies/quotes/views/bookmarks；非负整数或 null，未知不能写成 0 |
| relevance_evidence | 为什么与该产品相关，最多 1,000 字符；公司级账号尤其要逐帖核实 |

入库运行 `python3 scripts/ingest_x.py data/inbox/<文件>.jsonl`。整批先校验再写入；错误会给出文件名与行号，不泄漏输入正文。相同 product_id + post_id 幂等，旧采集不覆盖新计数，同时间重复观察忽略。较新计数可下降（平台修正），因此不假设单调递增。时间顺序非法、身份不符和异常大文件均拒绝。写入有文件锁及原子替换。输入中的 HTML 作为文本转义，不执行。

没有账号的产品先经人工确认更新 accounts.json 再采集。Seedance 与 Dreamina 保持两个产品 ID；不要自动把全部 @dreamina_ai 帖子算给两者。Higgsfield 用户清单 handle 与官网社交元数据有差异，应接入前核对。OpenAI、xAI 等母账号必须提供产品相关性依据。当前工具只校验格式/映射，不能证明原帖真实；BOT 必须从原帖/API 获取并保留出处。

## GitHub 仓库与持续更新

仓库：[tinajin2026/ai-video-competitor-research](https://github.com/tinajin2026/ai-video-competitor-research)。机器人执行说明见 [GROK.md](GROK.md)。

此目录为仓库根目录，已准备 CI 与 Pages 工作流。初始化/推送时只推本目录，不要把上一级 `.secrets` 或完整采集工作区放进去。无需把 TabAPI/X/Grok 密钥写入网页或仓库。

1. 克隆上述仓库，从 main 创建数据更新分支。
2. Settings → Pages 将 Source 设为 GitHub Actions。已提供 `pages.yml`，main 提交后校验并发布 `public/`。
3. 给 Grok BOT 最小的目标仓库内容写权限，建议提交 PR；机器人只提交 data/inbox 文件，不改页面代码。
4. 工作流重放 inbox、校验并生成所有独立页面。失败时阻止新部署，保留上一版本。

当前公开 Sites 链接属于本次快照；GitHub Actions 的 Pages 部署是独立目标。GitHub 提交不会自动更新 Sites。若以 GitHub + BOT 为长期维护方式，启用 Pages 后使用仓库的 Pages 链接。需要继续更新 Sites 时，通过 Sites 保存并部署新版本。

## 更新网站数据

没有将付费 API key 带入此仓库。需要新增流量月份时先通过授权采集端取得数据，在边界校验后更新公开快照；宏观固定月份/派生指标也应同时重新计算。当前不是“改一个日期就自动刷新”的看板。export_snapshot.py 是从本地完整报告导出白名单的单次迁移工具，会覆盖 src 中继承的工作台源文件，后续维护不要重复运行它。

## 来源与限制

访问是域名级估算，不是用户/付费/收入。品牌词数量不代表品牌访问份额。Direct 不等于留存。新旧域不相加，母域背景不伪装成产品流量。官网动作、事件日期与观察日期分开。试用、年付折月、续费与促销条件分开。所有建议是自身实验，不宣称竞品达到了该效果。完整原始 API 返回留在本地采集包，公开站只保留数据和研究摘记。
