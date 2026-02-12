# 🌀 Echo Chamber Detector

An advanced NLP application that analyzes a user's social media activity to detect polarization and recommend opposing viewpoints to "break the bubble."

![Streamlit App](https://img.shields.io/badge/Streamlit-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

## 🚀 Live Demo
**[Click here to view the live application](https://echo-chamber-detector-obj2hgycrdg46njglkj3xb.streamlit.app/)** 

## 📖 Project Overview
In the age of social media, users often find themselves in "echo chambers" where their existing beliefs are reinforced. This tool uses Natural Language Processing (NLP) to:

1.  **Analyze Stance:** Determine if a user is "In Favor," "Against," or "Neutral" on specific topics.
2.  **Quantify Bias:** Calculate a "Rigidity Score" (0.0 to 1.0) to measure polarization.
3.  **Break the Bubble:** Recommend articles with opposing viewpoints.

## 🛠️ Tech Stack
*   **Language:** Python
*   **Data Ingestion:** PRAW (Reddit API)
*   **NLP Models:** Topic Modeling & Stance Detection
*   **Visualization:** Plotly, Streamlit
*   **Deployment:** Streamlit Community Cloud

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone https://github.com/PavanKumarAadelli/echo-chamber-detector.git
    cd echo-chamber-detector
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the app**
    ```bash
    streamlit run app.py
    ```

## 📊 Methodology

1.  **Data Acquisition:** Fetches comments via Reddit API or uses sample data.
2.  **Topic Discovery:** Identifies key themes (e.g., Politics, Technology).
3.  **Stance Analysis:** Analyzes sentiment relative to the topic.
4.  **Metric Calculation:** Calculates a Rigidity Score to measure bias.

## ✍️ Author
**Pavan Kumar Aadelli**