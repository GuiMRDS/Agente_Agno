from database.chroma import get_vector_db

class VectorStoreService:

    @staticmethod
    def get_db():
        return get_vector_db()