# rag_build_index.py - 构建向量索引
import chromadb
from chromadb.utils import embedding_functions
from rag_data import knowledge_docs

# 初始化 Chroma 客户端（数据会持久化保存到 ./chroma_db 文件夹）
client = chromadb.PersistentClient(path="./chroma_db")

# 使用 sentence-transformers 作为 Embedding 模型（免费、本地运行）
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 创建或获取 Collection
collection = client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=embedding_fn
)

# 准备数据
ids = []
documents = []
metadatas = []

for doc in knowledge_docs:
    ids.append(doc["id"])
    documents.append(doc["content"])
    metadatas.append({"title": doc["title"]})

# 插入数据到向量库
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print(f"✅ 成功插入 {len(ids)} 条知识到向量数据库")
print(f"📁 数据保存在 ./chroma_db 文件夹中")