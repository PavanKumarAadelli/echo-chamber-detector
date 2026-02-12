# LIGHTWEIGHT SIMULATION MODE
# Uses keyword matching instead of heavy AI models for guaranteed deployment.

def fit_topic_model(documents):
    topics = []
    for doc in documents:
        # Create a simple topic name from the first 3 words
        words = doc.split()[:3]
        topics.append("_".join(words))
    return None, topics

def load_stance_model():
    # No model to load in simulation mode
    return None

def get_stance_scores(texts, targets, model):
    scores = []
    
    # Simple keyword-based stance detection
    positive_words = ['love', 'great', 'good', 'support', 'future', 'best', 'amazing', 'right', 'fantastic']
    negative_words = ['hate', 'bad', 'terrible', 'ruin', 'scam', 'wrong', 'worst', 'destroy', 'waste']
    
    for text in texts:
        text_lower = text.lower()
        score = 0
        
        # Check for keywords
        if any(word in text_lower for word in positive_words):
            score = 1
        elif any(word in text_lower for word in negative_words):
            score = -1
        
        scores.append(score)
        
    return scores