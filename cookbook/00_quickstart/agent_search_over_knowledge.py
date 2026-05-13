"""
知识库上的智能搜索 - 带知识库的 Agent
====================================
此示例展示了如何为 Agent 提供可搜索的知识库。
Agent 可以搜索文档（PDF、文本、URL）来回答问题。

关键概念：
- Knowledge：可搜索的文档集合（PDF、文本、URL）
- 智能搜索：Agent 决定何时搜索知识库
- 混合搜索：结合语义相似性和关键词匹配。

可以尝试的示例提示：
- "Agno 是什么？"
- "AgentOS 是什么？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

from agno.knowledge.embedder.ollama import OllamaEmbedder

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

embeddings = OllamaEmbedder(id="bge-m3", host="http://127.0.0.1:11434", dimensions=1024)

a = embeddings.get_embedding("The quick brown fox jumps over the lazy dog.")

print(f"Embedding : {a}")

# Print the embeddings and their dimensions
print(f"Embeddings: {a[:5]}")
print(f"Dimensions: {len(a)}")

knowledge = Knowledge(
    name="Agno Documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        collection="agno_docs",
        path="tmp/chromadb",
        persistent_client=True,
        # 启用混合搜索 - 使用 RRF 结合向量相似性和关键词匹配
        search_type=SearchType.hybrid,
        # RRF (Reciprocal Rank Fusion) 常数 - 控制排名平滑度。
        # 较高值（如 60）给予较低排名结果更多权重，
        # 较低值使顶级结果更占主导。默认为 60（根据原始 RRF 论文）。
        hybrid_rrf_k=60,
        embedder=embeddings
    ),
    # 查询时返回 5 个结果
    max_results=5,
    # 在 agent 数据库中存储内容的元数据，table_name="agno_knowledge"
    contents_db=agent_db,
)

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是 Agno 框架和构建 AI Agent 的专家。

## 工作流程

1. 搜索
   - 关于 Agno 的问题，始终先搜索知识库
   - 从查询中提取关键概念以有效搜索

2. 综合
   - 结合多个搜索结果的信息
   - 优先官方文档而非通用知识

3. 呈现
   - 以直接答案开头
   - 有帮助时包含代码示例
   - 保持实用和可操作

## 规则

- 回答 Agno 问题前始终搜索知识库
- 如果答案不在知识库中，说明这一点
- 实现问题包含代码片段
- 保持简洁 —— 开发者想要答案，不是长文\
"""

instructions2 = '''


'''

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

import os
from dotenv import load_dotenv

from agno.models.deepseek import DeepSeek

# Load environment variables from cookbook/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Get the key from environment
key = os.getenv("DEEPSEEK_API_KEY")

agent_with_knowledge = Agent(
    name="Agent with Knowledge",
    model=DeepSeek(id="deepseek-chat", api_key=key),
    instructions=instructions,
    knowledge=knowledge,
    search_knowledge=True,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 将 Agno 文档的介绍加载到知识库
    # 我们只加载 1 个文件来保持示例简单。
    # knowledge.insert(name="Agno Introduction", url="https://docs.agno.com/introduction.md")
    knowledge.insert(name = '信息安规',path = r"C:\Users\ww193\Desktop\345-所属班组-信息类班组（外包）.xlsx")
    contents, count = knowledge.get_content()
    print(f"\n知识库中共有 {count} 个内容项:")
    for content in contents:
        print(f"  - {content.name} (ID: {content.id}, Status: {content.status})")
    agent_with_knowledge.print_response(
        "工作许可人的安全职责包括确认工作票上所填安全措施是否正确完备。",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
加载自己的知识：

1. 从 URL
   knowledge.insert(url="https://example.com/docs.pdf")

2. 从本地文件
   knowledge.insert(path="path/to/document.pdf")

3. 直接从文本
   knowledge.insert(text_content="你的内容在这里...")

混合搜索结合：
- 语义搜索：找到概念上相似的内容
- 关键词搜索：找到精确词语匹配
- 结果使用 Reciprocal Rank Fusion (RRF) 融合

Agent 在相关时自动搜索（智能搜索）。
"""
