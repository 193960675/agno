# Agno Demo
# Agno 演示

5 agents, 1 team, 1 workflow served via AgentOS. Each agent learns from interactions and improves with every use.
5个智能体、1个团队、1个工作流通过AgentOS提供服务。每个智能体都能从交互中学习，并在每次使用中不断改进。

## Overview
## 概览

### Agents
### 智能体

| Agent | Description |
|-------|-------------|
| **Dash** | An adaptive data agent that queries and interprets your data — improving its understanding of your schema, metrics, and priorities with every interaction. |
| **Pal** | A personal agent that learns your preferences, context, and history. |
| **Gcode** | A lightweight coding agent that writes, reviews, and iterates on code. No bloat, no IDE lock-in — just a fast agent that gets sharper the more you use it. |
| **Scout** | A self-managing context agent that researches, drafts, and refines information stored in s3 buckets. |
| **Seek** | A self-learning research agent that investigates complex topics over time, building persistent knowledge that compounds across sessions. |

| 智能体 | 描述 |
|-------|-------------|
| **Dash** | 一个自适应数据智能体，用于查询和解释您的数据——随着每次交互不断改进对您数据结构、指标和优先级的理解。 |
| **Pal** | 一个个人智能体，学习您的偏好、上下文和历史记录。 |
| **Gcode** | 一个轻量级编码智能体，用于编写、审查和迭代代码。无臃肿、无IDE锁定——只是一个越用越敏锐的快速智能体。 |
| **Scout** | 一个自管理上下文智能体，用于研究、起草和完善存储在S3存储桶中的信息。 |
| **Seek** | 一个自学习研究智能体，随时间调查复杂主题，构建跨会话累积的持久知识。 |

### Team
### 团队

| Team | Description |
|------|-------------|
| **Research Team** | Seek and Scout working together as a team. |

| 团队 | 描述 |
|------|-------------|
| **研究团队** | Seek和Scout作为团队协同工作。 |

### Workflow
### 工作流

| Workflow | Description |
|----------|-------------|
| **Daily Brief** | A workflow that sources and surfaces new developments (using seek), tracks metrics (using dash), and produces a daily digest (using scout). |

| 工作流 | 描述 |
|----------|-------------|
| **每日简报** | 一个工作流，用于获取和展示新进展（使用seek）、跟踪指标（使用dash），并生成每日摘要（使用scout）。 |

## Architecture
## 架构

All agents share a common foundation:
所有智能体共享一个共同的基础：

- **Model**: `OpenAIResponses(id="gpt-5.2")`
- **模型**：`OpenAIResponses(id="gpt-5.2")`
- **Storage**: PostgreSQL + PgVector for knowledge, learnings, and chat history
- **存储**：PostgreSQL + PgVector用于知识、学习和聊天历史
- **Knowledge**: Dual knowledge system — static curated knowledge + dynamic learnings discovered at runtime
- **知识**：双知识系统——静态精选知识 + 运行时发现的动态学习
- **Search**: Hybrid search (semantic + keyword) with OpenAI embeddings (`text-embedding-3-small`)
- **搜索**：混合搜索（语义+关键词）配合OpenAI嵌入模型（`text-embedding-3-small`）
- **Learning**: `LearningMachine` in `AGENTIC` mode — agents decide when to save learnings
- **学习**：`AGENTIC`模式下的`LearningMachine`——智能体自行决定何时保存学习内容

## Getting Started
## 快速开始

### 1. Clone the repo
### 1. 克隆仓库

```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

### 2. Create and activate the demo virtual environment
### 2. 创建并激活演示虚拟环境

```bash
./scripts/demo_setup.sh
source .venvs/demo/bin/activate
```

### 3. Run PgVector
### 3. 运行PgVector

```bash
./cookbook/scripts/run_pgvector.sh
```

### 4. Export environment variables
### 4. 导出环境变量

```bash
export OPENAI_API_KEY="..."      # Required for all agents
export EXA_API_KEY="..."         # Optional (Exa MCP is currently free)
```
```bash
export OPENAI_API_KEY="..."      # 所有智能体必需
export EXA_API_KEY="..."         # 可选（Exa MCP目前免费）
```

### 5. Load data and knowledge
### 5. 加载数据和知识

```bash
cd cookbook/01_demo

python -m agents.dash.scripts.load_data
python -m agents.dash.scripts.load_knowledge
python -m agents.scout.scripts.load_knowledge
```

### 6. Run the demo
### 6. 运行演示

```bash
python -m run
```

### 7. Connect via AgentOS
### 7. 通过AgentOS连接

- Open [os.agno.com](https://os.agno.com) in your browser
- Click "Add AgentOS"
- Add `http://localhost:7777` as an endpoint
- Click "Connect"

- 在浏览器中打开 [os.agno.com](https://os.agno.com)
- 点击"添加AgentOS"
- 添加 `http://localhost:7777` 作为端点
- 点击"连接"

## Evals
## 评估

Test cases covering all agents, team, and workflow. Uses string-matching validation with `all` or `any` match modes.
涵盖所有智能体、团队和工作流的测试用例。使用带有`all`或`any`匹配模式的字符串匹配验证。

```bash
# Run all evals
# 运行所有评估
python -m evals.run_evals

# Filter by agent
# 按智能体过滤
python -m evals.run_evals --agent dash
python -m evals.run_evals --agent seek

# Verbose mode (show full responses on failure)
# 详细模式（失败时显示完整响应）
python -m evals.run_evals --verbose
```

## Agno Features Demonstrated
## 演示的Agno功能

| Feature | Where |
|---------|-------|
| LearningMachine (AGENTIC mode) | All 5 agents |
| CodingTools | Gcode |
| ReasoningTools | Gcode |
| SQL Tools | Dash, Pal |
| MCP Tools | Seek (Exa), Scout (Exa), Dash (Exa), Pal (Exa) |
| Knowledge (hybrid search) | All agents |
| Persistent Memory | Pal, Seek |
| Teams (coordinate mode) | Research Team |
| Workflows (parallel steps) | Daily Brief |
| Scheduled Tasks | Daily Brief |
| AgentOS | run.py |

| 功能 | 位置 |
|---------|-------|
| LearningMachine（AGENTIC模式） | 全部5个智能体 |
| CodingTools | Gcode |
| ReasoningTools | Gcode |
| SQL工具 | Dash, Pal |
| MCP工具 | Seek (Exa), Scout (Exa), Dash (Exa), Pal (Exa) |
| 知识（混合搜索） | 全部智能体 |
| 持久记忆 | Pal, Seek |
| 团队（协调模式） | 研究团队 |
| 工作流（并行步骤） | 每日简报 |
| 定时任务 | 每日简报 |
| AgentOS | run.py |
