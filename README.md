# 🧠 goldentellus-knowledge

按 FDE 流水线角色组织的方法论与案例学习库。

## 🗺️ 三句话导航

> 这是什么：GoldenTellus 按岗位组织的方法论与案例学习内容。
>
> 上一个：`goldentellus-roadmap` -> **当前** -> 下一个：`goldentellus-playbooks`
>
> 我应该看：先读流水线基础，再选择一个工位，把方法论与案例学习并读，最后回到完整案例复盘。

## 🧩 路径

- [00-pipeline-fundamentals/](./00-pipeline-fundamentals/)：全员通识
- [01-lead-fde/](./01-lead-fde/)：全流程协调
- [02-analyst/](./02-analyst/)：需求诊断
- [03-architect/](./03-architect/)：方案设计
- [04-builder/](./04-builder/)：原型开发
- [05-data-engineer/](./05-data-engineer/)：数据工程
- [06-integrator/](./06-integrator/)：集成交付
- [07-ops/](./07-ops/)：运营迭代
- [08-industry-specific/](./08-industry-specific/)：行业专题

## 📚 内容边界

- `goldentellus-cases` 是完整案例的唯一事实来源，保存六段复盘、授权与脱敏信息、业务上下文和效果数据。
- 本仓库只沉淀可学习、可复用的岗位方法与决策复盘；不得复制完整案例正文，也不得补写未经确认的案例数据。
- `methodology` 用于原理、框架和角色工作法；`case-learning` 用于从已授权、已脱敏案例中提炼的岗位学习内容。
- 案例学习文章必须通过 `related_cases` 关联案例 ID；案例侧以 `related_knowledge` 反向关联文章 ID。

角色数量和命名可按实际协作调整。跨角色共同语言写入 `00-pipeline-fundamentals`，行业共性模式写入 `08-industry-specific`；不设置独立的案例副本目录。

文章模板要求标注 `content_type`、难度、角色、相关案例和相关 Demo。当前新增文章均为待填草稿，不代表已发布知识或客户事实。

## ✅ 文章校验

新增或实质更新的文章必须从第一行开始使用 YAML frontmatter，并通过：

```bash
python scripts/validate_knowledge.py
```

当前已登记的“待填草稿”占位文件可暂不补齐 metadata；一旦修改或新增文章，必须同时补齐 frontmatter。
