# 🧠 goldentellus-knowledge

GoldenTellus 的 FDE 学习、成长与方法论中心。这里把原 `goldentellus-roadmap` 的学习路线、技能矩阵和职业资料，与按岗位组织的方法论和案例学习放在同一条连续路径中。

## 🗺️ 三句话导航

> 这是什么：先找到自己的工位，再沿学习路径掌握岗位方法，并通过案例学习形成真实判断。
>
> 上一个：`goldentellus-home` -> **当前** -> 下一个：`goldentellus-playbooks`
>
> 我应该看：先完成 [找到你的工位](./learning/find-your-role.md)，选择学习路径，再进入对应岗位的基础方法与案例学习。

## 🌱 从哪里开始

- [找到你的工位](./learning/find-your-role.md)：判断更适合哪一个 FDE 工位。
- [学习路径](./learning/learning-paths/)：按岗位规划从入门到实践的学习顺序。
- [技能矩阵](./learning/skill-matrix/)：理解各岗位需要具备的能力。
- [阅读清单](./learning/reading-list/)：书籍、课程、播客和社群资源。
- [职业指南](./learning/career-guide/)：第一个项目、作品集、面试和定价参考。
- [认证说明](./learning/certification/)：仍在探索的能力等级设想，不承诺资格或结果。

## 🧩 按岗位学习

- [00-pipeline-fundamentals/](./00-pipeline-fundamentals/)：全员通识与流水线共同语言
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

角色数量和命名可按实际协作调整。跨角色共同语言写入 `00-pipeline-fundamentals`，行业共性模式写入 `08-industry-specific`；不设置独立的案例副本目录。学习路径回答“先学什么”，岗位内容回答“具体怎么判断和工作”，两者互相链接但不重复维护。

文章模板要求标注 `content_type`、难度、角色、相关案例和相关 Demo。当前新增文章均为待填草稿，不代表已发布知识或客户事实。

## ✅ 文章校验

新增或实质更新的文章必须从第一行开始使用 YAML frontmatter，并通过：

```bash
python scripts/validate_knowledge.py
```

当前已登记的“待填草稿”占位文件可暂不补齐 metadata；一旦修改或新增文章，必须同时补齐 frontmatter。
