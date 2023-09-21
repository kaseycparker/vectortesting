import vecs

# connection requires client to communicate with Postgres, I used Neon https://neon.tech/
DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"

# create vector store client
vx = vecs.create_client(DB_CONNECTION)

# create collection
docs = vx.create_collection(name="docs", dimension=3)

# get an existing collection
docs = vx.get_collection(name="docs")

# add records to the collection
docs.upsert(
    records=[
        (
         "vec0",           # the vector's identifier
         [0.1, 0.2, 0.3],  # the vector. list or np.array
         {"year": 1973}    # associated  metadata
        ),
        (
         "vec1",
         [0.7, 0.8, 0.9],
         {"year": 2012}
        )
    ]
)

# index the collection to be queried by cosine distance
docs.create_index(measure=vecs.IndexMeasure.cosine_distance)

# basic query
docs.query(
    data=[0.4,0.5,0.6],  # required
    limit=5,                     # number of records to return
    filters={},                  # metadata filters
    measure="cosine_distance",   # distance measure to use
    include_value=False,         # should distance measure values be returned?
    include_metadata=False,      # should record metadata be returned?


# metatdata filtering
docs.query(
    data=[0.4,0.5,0.6],
    filters={"year": {"$eq": 2012}}, # metadata filters
)

