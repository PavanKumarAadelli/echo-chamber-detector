# A simple list of articles for recommendations (no database needed)
articles = [
    {"text": "Why renewable energy is unreliable and nuclear is the future.", "topic": "environment", "stance": "against"},
    {"text": "Cryptocurrency is a revolutionary technology freeing people from banks.", "topic": "crypto", "stance": "favor"},
    {"text": "Why traditional gasoline cars are still superior to electric vehicles.", "topic": "cars", "stance": "against"},
    {"text": "The government should not interfere with free market economics.", "topic": "politics", "stance": "against"},
    {"text": "Climate change is a serious threat requiring global cooperation.", "topic": "environment", "stance": "favor"},
    {"text": "AI will create more jobs than it destroys, experts say.", "topic": "technology", "stance": "favor"},
]

def setup_database():
    # Nothing to setup anymore since we use a simple list
    pass

def get_opposite_view(topic_name, user_stance):
    # Simple search: Find an article that matches the opposite stance
    target_stance = "against" if user_stance > 0 else "favor"
    
    # Search through our list
    for article in articles:
        # Check if the stance matches and if the topic is somewhat similar
        if article["stance"] == target_stance:
            return article["text"]
            
    return None