
# Hospitality-Focused Analytics Suite

The **Hospitality-Focused Analytics Suite** is a data analysis and forecasting tool designed for hospitality businesses. It leverages Python and machine learning to analyze booking trends, optimize revenue, and generate interactive visualizations.

## Features
- Data preprocessing for booking and guest analytics.
- Revenue forecasting using Gradient Boosting Regressor.
- Hyperparameter tuning for optimal model performance.
- Interactive dashboards for booking trend visualizations using Dash and Plotly.

## Installation

Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```text
   pandas
   numpy
   scikit-learn
   dash
   plotly
   joblib
   ```

## Usage

1. **Prepare Your Dataset:**
   Ensure your dataset includes the following columns:
   - `BookingDate`
   - `CheckInDate`
   - `CheckOutDate`
   - `Revenue`
   - `RoomType`
   - `GuestType`

   Save the dataset as `hospitality_data.csv`.

2. **Run the Script:**
   ```bash
   python hospitality_analytics.py
   ```

3. **Explore Interactive Dashboards:**
   The script will launch a Dash server to visualize booking trends.

## Example Output
- **Model Performance:** Mean Squared Error and hyperparameter tuning results.
- **Visualization:** Interactive time-series plots of booking trends.

## Folder Structure
```
hospitality-analytics-suite/
├── hospitality_analytics.py  # Main script          
└── README.md                 # Documentation
```

## Contribution
Contributions are welcome!

## License
This project is licensed under the MIT License. 