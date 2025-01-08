import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    SimpleKeywordTableIndex
)
from llama_index.core import SummaryIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.tools import QueryEngineTool, RetrieverTool
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
data_dir = './data_dir'


def rag (api_key: str, query: str):
    """Useful for Responding to User's query about a specific coin or token"""
    try:
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2, api_key=api_key)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=openai_api_key)

        document_dir = data_dir
        documents = SimpleDirectoryReader(document_dir).load_data()

        Settings.chunk_size = 1024
        nodes = Settings.node_parser.get_nodes_from_documents(documents)

        storage_context = StorageContext.from_defaults()
        storage_context.docstore.add_documents(nodes)

        summary_index = SummaryIndex(nodes, storage_context=storage_context)
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)

        list_query_engine = summary_index.as_query_engine(
        response_mode = "compact",
        use_async = True
    )
        vector_query_engine = vector_index.as_query_engine()
        keyword_query_engine = keyword_index.as_query_engine()

        list_tool = QueryEngineTool.from_defaults(
        query_engine = list_query_engine,
        description=(
            "useful for summarization and providing explanation to context"
        )
    )

        vector_tool = QueryEngineTool.from_defaults(
            query_engine= vector_query_engine,
            description= (
                "useful for retrieving specific context from multiple documents as provided"
            )
        )

        keyword_tool = QueryEngineTool.from_defaults(
            query_engine = keyword_query_engine,
            description = (
                "useful for retrieving specific context from the provided document based on (specific entities within query)"
            )
        )

        query_engine = RouterQueryEngine(
        selector = LLMSingleSelector.from_defaults(),
        query_engine_tools = [
            list_tool,
            vector_tool,
            keyword_tool
        ]

    )   
        
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        print(str(e))



if __name__ == "__main__":
    
    query = input("Enter a Question based on the tokens (coins): ")

    print(rag(str(openai_api_key), query))