import streamlit as st
import pandas as pd
import sys
import os

# --- SETUP PATH FOR IMPORTS ---
# This tells Python to look inside the 'src' folder for files
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# --- IMPORTS ---
# Now we can import files from the src folder
from fetcher import fetch_user_data
from analyzer import fit_topic_model, load_stance_model, get_stance_scores
from utils import calculate_echo_score
from recommender import setup_database, get_opposite_view
import plotly.express as px
print("--- Imports Successful ---")
except Exception as e:
    st.error(f"Import Error: {e}")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Echo Chamber Detector", layout="wide")
st.title("🌀 Echo Chamber Detector")
st.write("Analyze a user's stance polarization using NLP.")

# --- Sidebar ---
username = st.sidebar.text_input("Enter Username", value="demo_user")
limit = st.sidebar.slider("Number of Comments", 5, 20, 8) 
run_analysis = st.sidebar.button("Analyze User")

# --- Main Logic ---
if run_analysis:
    print("--- Button Clicked ---")
    # 1. Fetch Data
    with st.spinner("Loading data..."):
        data = fetch_user_data(username, limit)
    
    if not data:
        st.error("No data found. Check sample_data.json.")
    else:
        st.success(f"Loaded {len(data)} comments.")
        df = pd.DataFrame(data)

               # 2. Topic Modeling
        with st.spinner("Discovering topics (AI thinking)..."):
            docs = df['text'].tolist()
            topic_model, topics = fit_topic_model(docs)
            
            # --- Generate Clean Topic Names ---
            topic_names = []
            for t in topics:
                if t == -1:
                    topic_names.append("General")
                else:
                    # Get the top words for the topic
                    topic_words = topic_model.get_topic(t)
                    if topic_words:
                        # Take top 3 words and join them
                        name = "_".join([word for word, _ in topic_words[:3]])
                        topic_names.append(name)
                    else:
                        topic_names.append("Topic_" + str(t))
            
            # IMPORTANT: Attach the names to the DataFrame
            df['topic'] = topic_names

        # 3. Stance Detection
        with st.spinner("Detecting stances (Using Zero-Shot AI)..."):
            classifier = load_stance_model()
            # We pass the text and the newly created topic names
            stance_scores = get_stance_scores(docs, topic_names, classifier)
            df['stance_score'] = stance_scores

        # 4. Calculate Metrics
        echo_scores, rigidity = calculate_echo_score(df)
        
        # Display
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Rigidity Score", f"{rigidity:.2f}")
        with col2:
            st.metric("Unique Topics Found", len(set(topics)))

        # Chart
        chart_data = pd.DataFrame({
            "Topic": list(echo_scores.keys()),
            "Polarization": list(echo_scores.values())
        })
        fig = px.bar(chart_data, x='Topic', y='Polarization', color='Polarization', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Raw Data")
        st.dataframe(df[['text', 'topic', 'stance_score']])
                # --- Step 5: Recommendation System ---
        st.subheader("💡 Break the Bubble")
        
        # Setup the small database of articles
        setup_database()
        
        # Find the topic the user is most polarized on
        most_polarized_topic = max(echo_scores, key=echo_scores.get)
        stance_on_topic = df[df['topic'] == most_polarized_topic]['stance_score'].mean()
        
        st.write(f"You seem to have a strong opinion on **{most_polarized_topic}**.")
        
        # Find an opposing article
        recommendation = get_opposite_view(most_polarized_topic, stance_on_topic)
        
        if recommendation:
            st.info(f"**Read this opposing view:**\n\n{recommendation}")
        else:
            st.write("We couldn't find an opposing article for your top topic, but keep exploring!")