# --- LAZY IMPORTS ---
# We import heavy libraries inside the functions so the app starts faster

def fit_topic_model(documents):
    # Import heavy libraries only when needed
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    from hdbscan import HDBSCAN
    
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    hdbscan_model = HDBSCAN(min_cluster_size=2, metric='euclidean', prediction_data=True)
    
    topic_model = BERTopic(
        embedding_model=sentence_model, 
        hdbscan_model=hdbscan_model, 
        language="english", 
        verbose=False
    )
    
    topics, probs = topic_model.fit_transform(documents)
    return topic_model, topics

def load_stance_model():
    from transformers import pipeline
    # Use a smaller, faster model for the cloud
    classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-mnli")
    return classifier

def get_stance_scores(texts, targets, classifier):
    labels = []
    candidate_labels = ["favor", "against"]
    
    for text, target in zip(texts, targets):
        result = classifier(text, candidate_labels)
        favor_score = result['scores'][result['labels'].index('favor')]
        against_score = result['scores'][result['labels'].index('against')]
        
        if favor_score > 0.7:
            score = 1
        elif against_score > 0.7:
            score = -1
        else:
            score = 0
            
        labels.append(score)
    return labels