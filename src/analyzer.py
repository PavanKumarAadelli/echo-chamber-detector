from bertopic import BERTopic
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN

def fit_topic_model(documents):
    # Use a specific model for embeddings
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # FIX: Configure HDBSCAN to work with small datasets
    hdbscan_model = HDBSCAN(min_cluster_size=2, metric='euclidean', prediction_data=True)
    
    topic_model = BERTopic(
        embedding_model=sentence_model, 
        hdbscan_model=hdbscan_model, 
        language="english", 
        verbose=False
    )
    
    topics, probs = topic_model.fit_transform(documents)
    return topic_model, topics

# 2. Stance Detection Functions (Using Zero-Shot Classification)
def load_stance_model():
    # This model is powerful and works on any topic
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return classifier

def get_stance_scores(texts, targets, classifier):
    labels = []
    candidate_labels = ["favor", "against"]
    
    print("Analyzing stances (Zero-Shot)...")
    for text, target in zip(texts, targets):
        # We ask the model: Does this text look like "favor" or "against" the topic?
        result = classifier(text, candidate_labels)
        
        # The result gives scores for each label
        favor_score = result['scores'][result['labels'].index('favor')]
        against_score = result['scores'][result['labels'].index('against')]
        
        # Simple logic: Convert to -1, 0, 1
        if favor_score > 0.7:
            score = 1
        elif against_score > 0.7:
            score = -1
        else:
            score = 0
            
        labels.append(score)
        
    return labels