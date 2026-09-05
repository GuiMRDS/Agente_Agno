from agno.vectordb.chroma import ChromaDb

from config.settings import CHROMA_DIR

def get_vector_db():

    return ChromaDb(
        collection="knowledge",
        path=str(CHROMA_DIR)
    )