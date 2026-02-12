import chromadb
from sentence_transformers import SentenceTransformer

# Setup a simple local vector database
client = chromadb.Client()
collection = client.get_or_create_collection(name="news_articles")

# Dummy data: Articles with specific stances
opposing_articles = [
    {"text": "Why renewable energy is unreliable and nuclear is the future.", "topic": "environment", "stance": "against"},
    {"text": "Cryptocurrency is a revolutionary technology freeing people from banks.", "topic": "crypto", "stance": "favor"},
    {"text": "Why traditional gasoline cars are still superior to electric vehicles.", "topic": "cars", "stance": "against"},
    {"text": "The government should not interfere with free market economics.", "topic": "politics", "stance": "against"},
    {"text": "Climate change is a serious threat requiring global cooperation.", "topic": "environment", "stance": "favor"},
    {"text": "AI will create more jobs than it destroys, experts say.", "topic": "technology", "stance": "favor"},
]

def setup_database():
    # Clear old data
    try:
        client.delete_collection("news_articles")
    except:
        pass
    
    global collection
    collection = client.get_or_create_collection(name="news_articles")
    
    # Add our articles to the database
    for i, article in enumerate(opposing_articles):
        collection.add(
            documents=[article["text"]],
            metadatas=[{"topic": article["topic"], "stance": article["stance"]}],
            ids=[f"article_{i}"]
        )

def get_opposite_view(topic_name, user_stance):
    target_stance = "against" if user_stance > 0 else "favor"
    
    results = collection.query(
        query_texts=[topic_name],
        n_results=1,
        where={"stance": target_stance} 
    )
    
    if results['documents']:
        return results['documents'][0][0]
    return None