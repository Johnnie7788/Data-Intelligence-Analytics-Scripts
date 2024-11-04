#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sqlalchemy
import logging

# Logging setup for tracking progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def load_performance_data(sql_connection_string):
    """
    Load data from SQL database containing marketing performance metrics.
    """
    try:
        logger.info("Connecting to SQL database...")
        engine = sqlalchemy.create_engine(sql_connection_string)
        query = """
        SELECT * FROM marketing_performance_data
        WHERE date >= '2023-01-01' AND channel IN ('Paid Search', 'Social Media', 'Display')
        """
        data = pd.read_sql(query, engine)
        logger.info(f"Loaded {data.shape[0]} records from SQL database.")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        data = pd.DataFrame()
    return data

def preprocess_data(data):
    """
    Preprocess data by handling missing values and converting date column to datetime.
    """
    logger.info("Preprocessing data...")
    data['date'] = pd.to_datetime(data['date'])
    data.fillna(method='ffill', inplace=True)
    logger.info("Data preprocessing completed.")
    return data

def performance_analysis(data):
    """
    Generate visualizations for performance across marketing channels.
    """
    logger.info("Starting performance analysis...")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='date', y='spend', hue='channel')
    plt.xlabel("Date")
    plt.ylabel("Spend")
    plt.title("Marketing Spend Over Time by Channel")
    plt.savefig('marketing_spend_over_time.png')
    plt.close()
    logger.info("Generated marketing spend visualization.")

    plt.figure(figsize=(10, 5))
    sns.barplot(data=data, x='channel', y='roi')
    plt.xlabel("Channel")
    plt.ylabel("ROI")
    plt.title("ROI by Marketing Channel")
    plt.savefig('roi_by_channel.png')
    plt.close()
    logger.info("Generated ROI by channel visualization.")

def budget_prediction(data):
    """
    Predict future budget requirements using an advanced regression model.
    """
    logger.info("Starting budget prediction modeling...")
    data['month'] = data['date'].dt.month
    X = data[['spend', 'roi', 'month']]
    y = data['conversions']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Use Gradient Boosting for better accuracy in predictions
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    logger.info(f"Budget prediction model completed with MSE: {mse:.2f} and R2: {r2:.2f}")
    
    return model, y_test, y_pred

def attribution_analysis(data):
    """
    Perform multi-touch attribution modeling to assign credit to each channel.
    """
    logger.info("Starting attribution analysis...")
    attribution = data.groupby('channel')['conversions'].sum() / data['conversions'].sum()
    attribution_df = attribution.reset_index()
    attribution_df.columns = ['channel', 'attribution']
    
    # Save attribution results to CSV for reporting
    attribution_df.to_csv('channel_attribution.csv', index=False)
    logger.info("Attribution analysis completed and saved as channel_attribution.csv.")
    return attribution_df

def incrementality_analysis(data):
    """
    Perform A/B testing to analyze the incrementality of marketing channels.
    """
    logger.info("Starting incrementality analysis...")
    group_a = data[data['campaign_type'] == 'A']
    group_b = data[data['campaign_type'] == 'B']
    
    t_stat, p_value = stats.ttest_ind(group_a['conversions'], group_b['conversions'])
    logger.info(f"Incrementality analysis completed with T-Statistic: {t_stat:.2f}, P-Value: {p_value:.4f}")
    
    return {'t_stat': t_stat, 'p_value': p_value}

def profitability_metrics(data):
    """
    Calculate key profitability metrics including CPA, LTV, and overall profitability.
    """
    logger.info("Calculating profitability metrics...")
    data['CPA'] = data['spend'] / data['conversions']
    avg_cpa = data['CPA'].mean()
    total_ltv = data['conversions'].sum() * 100  # Assume an average LTV of $100 for demonstration
    total_spend = data['spend'].sum()
    profitability = total_ltv - total_spend
    
    profitability_metrics = {
        'Average CPA': avg_cpa,
        'Total LTV': total_ltv,
        'Profitability': profitability
    }
    logger.info(f"Profitability metrics calculated: {profitability_metrics}")
    return profitability_metrics

def generate_dashboard(data):
    """
    Generate key metrics and visualizations for dashboard export.
    """
    logger.info("Generating Google Data Studio-compatible reports...")
    total_spend = data['spend'].sum()
    total_conversions = data['conversions'].sum()
    avg_roi = data['roi'].mean()
    
    metrics_summary = pd.DataFrame({
        'Metric': ['Total Spend', 'Total Conversions', 'Average ROI'],
        'Value': [total_spend, total_conversions, avg_roi]
    })
    metrics_summary.to_csv('metrics_summary.csv', index=False)
    logger.info("Generated summary metrics for dashboard export.")

def main():
    sql_connection_string = 'sqlite:///marketing_analytics.db'
    data = load_performance_data(sql_connection_string)
    data = preprocess_data(data)
    performance_analysis(data)
    model, y_test, y_pred = budget_prediction(data)
    attribution_df = attribution_analysis(data)
    incrementality_results = incrementality_analysis(data)
    profitability_metrics_results = profitability_metrics(data)
    
    print(f"Incrementality Test Results: T-Statistic = {incrementality_results['t_stat']}, P-Value = {incrementality_results['p_value']}")
    print(f"Profitability Metrics: {profitability_metrics_results}")
    
    generate_dashboard(data)
    logger.info("Advanced Marketing Analytics and Budget Prediction Suite completed successfully.")

if __name__ == "__main__":
    main()

