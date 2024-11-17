#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import logging
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error
import joblib
import dash
from dash import dcc, html
import plotly.express as px

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HospitalityAnalytics:
    """Class for analyzing and forecasting hospitality data."""

    def __init__(self, file_path):
        self.data = self.load_data(file_path)
        self.model = None

    @staticmethod
    def load_data(file_path):
        """Load data from a CSV file with error handling."""
        try:
            logging.info(f"Loading data from {file_path}")
            return pd.read_csv(file_path)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            raise

    def preprocess_data(self):
        """Preprocess the dataset."""
        logging.info("Preprocessing data")
        if not {'BookingDate', 'CheckInDate', 'CheckOutDate', 'Revenue'}.issubset(self.data.columns):
            raise ValueError("Required columns are missing from the dataset.")
        self.data['BookingDate'] = pd.to_datetime(self.data['BookingDate'])
        self.data['CheckInDate'] = pd.to_datetime(self.data['CheckInDate'])
        self.data['StayDuration'] = (self.data['CheckOutDate'] - self.data['CheckInDate']).dt.days
        self.data['Season'] = self.data['CheckInDate'].dt.month % 12 // 3 + 1
        self.data['WeekendStay'] = self.data['CheckInDate'].dt.weekday >= 5
        self.data = pd.get_dummies(self.data, columns=['RoomType', 'GuestType'], drop_first=True)
        self.data.dropna(inplace=True)

    def train_model(self):
        """Train a Gradient Boosting Regressor with hyperparameter tuning."""
        logging.info("Training Gradient Boosting model")
        features = ['Season', 'StayDuration', 'WeekendStay']
        if not set(features).issubset(self.data.columns):
            raise ValueError(f"Missing features in dataset: {set(features) - set(self.data.columns)}")

        X = self.data[features]
        y = self.data['Revenue']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = GradientBoostingRegressor(random_state=42)
        param_grid = {'n_estimators': [100, 200], 'learning_rate': [0.05, 0.1], 'max_depth': [3, 5]}
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_
        joblib.dump(self.model, 'revenue_forecasting_model.pkl')

        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logging.info(f"Model Mean Squared Error: {mse}")
        return mse

    def visualize_trends(self):
        """Create interactive visualizations for booking trends."""
        logging.info("Visualizing booking trends")
        trend_data = self.data.groupby(self.data['BookingDate'].dt.to_period('M')).size()
        trend_df = trend_data.reset_index(name='Bookings')
        trend_df['BookingDate'] = trend_df['BookingDate'].astype(str)

        app = dash.Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(
                figure=px.line(trend_df, x='BookingDate', y='Bookings', title='Monthly Booking Trends')
            )
        ])

        if __name__ == '__main__':
            app.run_server(debug=True)


# Main Execution
file_path = 'hospitality_data.csv'
analytics = HospitalityAnalytics(file_path)
analytics.preprocess_data()
analytics.train_model()
analytics.visualize_trends()

