#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Cloud Data Insights Suite (CDIS)
# Description: A comprehensive cloud-based data analytics suite for automated multi-cloud data ingestion, ETL,
#              advanced predictive analytics, interactive real-time dashboards, and automated reporting.
#              Designed to meet the demands of modern cloud data analytics.

# Import necessary libraries
import boto3  # AWS S3 integration
from google.cloud import storage  # GCP Storage integration
from azure.storage.blob import BlobServiceClient  # Azure Blob Storage integration
import pandas as pd  # Data manipulation
import matplotlib.pyplot as plt  # Data visualization
import seaborn as sns  # Advanced visualization
from sklearn.linear_model import LinearRegression  # Predictive analysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing  # Advanced forecasting
from sqlalchemy import create_engine  # Cloud data warehousing
from reportlab.pdfgen import canvas  # Automated reporting
import streamlit as st  # Interactive dashboard
import logging  # For error handling and logging
from datetime import datetime

# Configure logging for error tracking and debugging
logging.basicConfig(filename='cloud_data_insights.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Configuration Section: Set up cloud and database configurations
AWS_BUCKET_NAME = 'your-bucket-name'
AWS_ACCESS_KEY = 'your-access-key'
AWS_SECRET_KEY = 'your-secret-key'
GCP_BUCKET_NAME = 'your-gcp-bucket'
AZURE_CONNECTION_STRING = 'your-azure-connection-string'
REDSHIFT_CONNECTION_STRING = 'your_redshift_connection_string'

# Step 1: Multi-Cloud Data Ingestion
def ingest_data_from_cloud(provider, file_key):
    """Connects to cloud storage (AWS, Azure, or GCP) and retrieves data."""
    try:
        if provider == 'aws':
            s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=file_key)
            data = pd.read_csv(obj['Body'])
        elif provider == 'gcp':
            client = storage.Client()
            bucket = client.bucket(GCP_BUCKET_NAME)
            blob = bucket.blob(file_key)
            data = pd.read_csv(blob.download_as_text())
        elif provider == 'azure':
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container='your-container-name', blob=file_key)
            data = pd.read_csv(blob_client.download_blob().content_as_text())
        else:
            raise ValueError("Unsupported cloud provider. Choose 'aws', 'gcp', or 'azure'.")
        logging.info(f"Data successfully ingested from {provider.upper()} for file {file_key}.")
        return data
    except Exception as e:
        logging.error(f"Error ingesting data from {provider.upper()}: {e}")
        raise

# Step 2: Data Cleaning and Transformation
def clean_transform_data(df):
    """Performs data cleaning and transformation on the ingested data."""
    try:
        df.dropna(inplace=True)  # Drop missing values
        df['date'] = pd.to_datetime(df['date'])  # Standardize date format
        df['category'] = df['category'].str.upper()  # Standardize categorical fields
        logging.info("Data cleaned and transformed successfully.")
        return df
    except Exception as e:
        logging.error(f"Error in data cleaning and transformation: {e}")
        raise

# Step 3: Load Data to Cloud Data Warehouse (AWS Redshift)
def load_data_to_redshift(df, table_name):
    """Loads the transformed data into a Redshift data warehouse."""
    try:
        engine = create_engine(REDSHIFT_CONNECTION_STRING)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data successfully loaded to Redshift table '{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data to Redshift: {e}")
        raise

# Step 4: Descriptive Analytics
def descriptive_analytics(df):
    """Generates descriptive statistics and visualizations for the dataset."""
    try:
        print("Descriptive Analytics Summary:")
        print(df.describe())  # Summary statistics
        plt.figure(figsize=(10, 6))
        sns.histplot(df['sales'], kde=True)
        plt.title("Sales Distribution")
        plt.savefig("sales_distribution.png")
        plt.show()
        logging.info("Descriptive analytics completed successfully.")
    except Exception as e:
        logging.error(f"Error in descriptive analytics: {e}")
        raise

# Step 5: Advanced Predictive Analytics - Time Series Forecasting
def predictive_analytics(df, target_column, feature_columns, forecast_period=12):
    """Builds a time series forecasting model using Exponential Smoothing."""
    try:
        model = ExponentialSmoothing(df[target_column], trend="add", seasonal="add", seasonal_periods=12)
        fitted_model = model.fit()
        forecast = fitted_model.forecast(forecast_period)
        logging.info("Predictive analytics model successfully fitted and forecast generated.")
        return fitted_model, forecast
    except Exception as e:
        logging.error(f"Error in predictive analytics: {e}")
        raise

# Step 6: Real-Time Interactive Dashboard with Streamlit
def interactive_dashboard(df, forecast):
    """Sets up an interactive dashboard using Streamlit to explore data in real time."""
    try:
        st.title("Cloud Data Insights Suite - Interactive Dashboard")
        st.write("## Sales Overview")
        st.line_chart(df.set_index('date')['sales'])
        
        st.write("## Forecasted Sales")
        st.line_chart(forecast)

        st.write("## Data Summary")
        st.write(df.describe())

        st.write("## Sales Distribution")
        st.bar_chart(df['sales'])

        st.write("## Filtered Data")
        category = st.selectbox("Choose category:", df['category'].unique())
        filtered_data = df[df['category'] == category]
        st.write(filtered_data)

        logging.info("Interactive dashboard loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading interactive dashboard: {e}")
        raise

# Step 7: Automated Reporting with PDF and Cloud Report Storage
def generate_pdf_report(summary_text):
    """Generates a PDF report summarizing key analytics results and uploads it to cloud storage."""
    try:
        pdf = canvas.Canvas("report.pdf")
        pdf.drawString(100, 750, "Cloud Data Insights Suite - Analytics Report")
        pdf.drawString(100, 730, summary_text)
        pdf.drawImage("sales_distribution.png", 100, 600, width=400, height=200)
        pdf.save()
        logging.info("PDF report generated successfully.")

        # Optional: Upload the report to AWS S3 for sharing
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        with open("report.pdf", "rb") as f:
            s3_client.upload_fileobj(f, AWS_BUCKET_NAME, "reports/report.pdf")
        logging.info("PDF report uploaded to AWS S3 successfully.")
    except Exception as e:
        logging.error(f"Error generating PDF report: {e}")
        raise

# Step 8: Main Function to Orchestrate Workflow
def main():
    # Configuration - File and Table names
    provider = 'aws'  # Choose from 'aws', 'gcp', or 'azure'
    file_key = 'your-data-file.csv'
    table_name = 'cloud_data_analytics'

    try:
        # Data Ingestion
        data = ingest_data_from_cloud(provider, file_key)

        # Data Cleaning and Transformation
        clean_data = clean_transform_data(data)

        # Load Data to Redshift
        load_data_to_redshift(clean_data, table_name)

        # Descriptive Analytics
        descriptive_analytics(clean_data)

        # Predictive Analytics - Forecasting sales with Exponential Smoothing
        target_column = 'sales'
        model, forecast = predictive_analytics(clean_data, target_column, feature_columns=['ad_spend', 'num_customers'], forecast_period=12)

        # Interactive Dashboard - Run with Streamlit
        interactive_dashboard(clean_data, forecast)

        # Generate PDF Report
        summary_text = f"Cloud Data Analytics - Advanced Forecasting Model Summary. Forecast generated for next 12 periods."
        generate_pdf_report(summary_text)

        print("Ultimate Cloud Data Insights Suite (CDIS) workflow completed successfully.")
        logging.info("CDIS workflow executed successfully.")
    except Exception as e:
        logging.error(f"Error in CDIS main workflow: {e}")

# Run the script
if __name__ == "__main__":
    main()

