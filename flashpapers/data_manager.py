import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from utils import save_json

logger = logging.getLogger(__name__)

DATA_DIR = "data"
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
FLASHPAPER_FILE = os.path.join(DATA_DIR, "flashpapers.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "categories": [
        "LLM",
        "RL",
        "NLP",
        "ML/DL",
        "SSL",
        "Optimization",
        "CV",
        "Other",
    ],
    "backup_frequency_days": 2,
    "last_backup_timestamp": None,  # Store timestamp for better tracking
    "srs_parameters": {
        "initial_ease_factor": 2.5,
        "minimum_interval_days": 1,
        "maximum_interval_days": 365,
        # These could be used if modifying SM-2 or using another algorithm
        # "easy_interval_multiplier": 2.5,
        # "medium_interval_multiplier": 1.5,
        # "hard_interval_multiplier": 1.2,
    },
    "current_user": "default",  # Placeholder for potential multi-user features
}

DEFAULT_FLASHPAPER_STRUCTURE = {
    "Title": "Enter the title of the paper",
    "Authors": "Enter the authors of the paper",
    "Background of the study": "Summarize the motivation behind the research, its relevance, and the problem it aims to address.",
    "Research objectives and hypothesis": "Clearly outline the main goal of the study and the hypothesis the authors are testing.",
    "Methodology": "Describe how the authors conducted their research, including experimental design, datasets, and evaluation methods.",
    "Results and findings": "Summarize the key outcomes of the study, highlighting improvements or novel discoveries.",
    "Discussion and interpretation": "Explain the broader implications of the findings and how they compare to existing approaches.",
    "Contributions to the field": "Highlight the unique contributions of the study and its significance.",
    "Achievements and significance": "Conclude with the practical impact and potential real-world applications of the research.",
    "Link": "Enter the link to the paper",
    "Notes": "Enter any additional notes or comments about the paper",
    "Keywords": "Enter relevant keywords or tags for the paper",
    "Category": "Select a category for the paper",
}


def ensure_directories():
    """
    Creates necessary data directories if they don't exist
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)


def _load_data(path: str, required_keys: List[str] = None) -> Any:
    """
    Loads JSON data from the given file path.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if required_keys:
                for key in required_keys:
                    if key not in data:
                        logger.warning(f"Missing key '{key}' in {path}.")
            return data
    except FileNotFoundError:
        logger.warning(f"File {path} not found. Returning default data.")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for file {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise


def load_config() -> Dict[str, Any]:
    return _load_data(CONFIG_FILE, required_keys=DEFAULT_CONFIG.keys())


def load_flashpapers() -> List[Dict[str, Any]]:
    return _load_data(FLASHPAPER_FILE, required_keys=DEFAULT_FLASHPAPER_STRUCTURE.keys())


def load_flashpapers_as_df() -> pd.DataFrame:
    """Loads flashpapers from the JSON file and returns them as a DataFrame."""
    # Check if flashpaper file exists
    if not Path(FLASHPAPER_FILE).exists():
        logger.warning(f"Flashpaper file {FLASHPAPER_FILE} does not exist")
        return pd.DataFrame()

    try:
        # Load the flashpapers from the file
        with open(FLASHPAPER_FILE, "r") as f:
            data = json.load(f)

        # If no data or empty list, return empty DataFrame
        if not data:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Convert date strings to datetime objects if they exist
        date_columns = ["added_date", "next_review_date"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])

        return df

    except Exception as e:
        logger.error(f"Error loading flashpapers: {e}")
        return pd.DataFrame()


def add_flashpaper(flashpaper: Dict[str, Any], file_path: str) -> None:
    """Adds a new flashpaper to the list of flashpapers."""
    print(flashpaper)
    save_json(flashpaper, file_path, mode="a")
