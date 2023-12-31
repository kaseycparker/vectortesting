# prereqs: use Atlas account to create a cluster, database, collection, trigger, index and load sample data. Follow tutorial: https://www.mongodb.com/library/vector-search/semantic-search-mongodb-using-atlas-vector-search?lb-mode=overlay

const axios = require('axios');
const MongoClient = require('mongodb').MongoClient;

async function getEmbedding(query) {
    // Define the OpenAI API url and key.
    const url = 'https://api.openai.com/v1/embeddings';
    const openai_key = process.env.OPENAI_APIKEY; // OS env with your OpenAI API key.
    
    // Call OpenAI API to get the embeddings.
    let response = await axios.post(url, {
        input: query,
        model: "text-embedding-ada-002"
    }, {
        headers: {
            'Authorization': `Bearer ${openai_key}`,
            'Content-Type': 'application/json'
        }
    });
    
    if(response.status === 200) {
        return response.data.data[0].embedding;
    } else {
        throw new Error(`Failed to get embedding. Status code: ${response.status}`);
    }
}

async function findSimilarDocuments(embedding) {
    const url = process.env.MONGO_URL; // OS env with your MongoDB url.
    const client = new MongoClient(url);
    
    try {
        await client.connect();
        
        const db = client.db(process.env.DBNAME); // Replace with your database name.
        const collection = db.collection(process.env.COLLECTION_NAME); // Replace with your collection name.
        
        // Query for similar documents.
        const documents = await collection.aggregate([
            {
            "$search": {
            "index": "moviesPlotIndex",
            "knnBeta": {
            "vector": embedding,
            "path": "plot_embedding",
            "k": 5
            }
            }
            }
            ]).toArray();
        
        return documents;
    } finally {
        await client.close();
    }
}

async function main() {
    const query = 'What does Paulines uncle leave her?'; // Replace with your query.
    
    try {
        const embedding = await getEmbedding(query);
        const documents = await findSimilarDocuments(embedding);
        
        console.log(documents);
    } catch(err) {
        console.error(err);
    }
}

main();
