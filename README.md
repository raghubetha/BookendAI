# **Bookend AI: A Personalized Book Recommendation Dashboard**

A full-stack data science application that leverages over one million Goodreads reviews to provide deep, data-driven insights and personalized book recommendations.

[Live Demo Link](https://bookend-ai-app.onrender.com)

*This project was developed as a personal portfolio piece to showcase skills in end-to-end data science, from data processing and advanced machine learning to building and deploying a user-facing interactive web application.*

## **Problem Statement**

In a world with millions of books, the process of discovering a new book that truly matches one's taste can be overwhelming. Standard recommendations often rely on broad genres, failing to capture the nuanced preferences of individual readers. Bookend AI was built to solve this problem by analyzing not just what books people rate highly, but the rich, qualitative data within their written reviews to provide a more intelligent and personalized discovery experience.

## **Features**

Bookend AI is a multi-page dashboard with three main interactive views:

* **Explorer Page: **Get a high-level overview of the entire book dataset. This page includes dynamically updating KPIs, sortable lists of the "Most Reviewed," "Most Popular," and "Hidden Gem" books, and interactive visualizations for genre and publication trends.
* **Book Deep Dive Page: ** A detailed report on any book in the dataset. This view provides metadata, rating distributions, a word cloud of common review topics, and AI-generated abstractive summaries that provide a "Reader's Consensus."
* **Your Profile Page: ** A personalized dashboard that generates upon entering a user_id. This view includes custom analytics on a user's reading habits (average rating, favorite genre), a virtual bookshelf of their reading history, and two types of recommendations from the machine learning models.

## **Technical Stack**

### **Data Science & Machine Learning**

* **Data Processing:** Pandas for cleaning, feature engineering (e.g., calculating reading time), and creating weighted popularity scores.
* **Recommendation Engines:**
  * **Content-Based Filtering: Scikit-learn** using **TF-IDF** vectorization and **Cosine Similarity**.
  * **Collaborative Filtering: scikit-surprise** library using **Singular Value Decomposition (SVD)** with hyperparameter tuning.
* **Natural Language Processing (NLP):**
  * **Sentiment Analysis: VADER** for scoring review text.
  * **Text Preprocessing: NLTK** for sentence tokenization.
  * **Abstractive Summarization: Hugging Face Transformers** for generating nuanced summaries of reviews.


### **Backend & Dashboard**

* **Web Framework: Dash**
* **UI Components: Dash Bootstrap Components**
* **Visulizations: Plotly Express**
* **Web Server: Gunicorn**

### **Deployment and Data Storage**

* **Version Control: Git & GitHub**
* **Data Hosting: Google Cloud Storage (GCS)** for hosting the large dataset.
* **Cloud Platform: Render** for continuous deployment and hosting.

## **Setup and Installation**

To run this project locally, please follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/raghubetha/BookendAI.git
   cd BookendAI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
     pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
     python app.py
   ```
   The app will be available at `http://127.0.0.1:8050`
  
