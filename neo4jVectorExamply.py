# prepreqs:
# setup a Neo4J Aura DB: https://login.neo4j.com/
# pip install langchain openai wikipedia tiktoken neo4j

# Example Data Set

from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import CharacterTextSplitter

# Read the wikipedia article
raw_documents = WikipediaLoader(query="The Witcher").load()
# Define chunking strategy
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=20
)
# Chunk the document
documents = text_splitter.split_documents(raw_documents)
# Remove the summary
for d in documents:
    del d.metadata["summary"]

# DB connection, replace with url, username and password for Aura DB
url = "AuraDB URL" 
username = "username"
password = "password"

# code to customize the node label, text and embedding properties
neo4j_db = Neo4jVector.from_documents(
    documents,
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    database="neo4j",  # neo4j by default
    index_name="wikipedia",  # vector by default
    node_label="WikipediaArticle",  # Chunk by default
    text_node_property="info",  # text by default
    embedding_node_property="vector",  # embedding by default
    create_id_index=True,  # True by default
)

neo4j_db.query("SHOW CONSTRAINTS")
#[{'id': 4,
#  'name': 'constraint_e5da4d45',
#  'type': 'UNIQUENESS',
#  'entityType': 'NODE',
#  'labelsOrTypes': ['WikipediaArticle'],
#  'properties': ['id'],
#  'ownedIndex': 'constraint_e5da4d45',
#  'propertyType': None}]

# show the vector index: 
neo4j_db.query(
    """SHOW INDEXES
       YIELD name, type, labelsOrTypes, properties, options
       WHERE type = 'VECTOR'
    """
)
#[{'name': 'wikipedia',
#  'type': 'VECTOR',
#  'labelsOrTypes': ['WikipediaArticle'],
#  'properties': ['vector'],
#  'options': {'indexProvider': 'vector-1.0',
#   'indexConfig': {'vector.dimensions': 1536,
#    'vector.similarity_function': 'cosine'}}}]


# load additional documents
eo4j_db.add_documents(
    [
        Document(
            page_content="LangChain is the coolest library since the Library of Alexandria",
            metadata={"author": "Tomaz", "confidence": 1.0}
        )
    ],
    ids=["langchain"],
)

print(existing_index.node_label)
print(existing_index.embedding_node_property)

read_query = (
    "CALL db.index.vector.queryNodes($index, $k, $embedding) "
    "YIELD node, score "
) + retrieval_query


existing_index.query(
    """MATCH (w:WikipediaArticle {id:'langchain'})
       MERGE (w)<-[:EDITED_BY]-(:Person {name:"Galileo"})
    """
)


retrieval_query = """
OPTIONAL MATCH (node)<-[:EDITED_BY]-(p)
WITH node, score, collect(p) AS editors
RETURN node.info AS text,
       score,
       node {.*, vector: Null, info: Null, editors: editors} AS metadata
"""

existing_index_return = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    database="neo4j",
    index_name="wikipedia",
    text_node_property="info",
    retrieval_query=retrieval_query,
)

existing_index_return.similarity_search("What do you know about LangChain?", k=1)

