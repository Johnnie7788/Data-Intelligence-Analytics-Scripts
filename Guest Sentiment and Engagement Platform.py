#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from transformers import pipeline
import pandas as pd
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SentimentAnalysis:
    """Class for sentiment analysis using a transformer-based model."""

    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize the sentiment analysis pipeline."""
        try:
            self.model = pipeline("sentiment-analysis", model=model_name)
            logging.info(f"Model '{model_name}' loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model '{model_name}': {e}")
            raise

    @staticmethod
    def validate_feedback(feedbacks):
        """Validate feedback inputs."""
        if not isinstance(feedbacks, list):
            raise ValueError("Feedbacks must be a list of strings.")
        if not all(isinstance(f, str) and f.strip() for f in feedbacks):
            raise ValueError("All feedbacks must be non-empty strings.")
        return feedbacks

    def analyze_feedback(self, feedbacks):
        """Analyze guest feedback for sentiment."""
        feedbacks = self.validate_feedback(feedbacks)
        logging.info("Analyzing feedback for sentiment")
        results = self.model(feedbacks)
        return pd.DataFrame(results)

    def generate_report(self, feedbacks):
        """Generate a sentiment analysis report."""
        sentiment_df = self.analyze_feedback(feedbacks)
        summary = sentiment_df['label'].value_counts(normalize=True) * 100
        logging.info(f"Sentiment Summary:\n{summary}")
        return sentiment_df, summary


# Main Execution
feedbacks = [
    "The room was clean and spacious, loved it!",
    "Terrible service, the staff was rude and unhelpful.",
    "Great location, but the noise was unbearable.",
    "Loved the amenities and the friendly staff."
]

analyzer = SentimentAnalysis()
df, summary = analyzer.generate_report(feedbacks)
print("Sentiment Analysis Results:")
print(df)
print("\nSentiment Summary (%):")
print(summary)

