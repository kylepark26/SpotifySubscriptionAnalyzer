"""
Process and clean Spotify streaming history data.

This module handles:
- Converting timestamps to datetime objects
- Calculating listening hours
- Adding time-based features (month, weekday, hour, etc.)
- Filtering out very short plays (skips)
"""

import pandas as pd
import numpy as np


def process_streaming_data(df: pd.DataFrame, min_seconds: int = 30) -> pd.DataFrame:
    """
    Process raw streaming data into analysis-ready format.

    Args:
        df: Raw DataFrame from load_data.py
        min_seconds: Minimum play time in seconds to count as a "listen"
                     (filters out skips). Default is 30 seconds.

    Returns:
        Processed DataFrame with datetime columns and time features
    """
    # Create a copy to avoid modifying the original
    df = df.copy()

    # Convert endTime to datetime
    df['endTime'] = pd.to_datetime(df['endTime'])

    # Calculate minutes and hours played
    df['minutes_played'] = df['msPlayed'] / (1000 * 60)
    df['hours_played'] = df['msPlayed'] / (1000 * 60 * 60)

    # Filter out very short plays (likely skips)
    df = df[df['msPlayed'] >= min_seconds * 1000].copy()

    # Extract time features for analysis
    df['date'] = df['endTime'].dt.date
    df['year'] = df['endTime'].dt.year
    df['month'] = df['endTime'].dt.to_period('M')  # e.g., "2024-01"
    df['day_of_week'] = df['endTime'].dt.day_name()
    df['hour_of_day'] = df['endTime'].dt.hour
    df['is_weekend'] = df['endTime'].dt.dayofweek.isin([5, 6])  # Saturday=5, Sunday=6

    # Sort by time
    df = df.sort_values('endTime').reset_index(drop=True)

    print(f"Processed {len(df):,} listening records")
    print(f"Filtered out {len(df) - len(df):,} short plays (< {min_seconds}s)")
    print(f"Total listening time: {df['hours_played'].sum():.1f} hours")

    return df


def aggregate_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate listening data by month.

    Args:
        df: Processed DataFrame from process_streaming_data()

    Returns:
        DataFrame with monthly aggregations:
        - total_hours: Total listening hours
        - total_tracks: Number of tracks played
        - unique_artists: Number of unique artists
        - unique_tracks: Number of unique tracks
    """
    monthly = df.groupby('month').agg({
        'hours_played': 'sum',
        'trackName': 'count',
        'artistName': 'nunique',
        'trackName': 'nunique'
    }).rename(columns={
        'hours_played': 'total_hours',
        'trackName': 'total_tracks',
        'artistName': 'unique_artists'
    })

    # Fix duplicate column name issue
    monthly = df.groupby('month').agg(
        total_hours=('hours_played', 'sum'),
        total_tracks=('trackName', 'count'),
        unique_artists=('artistName', 'nunique'),
        unique_tracks=('trackName', 'nunique')
    )

    # Calculate percent change from previous month
    monthly['hours_change_pct'] = monthly['total_hours'].pct_change() * 100

    return monthly


def get_weekday_weekend_stats(df: pd.DataFrame) -> dict:
    """
    Calculate average listening time for weekdays vs weekends.

    Args:
        df: Processed DataFrame from process_streaming_data()

    Returns:
        Dictionary with weekday and weekend statistics
    """
    weekday_avg = df[~df['is_weekend']].groupby('date')['minutes_played'].sum().mean()
    weekend_avg = df[df['is_weekend']].groupby('date')['minutes_played'].sum().mean()

    # Calculate percentage difference
    pct_diff = ((weekend_avg - weekday_avg) / weekday_avg) * 100

    return {
        'weekday_avg_minutes': weekday_avg,
        'weekend_avg_minutes': weekend_avg,
        'difference_pct': pct_diff,
        'weekend_higher': weekend_avg > weekday_avg
    }


def get_hourly_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get listening time distribution by hour of day.

    Args:
        df: Processed DataFrame from process_streaming_data()

    Returns:
        DataFrame with hours (0-23) and total minutes played
    """
    hourly = df.groupby('hour_of_day').agg(
        total_minutes=('minutes_played', 'sum'),
        count=('trackName', 'count')
    )

    return hourly


if __name__ == "__main__":
    # Example usage
    from load_data import load_streaming_history

    df = load_streaming_history("../data")
    df = process_streaming_data(df)

    print("\nMonthly aggregation:")
    print(aggregate_by_month(df))

    print("\nWeekday vs Weekend:")
    print(get_weekday_weekend_stats(df))

    print("\nHourly distribution:")
    print(get_hourly_distribution(df).head(10))
