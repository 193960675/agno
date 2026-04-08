# The Agent Quickstart: 12 Guided Cookbooks

# Agent 快速入门：12 个引导式 Cookbook 示例

Learn how to build agents with 12 guided cookbooks. We'll go from single tool-using agent to multi-agent teams and step-based workflows through clean, runnable examples.

通过 12 个引导式 Cookbook 学习如何构建 Agent。我们将从单个使用工具的 Agent 出发，逐步过渡到多智能体团队和基于步骤的工作流，全部通过简洁、可直接运行的示例来演示。

Each example can be run independently and contains detailed comments to help you understand what's happening under the hood. We'll use Gemini 3 Flash — fast, affordable, and excellent at tool calling but you can swap in any model with a one line change.

每个示例都可以独立运行，并包含详细的注释帮助你理解底层机制。我们使用 Gemini 3 Flash —— 速度快、价格低、工具调用能力出色，但你只需改一行代码就可以替换为任意模型。

## What You'll Build

## 你将构建什么

| # | File | What You'll Learn | Key Features |
|:--|:---------|:------------------|:-------------|
| 01 | `agent_with_tools.py` | Give an agent tools to fetch real-time data | Tool Calling, Data Fetching |
| 02 | `agent_with_structured_output.py` | Return typed Pydantic objects | Structured Output, Type Safety |
| 03 | `agent_with_typed_input_output.py` | Full type safety on input and output | Input Schema, Output Schema |
| 04 | `agent_with_storage.py` | Persist conversations across runs | Persistent Storage, Session Management |
| 05 | `agent_with_memory.py` | Remember user preferences across sessions | Memory Manager, Personalization |
| 06 | `agent_with_state_management.py` | Track, modify, and persist structured state | Session State, State Management |
| 07 | `agent_search_over_knowledge.py` | Load documents into a knowledge base and search with hybrid search | Chunking, Embedding, Hybrid Search, Agentic Retrieval |
| 08 | `custom_tool_for_self_learning.py` | How to write your own tools and add self-learning capabilities | Custom Tools, Self-Learning |
| 09 | `agent_with_guardrails.py` | Add input validation and safety checks | Guardrails, PII Detection, Prompt Injection |
| 10 | `human_in_the_loop.py` | Require user confirmation before executing tools | Human in the Loop, Tool Confirmation |
| 11 | `multi_agent_team.py` | Coordinate multiple agents by organizing them into a team | Multi-Agent Team, Dynamic Collaboration |
| 12 | `sequential_workflow.py` | Sequentially execute agents/teams/functions | Agentic Workflow, Pipelines |

| # | 文件 | 你将学到 | 关键特性 |
|:--|:---------|:---------|:---------|
| 01 | `agent_with_tools.py` | 给 Agent 赋予工具以获取实时数据 | 工具调用、数据获取 |
| 02 | `agent_with_structured_output.py` | 返回类型化的 Pydantic 对象 | 结构化输出、类型安全 |
| 03 | `agent_with_typed_input_output.py` | 输入输出的完整类型安全 | 输入 Schema、输出 Schema |
| 04 | `agent_with_storage.py` | 跨运行持久化对话 | 持久化存储、会话管理 |
| 05 | `agent_with_memory.py` | 跨会话记住用户偏好 | 记忆管理器、个性化 |
| 06 | `agent_with_state_management.py` | 跟踪、修改和持久化结构化状态 | 会话状态、状态管理 |
| 07 | `agent_search_over_knowledge.py` | 将文档加载到知识库并使用混合搜索 | 分块、嵌入、混合搜索、智能体检索 |
| 08 | `custom_tool_for_self_learning.py` | 如何编写自定义工具并添加自学习能力 | 自定义工具、自学习 |
| 09 | `agent_with_guardrails.py` | 添加输入验证和安全检查 | 安全护栏、PII 检测、提示注入防护 |
| 10 | `human_in_the_loop.py` | 在执行工具前要求用户确认 | 人机协作、工具确认 |
| 11 | `multi_agent_team.py` | 将多个 Agent 组织成团队进行协调 | 多智能体团队、动态协作 |
| 12 | `sequential_workflow.py` | 顺序执行 Agent/团队/函数 | 智能体工作流、管道 |

## Key Concepts

## 核心概念

| Concept | What It Does | When to Use |
|:--------|:-------------|:------------|
| **Tools** | Let agents take actions | Fetch data, call APIs, run code |
| **Storage** | Persist conversation history | Multi-turn conversations and state management |
| **Knowledge** | Searchable document store | RAG, documentation Q&A |
| **Memory** | Remember user preferences | Personalization |
| **State** | Structured data the agent manages | Tracking progress, managing lists |
| **Teams** | Multiple agents collaborating | Dynamic collaboration of specialized agents |
| **Workflows** | Sequential agent pipelines | Predictable multi-step processes and data flow |
| **Guardrails** | Validate and filter input | Block PII, prevent prompt injection |
| **Human in the Loop** | Require confirmation for actions | Sensitive operations, safety-critical tools |

| 概念 | 功能 | 使用场景 |
|:-----|:-----|:---------|
| **工具 (Tools)** | 让 Agent 执行操作 | 获取数据、调用 API、运行代码 |
| **存储 (Storage)** | 持久化对话历史 | 多轮对话和状态管理 |
| **知识库 (Knowledge)** | 可搜索的文档存储 | RAG、文档问答 |
| **记忆 (Memory)** | 记住用户偏好 | 个性化 |
| **状态 (State)** | Agent 管理的结构化数据 | 跟踪进度、管理列表 |
| **团队 (Teams)** | 多个 Agent 协作 | 专业化 Agent 的动态协作 |
| **工作流 (Workflows)** | 顺序 Agent 管道 | 可预测的多步骤流程和数据流 |
| **护栏 (Guardrails)** | 验证和过滤输入 | 阻止 PII 泄露、防止提示注入 |
| **人机协作 (Human in the Loop)** | 操作前要求确认 | 敏感操作、安全关键的工具 |

## Getting Started

## 开始使用

### 1. Clone the repo / 克隆仓库
```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

### 2. Create and activate a virtual environment / 创建并激活虚拟环境
```bash
uv venv .venvs/quickstart --python 3.12
source .venvs/quickstart/bin/activate
```

### 3. Install dependencies / 安装依赖
```bash
uv pip install -r cookbook/00_quickstart/requirements.txt
```

### 4. Set your API key / 设置 API 密钥
```bash
export GOOGLE_API_KEY=your-google-api-key
```

### 5. Run any cookbook / 运行任意 Cookbook
```bash
python cookbook/00_quickstart/agent_with_tools.py
```

**That's it.** No Docker, no Postgres — just Python and an API key.

**就这么简单。** 不需要 Docker，不需要 Postgres —— 只需 Python 和一个 API 密钥。

## Run via Agent OS

## 通过 Agent OS 运行

Agent OS provides a web interface for interacting with your agents. Start the server:

Agent OS 提供了一个与 Agent 交互的 Web 界面。启动服务器：

```bash
python cookbook/00_quickstart/run.py
```

Then visit [os.agno.com](https://os.agno.com) and add `http://localhost:7777` as an endpoint.

然后访问 [os.agno.com](https://os.agno.com)，添加 `http://localhost:7777` 作为端点。

Here's how it looks in action — chat with your agents, explore sessions, monitor traces, manage knowledge and memories, all through a beautiful visual UI.

以下是实际运行效果 —— 通过精美的可视化界面与 Agent 聊天、浏览会话、监控链路追踪、管理知识库和记忆。

https://github.com/user-attachments/assets/aae0086b-86f6-4939-a0ce-e1ec9b87ba1f

> [!TIP]
> To run the agent-with-knowledge, remember to load the knowledge base first using:
> ```bash
> python cookbook/00_quickstart/agent_search_over_knowledge.py
> ```

> [!TIP]
> 要运行知识库 Agent，请先加载知识库：
> ```bash
> python cookbook/00_quickstart/agent_search_over_knowledge.py
> ```

## Swap Models Anytime

## 随时切换模型

Agno is model-agnostic. Same code, different provider:

Agno 与模型无关。相同代码，不同提供商：

```python
# Gemini (default in these examples / 这些示例的默认模型)
from agno.models.google import Gemini
model = Gemini(id="gemini-3-flash-preview")

# OpenAI
from agno.models.openai import OpenAIResponses
model = OpenAIResponses(id="gpt-5.2")

# Anthropic
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")
```

## Run Cookbooks Individually

## 单独运行各 Cookbook

```bash
# 01 - Tools: Fetch real market data / 工具：获取实时市场数据
python cookbook/00_quickstart/agent_with_tools.py

# 02 - Structured Output: Get typed responses / 结构化输出：获取类型化响应
python cookbook/00_quickstart/agent_with_structured_output.py

# 03 - Typed I/O: Full type safety / 类型化输入输出：完整类型安全
python cookbook/00_quickstart/agent_with_typed_input_output.py

# 04 - Storage: Remember conversations / 存储：记住对话
python cookbook/00_quickstart/agent_with_storage.py

# 05 - Memory: Remember user preferences / 记忆：记住用户偏好
python cookbook/00_quickstart/agent_with_memory.py

# 06 - State: Manage watchlists / 状态：管理自选列表
python cookbook/00_quickstart/agent_with_state_management.py

# 07 - Knowledge: Search your documents / 知识库：搜索你的文档
python cookbook/00_quickstart/agent_search_over_knowledge.py

# 08 - Custom Tools: Write your own / 自定义工具：编写自己的工具
python cookbook/00_quickstart/custom_tool_for_self_learning.py

# 09 - Guardrails: Input validation and safety / 安全护栏：输入验证与安全
python cookbook/00_quickstart/agent_with_guardrails.py

# 10 - Human in the Loop: Confirm before executing / 人机协作：执行前确认
python cookbook/00_quickstart/human_in_the_loop.py

# 11 - Teams: Bull vs Bear analysis / 团队：多空分析对决
python cookbook/00_quickstart/multi_agent_team.py

# 12 - Workflows: Research pipeline / 工作流：研究管道
python cookbook/00_quickstart/sequential_workflow.py
```

## Async Patterns

## 异步模式

All examples in this Quick Start use synchronous code for simplicity. For async/await patterns (recommended for production), see `cookbook/02_agents/` which includes async variants of most features.

本快速入门中的所有示例都使用同步代码以保持简洁。如需 async/await 模式（生产环境推荐），请参阅 `cookbook/02_agents/`，其中包含大多数功能的异步版本。

## Learn More

## 了解更多

- [Agno Documentation / Agno 文档](https://docs.agno.com)
- [Agent OS Overview / Agent OS 概述](https://docs.agno.com/agent-os/introduction)
