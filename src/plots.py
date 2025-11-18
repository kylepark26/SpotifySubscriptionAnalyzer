"""
Visualization functions for Spotify listening data.

This module creates clean, interpretable plots for:
- Monthly listening trends
- Cost per hour over time
- Hourly listening patterns
- Weekday vs weekend comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def set_plot_style():
    """Set a clean, professional plot style."""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10


def plot_monthly_hours(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot monthly listening hours over time.

    Args:
        df: Processed DataFrame with 'month' and 'hours_played' columns
        save_path: Optional path to save the figure
    """
    # Aggregate by month
    monthly = df.groupby('month')['hours_played'].sum()

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot bars
    monthly.plot(kind='bar', ax=ax, color='#1DB954', alpha=0.8)

    # Add trend line
    x = np.arange(len(monthly))
    z = np.polyfit(x, monthly.values, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r--", alpha=0.6, linewidth=2, label='Trend')

    # Formatting
    ax.set_title('Monthly Listening Hours', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Hours Played')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add value labels on bars
    for i, v in enumerate(monthly.values):
        ax.text(i, v + 1, f'{v:.0f}h', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    plt.show()


def plot_cost_per_hour(df: pd.DataFrame, subscription_cost: float, save_path: Optional[str] = None) -> None:
    """
    Plot cost per hour of listening over time.

    Args:
        df: Processed DataFrame with 'month' and 'hours_played' columns
        subscription_cost: Monthly subscription cost
        save_path: Optional path to save the figure
    """
    from stats import calculate_cost_per_hour

    # Aggregate by month
    monthly_hours = df.groupby('month')['hours_played'].sum()
    cost_per_hour = calculate_cost_per_hour(monthly_hours, subscription_cost)

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot line
    cost_per_hour.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=8, color='#1DB954')

    # Add average line
    avg_cost = cost_per_hour.mean()
    ax.axhline(avg_cost, color='red', linestyle='--', alpha=0.6,
               label=f'Average: ${avg_cost:.2f}/hour')

    # Formatting
    ax.set_title(f'Cost Per Hour of Listening (${subscription_cost:.2f}/month subscription)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Cost per Hour ($)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    plt.show()


def plot_hourly_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot listening time distribution by hour of day.

    Args:
        df: Processed DataFrame with 'hour_of_day' and 'minutes_played' columns
        save_path: Optional path to save the figure
    """
    # Aggregate by hour
    hourly = df.groupby('hour_of_day')['minutes_played'].sum()

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot bars
    hourly.plot(kind='bar', ax=ax, color='#1DB954', alpha=0.8)

    # Formatting
    ax.set_title('Listening Distribution by Hour of Day', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour of Day (24-hour format)')
    ax.set_ylabel('Total Minutes Played')
    ax.grid(axis='y', alpha=0.3)

    # Highlight peak hours
    peak_hour = hourly.idxmax()
    ax.get_children()[peak_hour].set_color('#FF6B6B')

    # Add note about peak hour
    ax.text(0.98, 0.95, f'Peak: {peak_hour}:00 ({hourly.max():.0f} min)',
            transform=ax.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Format x-axis
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h}:00' for h in range(0, 24, 2)])
    plt.xticks(rotation=0)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    plt.show()


def plot_weekday_weekend_comparison(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot comparison of weekday vs weekend listening.

    Args:
        df: Processed DataFrame with 'is_weekend' and 'minutes_played' columns
        save_path: Optional path to save the figure
    """
    # Calculate daily averages
    daily = df.groupby(['date', 'is_weekend'])['minutes_played'].sum().reset_index()

    weekday_data = daily[~daily['is_weekend']]['minutes_played']
    weekend_data = daily[daily['is_weekend']]['minutes_played']

    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Box plot comparison
    ax1.boxplot([weekday_data, weekend_data], labels=['Weekday', 'Weekend'],
                patch_artist=True,
                boxprops=dict(facecolor='#1DB954', alpha=0.6))

    ax1.set_title('Weekday vs Weekend Listening', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Minutes per Day')
    ax1.grid(axis='y', alpha=0.3)

    # Add mean markers
    ax1.plot([1, 2], [weekday_data.mean(), weekend_data.mean()],
             'ro', markersize=10, label='Mean')
    ax1.legend()

    # Bar plot of averages
    means = [weekday_data.mean(), weekend_data.mean()]
    std_errs = [weekday_data.sem(), weekend_data.sem()]

    x_pos = [0, 1]
    ax2.bar(x_pos, means, yerr=std_errs, capsize=10,
            color=['#1DB954', '#FF6B6B'], alpha=0.8)

    ax2.set_title('Average Daily Listening', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Minutes per Day')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(['Weekday', 'Weekend'])
    ax2.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, (mean, se) in enumerate(zip(means, std_errs)):
        ax2.text(i, mean + se + 5, f'{mean:.0f} min', ha='center', fontweight='bold')

    # Calculate and display percentage difference
    pct_diff = ((weekend_data.mean() - weekday_data.mean()) / weekday_data.mean()) * 100
    ax2.text(0.5, 0.95, f'Weekend is {abs(pct_diff):.1f}% {"higher" if pct_diff > 0 else "lower"}',
             transform=ax2.transAxes, ha='center', va='top', fontsize=11,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    plt.show()


def create_all_plots(df: pd.DataFrame, subscription_cost: float = 10.99, save_dir: Optional[str] = None) -> None:
    """
    Generate all plots at once.

    Args:
        df: Processed DataFrame
        subscription_cost: Monthly subscription cost
        save_dir: Optional directory to save plots
    """
    set_plot_style()

    print("Generating plots...")

    # Monthly hours
    save_path = f"{save_dir}/monthly_hours.png" if save_dir else None
    plot_monthly_hours(df, save_path)

    # Cost per hour
    save_path = f"{save_dir}/cost_per_hour.png" if save_dir else None
    plot_cost_per_hour(df, subscription_cost, save_path)

    # Hourly distribution
    save_path = f"{save_dir}/hourly_distribution.png" if save_dir else None
    plot_hourly_distribution(df, save_path)

    # Weekday vs weekend
    save_path = f"{save_dir}/weekday_weekend.png" if save_dir else None
    plot_weekday_weekend_comparison(df, save_path)

    print("\nAll plots generated!")


if __name__ == "__main__":
    # Example usage
    from load_data import load_streaming_history
    from process_data import process_streaming_data

    df = load_streaming_history("../data")
    df = process_streaming_data(df)

    create_all_plots(df, subscription_cost=10.99)
