
# Guest Sentiment and Engagement Platform

The **Guest Sentiment and Engagement Platform** is a machine learning tool for analyzing guest feedback. It uses transformer-based models to classify feedback as positive or negative and generates actionable insights.

## Features
- Sentiment analysis using a pre-trained transformer model (`DistilBERT`).
- Detailed sentiment analysis reports with percentages.
- Input validation and robust error handling.

## Installation

Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```text
   transformers
   pandas
   ```

## Usage

1. **Prepare Feedback Data:**
   Prepare a list of feedback strings to analyze, such as:
   ```python
   feedbacks = [
       "The room was clean and spacious, loved it!",
       "Terrible service, the staff was rude and unhelpful."
   ]
   ```

2. **Run the Script:**
   ```bash
   python sentiment_analysis.py
   ```

3. **Output:**
   - A DataFrame with sentiment predictions (positive/negative).
   - A summary of sentiment proportions (e.g., percentage of positive feedback).

## Example Output
- **Sentiment Analysis Results:**
  | Feedback                                | Label    | Score   |
  |-----------------------------------------|----------|---------|
  | The room was clean and spacious, loved it! | Positive | 0.95    |
  | Terrible service, the staff was rude.   | Negative | 0.87    |

- **Sentiment Summary (%):**
  - Positive: 50%
  - Negative: 50%

## Folder Structure
```
guest-sentiment-platform/
├── sentiment_analysis.py   # Main script
└── README.md               # Documentation
```

## Contribution
Contributions are welcome!

## License
This project is licensed under the MIT License.