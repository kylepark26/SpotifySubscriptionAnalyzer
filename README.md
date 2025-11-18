# Music Subscription Value Analyzer

A clean, interpretable data analysis project that quantifies the value of your Spotify subscription by analyzing your listening history.

## What This Project Does

This project analyzes your Spotify streaming history to answer the question: **"Am I getting good value from my music subscription?"**

It computes simple, interpretable statistics including:
- **Monthly listening hours** - How much you actually use Spotify
- **Cost per hour** - What you're really paying per hour of entertainment
- **95% confidence intervals** - Statistical bounds on your typical monthly usage
- **Weekend vs weekday patterns** - When you listen most
- **Hour-of-day correlations** - Your listening time preferences

**This is NOT a complex ML project.** It's a straightforward statistical analysis using descriptive statistics and basic hypothesis testing - perfect for explaining in interviews.

## Statistics Computed

### 1. Monthly Listening Hours
- Total hours listened per month
- Percent change between months
- Confidence interval for typical monthly usage

### 2. Cost Analysis
- Cost per hour of listening
- Best and worst value months
- Average subscription value

### 3. Temporal Patterns
- Weekend vs weekday average listening time
- Percentage difference and statistical significance (t-test, Cohen's d)
- Hourly distribution of listening
- Correlation between hour of day and listening time

### 4. Statistical Rigor
- **95% Confidence Intervals** using t-distribution
- **Pearson correlation** for time-of-day patterns
- **Cohen's d effect size** for weekday/weekend comparison
- **Independent t-tests** for group comparisons

## Project Structure

```
music_value_analyzer/
├── data/                          # Place your Spotify data here
│   └── StreamingHistory*.json     # Downloaded from Spotify
├── src/                           # Python modules
│   ├── load_data.py              # Load Spotify JSON files
│   ├── process_data.py           # Clean and process data
│   ├── stats.py                  # Statistical calculations
│   └── plots.py                  # Visualization functions
├── notebooks/                     # Jupyter notebooks
│   └── analysis.ipynb            # Main analysis walkthrough
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## How to Get Your Spotify Data

1. Go to [Spotify Account Privacy Settings](https://www.spotify.com/account/privacy/)
2. Scroll to "Download your data"
3. Request "Account data" (includes StreamingHistory)
4. Wait 1-2 weeks for Spotify to prepare your data
5. Download the ZIP file and extract it
6. Copy all `StreamingHistory*.json` files to the `data/` folder

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your Data

Place your `StreamingHistory*.json` files in the `data/` folder.

### 3. Run the Analysis

**Option A: Use Jupyter Notebook (Recommended)**

```bash
jupyter notebook notebooks/analysis.ipynb
```

This provides a step-by-step walkthrough with explanations.

**Option B: Run Python Scripts Directly**

```bash
# From the project root directory
cd src
python stats.py
python plots.py
```

## Understanding the Output

### Monthly Hours with Confidence Interval

```
Average: 42.3 hours/month
95% CI: [35.1, 49.5]
```

**Interpretation:** You typically listen 35-50 hours per month. There's a 95% probability your true average monthly listening falls in this range.

### Cost Per Hour

```
Subscription: $10.99/month
Average cost: $0.26/hour
```

**Interpretation:** You pay about $0.26 per hour of entertainment. Compare this to:
- Movie theater: ~$8-12/hour
- Streaming video: ~$0.50-1.00/hour

### Weekend vs Weekday

```
Weekday average: 82.4 min/day
Weekend average: 115.7 min/day
Difference: +33.3 min/day (+40.4%)
Cohen's d: 0.52 (medium effect)
p-value: 0.003 (significant)
```

**Interpretation:** You listen significantly more on weekends (about 40% more). The medium effect size suggests this is a meaningful behavioral difference.

### Hour-of-Day Correlation

```
Correlation: 0.234
p-value: 0.267
```

**Interpretation:** There's no statistically significant relationship between hour of day and listening time (p > 0.05).

## Technologies Used

- **pandas** - Data manipulation and aggregation
- **numpy** - Numerical computations
- **scipy** - Statistical tests (t-tests, confidence intervals)
- **matplotlib** - Data visualization
- **seaborn** - Enhanced plot styling

### Why These Technologies?

- **No ML libraries** - This is statistical analysis, not prediction
- **Industry-standard tools** - pandas/numpy are universal in data science
- **Simple & interpretable** - Every statistic has a clear meaning
- **Lightweight** - Fast to run, easy to understand

## Key Insights for Interviews

When discussing this project, emphasize:

1. **Problem Framing**: "I wanted to quantify subscription value using behavioral data"

2. **Statistical Rigor**: "I used confidence intervals to account for variability and effect sizes to measure practical significance, not just p-values"

3. **Interpretability**: "Every metric has a clear real-world meaning - cost per hour is directly comparable to other entertainment"

4. **Data Processing**: "I handled timestamp parsing, aggregation across multiple JSON files, and feature engineering for temporal patterns"

5. **Simplicity**: "I deliberately avoided overfitting or complex models - the goal was interpretable insights, not prediction"

## Potential Extensions

If you want to expand this project:

- Add artist/genre analysis
- Compare listening patterns across seasons
- Build a simple dashboard with plotly/streamlit
- Add API integration for automatic updates
- Export results to a clean PDF report

## License

MIT License - Feel free to use this for your own analysis!

## Questions?

This project demonstrates:
- Data ingestion and cleaning
- Temporal feature engineering
- Statistical hypothesis testing
- Confidence interval estimation
- Effect size calculation
- Data visualization
- Clear documentation and code organization

Perfect for discussing in data analyst/scientist interviews!
