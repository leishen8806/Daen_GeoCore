# DAEN For GEO Core

> Current active baseline: [docs/daen-geocore/README.md](docs/daen-geocore/README.md). The older notes below are retained as historical source material and are not authoritative for DAEN GEO CORE.

DAEN / Geo Core 项目的工作区。当前内容来自对话 **「DAEN 域联」** 的整理，尚未与代码仓、正式 PRD 或数据模型核对。

## 当前整理内容

- [产品方向与工作台需求](docs/PRODUCT_DIRECTION.md)：NiuMa 使用反馈、虚拟 AI 办公室构想、需求边界。
- [研发流程与模型分工讨论](docs/ENGINEERING_WORKFLOW.md)：DAEN / Geo Core M1 流程验证设想及成本路由建议。
- [品牌策略与命名候选](docs/BRAND_STRATEGY.md)：DAEN / 域联推荐、备选名称、品牌与技术产品层级。

## 状态约定

- **用户明确表达**：来自用户原话，可作为当前需求输入。
- **对话建议**：由助手提出，尚未得到明确确认，不视为已定方案。
- **待验证**：需要用 DAEN / Geo Core 的真实代码、数据和一次完整交付验证。

目前仅完成对话资料归档；尚未建立正式产品范围、架构、数据模型或实施计划。

## 关联对话

| 对话 | 用途 | 当前记录 |
|---|---|---|
| [DAEN 域联](chatgpt-conversation://6ac34756-c658-83ec-85ca-de987d86c389) | 品牌与项目方向、NiuMa 使用反馈、办公室体验 | 已整理为本项目文档 |
| [DAEN需求与规划](chatgpt-conversation://6ac387c3-4984-83ec-89a2-69ab93e1b731) | DAEN 需求与规划讨论 | 用户提出输出需求文档、边界、技术与 Logo 设计；本次仅建立关联 |

### 定位差异记录

「DAEN需求与规划」的助手提出了 “DAEN = AI Native Organization Operating System”，将虚拟办公室纳入组织运行平台。现有品牌稿提出的是 “Cambodia Location Infrastructure”。两者是不同的产品定位；前者目前仅为助手建议，尚未看到用户明确确认。后续引用该对话时应保留这一差异，不能据此自动覆盖 GEO Core 的位置基础设施方向。

## Software implementation baseline

The `impl/software-baseline` branch establishes the Phase 06E software scaffold: CPython, FastAPI/Uvicorn, Pydantic, PostgreSQL 17 with psycopg and SQLAlchemy Core, Alembic, Docker Compose, and GitHub Actions. Public Phase 05 `/v1` APIs are not implemented yet; infrastructure and provider selection remain open.

```text
uv sync
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
docker compose up
```
