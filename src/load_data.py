"""
Load Spotify streaming history data from JSON files.

This module handles loading and combining multiple StreamingHistory JSON files
exported from Spotify's "Your Data" download.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Union


def load_streaming_history(data_dir: Union[str, Path]) -> pd.DataFrame:
    """
    Load all StreamingHistory*.json files from the specified directory.

    Spotify exports streaming history in files named:
    - StreamingHistory0.json
    - StreamingHistory1.json
    - etc.

    Args:
        data_dir: Path to the directory containing StreamingHistory JSON files

    Returns:
        DataFrame with columns: endTime, artistName, trackName, msPlayed

    Raises:
        FileNotFoundError: If no StreamingHistory files are found
    """
    data_dir = Path(data_dir)

    # Find all StreamingHistory*.json files
    streaming_files = sorted(data_dir.glob("StreamingHistory*.json"))

    if not streaming_files:
        raise FileNotFoundError(
            f"No StreamingHistory*.json files found in {data_dir}.\n"
            "Please download your Spotify data from: "
            "https://www.spotify.com/account/privacy/"
        )

    print(f"Found {len(streaming_files)} streaming history file(s)")

    # Load and combine all files
    all_data = []
    for file_path in streaming_files:
        print(f"Loading {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    print(f"\nLoaded {len(df):,} streaming records")
    print(f"Date range: {df['endTime'].min()} to {df['endTime'].max()}")

    return df


def validate_data(df: pd.DataFrame) -> None:
    """
    Validate that the loaded data has the expected columns and format.

    Args:
        df: DataFrame to validate

    Raises:
        ValueError: If required columns are missing
    """
    required_columns = {'endTime', 'artistName', 'trackName', 'msPlayed'}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )

    print("✓ Data validation passed")


if __name__ == "__main__":
    # Example usage
    df = load_streaming_history("../data")
    validate_data(df)
    print("\nFirst few records:")
    print(df.head())
