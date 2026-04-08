<div align="center" id="top">
  <a href="https://agno.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://agno-public.s3.us-east-1.amazonaws.com/assets/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://agno-public.s3.us-east-1.amazonaws.com/assets/logo-light.svg">
      <img src="https://agno-public.s3.us-east-1.amazonaws.com/assets/logo-light.svg" alt="Agno">
    </picture>
  </a>
</div>

<p align="center">
  Build, run, and manage agentic software at scale.
</p>
<p align="center">
  大规模构建、运行和管理智能体软件。
</p>

<div align="center">
  <a href="https://docs.agno.com">Docs</a>
  <span>&nbsp;•&nbsp;</span>
  <a href="https://github.com/agno-agi/agno/tree/main/cookbook">Cookbook</a>
  <span>&nbsp;•&nbsp;</span>
  <a href="https://docs.agno.com/first-agent">Quickstart</a>
  <span>&nbsp;•&nbsp;</span>
  <a href="https://www.agno.com/discord">Discord</a>
</div>

## What is Agno

## Agno 是什么

Agno is the runtime for agentic software. Build agents, teams, and workflows. Run them as scalable services. Monitor and manage them in production.

Agno 是智能体软件的运行时。构建 Agent（智能体）、Team（团队）和 Workflow（工作流），将它们作为可扩展的服务运行，并在生产环境中进行监控和管理。

| Layer | What it does |
|-------|--------------|
| **Framework** | Build agents, teams, and workflows with memory, knowledge, guardrails, and 100+ integrations. |
| **Runtime** | Serve your system in production with a stateless, session-scoped FastAPI backend. |
| **Control Plane** | Test, monitor, and manage your system using the [AgentOS UI](https://os.agno.com). |

| 层级 | 功能 |
|------|------|
| **框架层 (Framework)** | 构建具备记忆、知识库、安全护栏和 100+ 集成的 Agent、Team 和 Workflow。 |
| **运行时 (Runtime)** | 通过无状态、会话隔离的 FastAPI 后端在生产环境中运行你的系统。 |
| **控制面板 (Control Plane)** | 使用 [AgentOS UI](https://os.agno.com) 测试、监控和管理你的系统。 |

## Quick Start

## 快速开始

Build a stateful, tool-using agent and serve it as a production API in ~20 lines.

用约 20 行代码构建一个有状态、可使用工具的 Agent，并将其部署为生产级 API。

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

agno_assist = Agent(
    name="Agno Assist",
    model=Claude(id="claude-sonnet-4-6"),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(url="https://docs.agno.com/mcp")],
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

agent_os = AgentOS(agents=[agno_assist], tracing=True)
app = agent_os.get_app()
```

Run it:

运行：

```bash
export ANTHROPIC_API_KEY="***"

uvx --python 3.12 \
  --with "agno[os]" \
  --with anthropic \
  --with mcp \
  fastapi dev agno_assist.py
```

In ~20 lines, you get:
- A stateful agent with streaming responses
- Per-user, per-session isolation
- A production API at http://localhost:8000
- Native tracing

仅约 20 行代码，你就获得了：
- 支持流式响应的有状态 Agent
- 按用户、按会话隔离
- 一个生产级 API，地址为 http://localhost:8000
- 原生链路追踪

Connect to the [AgentOS UI](https://os.agno.com) to monitor, manage, and test your agents.

连接 [AgentOS UI](https://os.agno.com) 来监控、管理和测试你的 Agent。

1. Open [os.agno.com](https://os.agno.com) and sign in.
2. Click **"Add new OS"** in the top navigation.
3. Select **"Local"** to connect to a local AgentOS.
4. Enter your endpoint URL (default: `http://localhost:8000`).
5. Name it "Local AgentOS".
6. Click **"Connect"**.

操作步骤：
1. 打开 [os.agno.com](https://os.agno.com) 并登录。
2. 点击顶部导航栏的 **"Add new OS"**。
3. 选择 **"Local"** 连接本地 AgentOS。
4. 输入你的端点 URL（默认：`http://localhost:8000`）。
5. 命名为 "Local AgentOS"。
6. 点击 **"Connect"**。

https://github.com/user-attachments/assets/75258047-2471-4920-8874-30d68c492683

Open Chat, select your agent, and ask:

打开聊天界面，选择你的 Agent，然后提问：

> What is Agno?

The agent retrieves context from the Agno MCP server and responds with grounded answers.

Agent 从 Agno MCP 服务器检索上下文，并给出基于事实的回答。

https://github.com/user-attachments/assets/24c28d28-1d17-492c-815d-810e992ea8d2

You can use this exact same architecture for running multi-agent systems in production.

你可以使用完全相同的架构在生产环境中运行多智能体系统。

## Why Agno?

## 为什么选择 Agno？

Agentic software introduces three fundamental shifts.

智能体软件引入了三个根本性变革。

### A new interaction model

### 全新的交互模型

Traditional software receives a request and returns a response. Agents stream reasoning, tool calls, and results in real time. They can pause mid-execution, wait for approval, and resume later.

传统软件接收请求并返回响应。而 Agent 可以实时流式输出推理过程、工具调用和结果。它们可以在执行中途暂停，等待审批，然后继续执行。

Agno treats streaming and long-running execution as first-class behavior.

Agno 将流式输出和长时间运行的执行视为一等公民。

### A new governance model

### 全新的治理模型

Traditional systems execute predefined decision logic written in advance. Agents choose actions dynamically. Some actions are low risk. Some require user approval. Some require administrative authority.

传统系统执行预先编写的决策逻辑。而 Agent 能动态选择行动。有些操作风险低，有些需要用户审批，有些需要管理员权限。

Agno lets you define who decides what as part of the agent definition, with:

Agno 让你在 Agent 定义中就指定谁决定什么，包括：

- Approval workflows
- Human-in-the-loop
- Audit logs
- Enforcement at runtime

- 审批工作流
- 人机协作（Human-in-the-loop）
- 审计日志
- 运行时强制执行

### A new trust model

### 全新的信任模型

Traditional systems are designed to be predictable. Every execution path is defined in advance. Agents introduce probabilistic reasoning into the execution path.

传统系统被设计为可预测的，每条执行路径都是预先定义的。而 Agent 在执行路径中引入了概率性推理。

Agno builds trust into the engine itself:

Agno 将信任机制内建于引擎之中：

- Guardrails run as part of execution
- Evaluations integrate into the agent loop
- Traces and audit logs are first-class

- 安全护栏（Guardrails）作为执行的一部分运行
- 评估（Evaluations）集成到 Agent 循环中
- 链路追踪和审计日志是一等公民

## Built for Production

## 为生产环境而生

Agno runs in your infrastructure, not ours.

Agno 运行在你的基础设施上，而不是我们的。

- Stateless, horizontally scalable runtime.
- 50+ APIs and background execution.
- Per-user and per-session isolation.
- Runtime approval enforcement.
- Native tracing and full auditability.
- Sessions, memory, knowledge, and traces stored in your database.

- 无状态、可水平扩展的运行时。
- 50+ API 接口和后台执行。
- 按用户和按会话隔离。
- 运行时审批强制执行。
- 原生链路追踪和完整的可审计性。
- 会话、记忆、知识库和追踪数据存储在你自己的数据库中。

You own the system. You own the data. You define the rules.

系统归你所有。数据归你所有。规则由你定义。

## What You Can Build

## 你可以构建什么

Agno powers real agentic systems built from the same primitives above.

Agno 驱动真实的智能体系统，它们都基于上述相同的基本构件。

- [**Pal →**](https://github.com/agno-agi/pal) A personal agent that learns your preferences.
- [**Dash →**](https://github.com/agno-agi/dash) A self-learning data agent grounded in six layers of context.
- [**Scout →**](https://github.com/agno-agi/scout) A self-learning context agent that manages enterprise context knowledge.
- [**Gcode →**](https://github.com/agno-agi/gcode) A post-IDE coding agent that improves over time.
- [**Investment Team →**](https://github.com/agno-agi/investment-team) A multi-agent investment committee that debates and allocates capital.

- [**Pal →**](https://github.com/agno-agi/pal) 一个能学习你偏好的个人助手 Agent。
- [**Dash →**](https://github.com/agno-agi/dash) 一个基于六层上下文的自学习数据 Agent。
- [**Scout →**](https://github.com/agno-agi/scout) 一个管理企业上下文知识的自学习 Agent。
- [**Gcode →**](https://github.com/agno-agi/gcode) 一个随时间自我改进的后 IDE 时代编程 Agent。
- [**Investment Team →**](https://github.com/agno-agi/investment-team) 一个进行辩论和资本配置的多智能体投资委员会。

Single agents. Coordinated teams. Structured workflows. All built on one architecture.

单个 Agent。协调团队。结构化工作流。全部基于同一架构。

## Get Started

## 开始使用

1. [Read the docs](https://docs.agno.com)
2. [Build your first agent](https://docs.agno.com/first-agent)
3. Explore the [cookbook](https://github.com/agno-agi/agno/tree/main/cookbook)

1. [阅读文档](https://docs.agno.com)
2. [构建你的第一个 Agent](https://docs.agno.com/first-agent)
3. 探索 [Cookbook 示例](https://github.com/agno-agi/agno/tree/main/cookbook)

## IDE Integration

## IDE 集成

Add Agno docs as a source in your coding tools:

在你的编程工具中添加 Agno 文档作为数据源：

**Cursor:** Settings → Indexing & Docs → Add `https://docs.agno.com/llms-full.txt`

Also works with VSCode, Windsurf, and similar tools.

同样适用于 VSCode、Windsurf 和类似工具。

## Contributing

## 参与贡献

See the [contributing guide](https://github.com/agno-agi/agno/blob/main/CONTRIBUTING.md).

参见[贡献指南](https://github.com/agno-agi/agno/blob/main/CONTRIBUTING.md)。

## Telemetry

## 遥测

Agno logs which model providers are used to prioritize updates. Disable with `AGNO_TELEMETRY=false`.

Agno 会记录使用了哪些模型提供商，以便确定更新优先级。可通过 `AGNO_TELEMETRY=false` 禁用。

<p align="right"><a href="#top">↑ Back to top / 返回顶部</a></p>
