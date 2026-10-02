# Grok 数据更新任务

仓库：https://github.com/tinajin2026/ai-video-competitor-research

目标：为已有 37 家竞品持续采集真实 X 帖子及互动观察，保留来源与采集时间；提交通过校验的数据，使网站在合并 main 后自动更新。

## 每次执行

1. 读取 README.md 的「Grok BOT 数据契约」和 data/accounts.json。账号标记为未核验的先核对官方身份；无映射的产品先提交映射变更供确认，不猜账号。
2. 只使用能访问并验证的原帖/API 数据。母公司账号逐帖判断产品相关性；Seedance、Dreamina 分开归属；缺失互动计数写 null，不能虚构为 0。
3. 从最新 main 新建分支，将新观察追加为 data/inbox/<UTC日期时间>-<唯一批次>.jsonl。每行字段严格按 README；原帖 ID 与 URL 一致。更新互动计数时写一条新的 collected_at 观察，不篡改过去观察。
4. 在仓库根目录运行下面三个命令。脚本会读取全部 inbox，合并重复记录并生成页面。只提交本次新增的 JSONL 文件；生成的 public 和 data/x-posts.json 由发布工作流重建，无需提交。
5. 创建 PR，写明时间范围、涉及产品、观察条数、原始来源和缺失项。CI 成功后由仓库所有者审阅合并；合并 main 自动发布 GitHub Pages。没有 GitHub 写权限时输出 JSONL 文件交给所有者，不能声称已经同步。

```sh
python3 scripts/ingest_x.py
python3 scripts/build.py
python3 scripts/test_site.py
```

单批上限 10,000 条，每个文件上限 10 MiB。校验失败时整批不写入；根据文件名、行号修正后重试。不要绕过校验或修改测试以接受错误记录。

## 边界

- 只更新授权产品的 X 观察，不擅自修改流量快照、分析口径、网页代码或 workflow。
- 不把 AI 总结填进原帖 text；relevance_evidence 是产品归属依据，不是增长效果结论。
- 付费 API/X/Grok/GitHub 凭据只放运行环境的 secret，不提交仓库或输出到帖子数据。
- GitHub 凭据仅授予这个仓库需要的内容/PR 权限；不需要修改 Actions workflow 的权限。
- 当前 X 页面为空是尚未接入的真实状态；不得用示例或合成帖子填充。
- GitHub Pages 随 main 更新；原 chatgpt.site 地址是独立部署，不会被这个 workflow 更新。

完整 schema、账号限制及未知值处理以 README.md 与 scripts/ingest_x.py 为准。当前 workflow 全量重放 inbox，超过批量上限前需由维护者安排归档与持久化调整，BOT 不自行删除历史。
