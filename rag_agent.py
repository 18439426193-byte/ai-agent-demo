# rag_agent.py - 交互式RAG Agent（最终成品）
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# 初始化 Chroma
client_chroma = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
collection = client_chroma.get_collection(
    name="knowledge_base",
    embedding_function=embedding_fn
)

# 初始化大模型
client_llm = OpenAI(
    api_key="your-api-key-here",  # ⚠️ 替换成你的新API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def rag_query(user_question: str):
    # 1. 检索相关文档
    results = collection.query(
        query_texts=[user_question],
        n_results=3
    )
    retrieved_docs = results["documents"][0]
    context = "\n\n".join(retrieved_docs)
    
    # 2. 构建 Prompt
    prompt = f"""请基于以下参考内容回答用户的问题。如果参考内容中没有相关信息，请直接说"知识库中没有相关内容"。

参考内容：
{context}

用户问题：{user_question}

回答："""
    
    # 3. 调用大模型生成回答
    response = client_llm.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# 交互式对话
print("🤖 RAG Agent 已启动（输入 exit 退出）\n")
print("📚 知识库包含：子不语公司、AI Agent、Function Calling、RAG、Chroma、杭州就业、Python\n")

while True:
    user_input = input("你：")
    if user_input == "exit":
        print("再见！")
        break
    
    answer = rag_query(user_input)
    print("AI：", answer)
    print()