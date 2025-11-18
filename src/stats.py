"""
Statistical calculations for Spotify listening data.

This module computes:
- Cost per hour of listening
- Confidence intervals for monthly listening
- Correlations between listening time and time of day
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Tuple


def calculate_cost_per_hour(monthly_hours: pd.Series, subscription_cost: float) -> pd.Series:
    """
    Calculate the cost per hour of listening for each month.

    Args:
        monthly_hours: Series of total hours listened per month
        subscription_cost: Monthly subscription cost (e.g., 10.99)

    Returns:
        Series with cost per hour for each month
    """
    # Avoid division by zero for months with no listening
    cost_per_hour = subscription_cost / monthly_hours.replace(0, np.nan)

    return cost_per_hour


def calculate_monthly_ci(monthly_hours: pd.Series, confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for monthly listening hours.

    This assumes monthly listening hours are normally distributed and
    computes the confidence interval for the mean.

    Args:
        monthly_hours: Series of total hours listened per month
        confidence: Confidence level (default: 0.95 for 95% CI)

    Returns:
        Tuple of (mean, lower_bound, upper_bound)
    """
    # Calculate mean and standard error
    mean = monthly_hours.mean()
    sem = stats.sem(monthly_hours)  # Standard error of the mean
    n = len(monthly_hours)

    # Calculate confidence interval using t-distribution
    # (appropriate for small sample sizes)
    confidence_interval = stats.t.interval(
        confidence,
        df=n - 1,  # degrees of freedom
        loc=mean,
        scale=sem
    )

    lower_bound, upper_bound = confidence_interval

    return mean, lower_bound, upper_bound


def calculate_hourly_correlation(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate correlation between hour of day and listening time.

    This helps answer: "Do I listen more at certain times of day?"

    Args:
        df: Processed DataFrame with 'hour_of_day' and 'minutes_played' columns

    Returns:
        Tuple of (correlation_coefficient, p_value)

    Note:
        - Correlation close to 0: no relationship
        - Positive correlation: more listening at later hours
        - Negative correlation: more listening at earlier hours
        - p_value < 0.05: statistically significant relationship
    """
    # Aggregate by hour to get average listening time
    hourly_avg = df.groupby('hour_of_day')['minutes_played'].mean()

    # Calculate Pearson correlation
    correlation, p_value = stats.pearsonr(
        hourly_avg.index,  # hours (0-23)
        hourly_avg.values  # average minutes
    )

    return correlation, p_value


def calculate_weekend_effect_size(df: pd.DataFrame) -> dict:
    """
    Calculate effect size of weekend vs weekday listening.

    Uses Cohen's d to measure the standardized difference between
    weekend and weekday listening.

    Args:
        df: Processed DataFrame with 'is_weekend' and 'minutes_played' columns

    Returns:
        Dictionary with effect size statistics

    Note:
        Cohen's d interpretation:
        - 0.2: small effect
        - 0.5: medium effect
        - 0.8: large effect
    """
    # Get daily listening totals
    daily_listening = df.groupby(['date', 'is_weekend'])['minutes_played'].sum().reset_index()

    weekday_data = daily_listening[~daily_listening['is_weekend']]['minutes_played']
    weekend_data = daily_listening[daily_listening['is_weekend']]['minutes_played']

    # Calculate Cohen's d
    mean_diff = weekend_data.mean() - weekday_data.mean()
    pooled_std = np.sqrt(
        ((len(weekday_data) - 1) * weekday_data.std() ** 2 +
         (len(weekend_data) - 1) * weekend_data.std() ** 2) /
        (len(weekday_data) + len(weekend_data) - 2)
    )

    cohens_d = mean_diff / pooled_std

    # Perform t-test to check if difference is statistically significant
    t_stat, p_value = stats.ttest_ind(weekend_data, weekday_data)

    return {
        'cohens_d': cohens_d,
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'weekday_mean': weekday_data.mean(),
        'weekend_mean': weekend_data.mean(),
        'mean_difference': mean_diff
    }


def generate_summary_stats(df: pd.DataFrame, subscription_cost: float = 10.99) -> dict:
    """
    Generate a comprehensive summary of all statistics.

    Args:
        df: Processed DataFrame
        subscription_cost: Monthly subscription cost

    Returns:
        Dictionary with all key statistics
    """
    # Monthly aggregation
    monthly = df.groupby('month').agg(
        total_hours=('hours_played', 'sum')
    )

    # Calculate statistics
    mean_hours, ci_lower, ci_upper = calculate_monthly_ci(monthly['total_hours'])
    cost_per_hour = calculate_cost_per_hour(monthly['total_hours'], subscription_cost)
    hourly_corr, hourly_p = calculate_hourly_correlation(df)
    weekend_stats = calculate_weekend_effect_size(df)

    summary = {
        'monthly_hours': {
            'mean': mean_hours,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'min': monthly['total_hours'].min(),
            'max': monthly['total_hours'].max(),
        },
        'cost_analysis': {
            'subscription_cost': subscription_cost,
            'avg_cost_per_hour': cost_per_hour.mean(),
            'min_cost_per_hour': cost_per_hour.min(),
            'max_cost_per_hour': cost_per_hour.max(),
        },
        'time_patterns': {
            'hourly_correlation': hourly_corr,
            'hourly_correlation_p_value': hourly_p,
            'weekend_vs_weekday': weekend_stats
        },
        'overall': {
            'total_hours': df['hours_played'].sum(),
            'total_tracks': len(df),
            'date_range': f"{df['endTime'].min().date()} to {df['endTime'].max().date()}",
        }
    }

    return summary


def print_summary(summary: dict) -> None:
    """
    Pretty-print the summary statistics.

    Args:
        summary: Dictionary from generate_summary_stats()
    """
    print("=" * 60)
    print("SPOTIFY SUBSCRIPTION VALUE ANALYSIS")
    print("=" * 60)

    print("\n📊 OVERALL STATISTICS")
    print(f"  Total listening time: {summary['overall']['total_hours']:.1f} hours")
    print(f"  Total tracks played: {summary['overall']['total_tracks']:,}")
    print(f"  Date range: {summary['overall']['date_range']}")

    print("\n📅 MONTHLY LISTENING HOURS")
    print(f"  Average: {summary['monthly_hours']['mean']:.1f} hours/month")
    print(f"  95% CI: [{summary['monthly_hours']['ci_95_lower']:.1f}, {summary['monthly_hours']['ci_95_upper']:.1f}]")
    print(f"  Range: {summary['monthly_hours']['min']:.1f} - {summary['monthly_hours']['max']:.1f} hours")

    print("\n💰 COST ANALYSIS")
    print(f"  Subscription cost: ${summary['cost_analysis']['subscription_cost']:.2f}/month")
    print(f"  Average cost per hour: ${summary['cost_analysis']['avg_cost_per_hour']:.2f}")
    print(f"  Best value: ${summary['cost_analysis']['min_cost_per_hour']:.2f}/hour")
    print(f"  Worst value: ${summary['cost_analysis']['max_cost_per_hour']:.2f}/hour")

    print("\n🕐 TIME PATTERNS")
    weekend_stats = summary['time_patterns']['weekend_vs_weekday']
    print(f"  Weekday average: {weekend_stats['weekday_mean']:.1f} min/day")
    print(f"  Weekend average: {weekend_stats['weekend_mean']:.1f} min/day")
    print(f"  Difference: {weekend_stats['mean_difference']:+.1f} min/day")
    print(f"  Effect size (Cohen's d): {weekend_stats['cohens_d']:.2f}")
    print(f"  Statistically significant: {'Yes' if weekend_stats['significant'] else 'No'} (p={weekend_stats['p_value']:.4f})")

    corr = summary['time_patterns']['hourly_correlation']
    corr_p = summary['time_patterns']['hourly_correlation_p_value']
    print(f"\n  Hour-of-day correlation: {corr:.3f} (p={corr_p:.4f})")
    if corr_p < 0.05:
        direction = "later" if corr > 0 else "earlier"
        print(f"  → You tend to listen more during {direction} hours of the day")
    else:
        print(f"  → No significant relationship with hour of day")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Example usage
    from load_data import load_streaming_history
    from process_data import process_streaming_data

    df = load_streaming_history("../data")
    df = process_streaming_data(df)

    summary = generate_summary_stats(df, subscription_cost=10.99)
    print_summary(summary)
