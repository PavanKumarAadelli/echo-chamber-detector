import pandas as pd
import numpy as np

def calculate_echo_score(df):
    """
    df: Pandas DataFrame with 'topic' and 'stance_score' columns.
    Returns a dictionary of scores per topic and an overall rigidity score.
    """
    # Group by topic and calculate mean stance
    topic_stats = df.groupby('topic')['stance_score'].mean()
    
    # Logic: 
    # If mean is near 1 (Favor) or -1 (Against), they are polarized.
    # If mean is near 0, they have mixed views.
    
    echo_scores = topic_stats.abs().to_dict()
    
    # Calculate overall user "Rigidity Score" (Average of absolute stances)
    if len(echo_scores) > 0:
        overall_rigidity = np.mean(list(echo_scores.values()))
    else:
        overall_rigidity = 0.0
        
    return echo_scores, overall_rigidity