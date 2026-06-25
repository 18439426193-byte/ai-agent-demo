# rag_search.py - 测试语义检索
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
collection = client.get_collection(
    name="knowledge_base",
    embedding_function=embedding_fn
)

# 测试检索
queries = [
    "子不语是做什么的？",
    "什么是RAG技术？",
    "杭州的工资水平怎么样？"
]

for query in queries:
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    print(f"\n🔍 问题：{query}")
    print("-" * 40)
    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"结果 {i+1}：{metadata['title']}")
        print(f"内容：{doc[:80]}...")