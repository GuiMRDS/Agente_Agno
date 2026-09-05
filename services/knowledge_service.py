from agno.knowledge import Knowledge
from agno.document.reader.pdf_reader import PDFReader

from services.vector_store_service import (
    VectorStoreService
)

class KnowledgeService:

    @staticmethod
    def create():

        return Knowledge(
            vector_db=VectorStoreService.get_db()
        )

    @staticmethod
    def load_pdf(path):

        knowledge = KnowledgeService.create()

        knowledge.insert(
            path=path,
            reader=PDFReader(),
            skip_if_exists=True
        )

        return knowledge