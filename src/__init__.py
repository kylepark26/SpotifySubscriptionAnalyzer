"""
Music Subscription Value Analyzer

A simple, interpretable data analysis project for quantifying
the value of your Spotify subscription.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .load_data import load_streaming_history, validate_data
from .process_data import process_streaming_data, aggregate_by_month
from .stats import generate_summary_stats, print_summary
from .plots import create_all_plots

__all__ = [
    'load_streaming_history',
    'validate_data',
    'process_streaming_data',
    'aggregate_by_month',
    'generate_summary_stats',
    'print_summary',
    'create_all_plots',
]
