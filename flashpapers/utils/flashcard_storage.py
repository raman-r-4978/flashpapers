"""Storage layer for flashpapers with JSON persistence."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

from flashpapers.models import Flashpaper


class FlashcardStorage:
    """Handles persistent storage of flashpapers."""

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize storage.

        Args:
            storage_path: Path to storage file. Defaults to data/flashpapers.json
        """
        self.storage_path = storage_path or Path("data/flashpapers.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage file if it doesn't exist."""
        if not self.storage_path.exists():
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_flashcards(self) -> pd.DataFrame:
        """
        Load all flashcards as DataFrame.

        Returns:
            DataFrame containing all flashcards
        """
        flashpapers = self.load_all()
        if not flashpapers:
            return pd.DataFrame()

        data = [fp.model_dump() for fp in flashpapers]
        df = pd.DataFrame(data)

        # Convert datetime strings to datetime objects
        datetime_cols = ["added_date", "next_review_date", "last_review_date"]
        for col in datetime_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

    def load_all(self) -> List[Flashpaper]:
        """
        Load all flashpapers from storage.

        Returns:
            List of Flashpaper objects
        """
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Flashpaper(**item) for item in data]
        except Exception as e:
            print(f"Error loading flashpapers: {e}")
            return []

    def load_by_id(self, flashpaper_id: str) -> Optional[Flashpaper]:
        """
        Load a specific flashpaper by ID.

        Args:
            flashpaper_id: ID of the flashpaper

        Returns:
            Flashpaper object or None if not found
        """
        flashpapers = self.load_all()
        for fp in flashpapers:
            if fp.id == flashpaper_id:
                return fp
        return None

    def save_all(self, flashpapers: List[Flashpaper]) -> None:
        """
        Save all flashpapers to storage.

        Args:
            flashpapers: List of Flashpaper objects
        """
        data = [fp.model_dump() for fp in flashpapers]
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def add(self, flashpaper: Flashpaper) -> str:
        """
        Add a new flashpaper.

        Args:
            flashpaper: Flashpaper object to add

        Returns:
            ID of the added flashpaper
        """
        flashpapers = self.load_all()
        flashpapers.append(flashpaper)
        self.save_all(flashpapers)
        return flashpaper.id

    def update(self, flashpaper: Flashpaper) -> bool:
        """
        Update an existing flashpaper.

        Args:
            flashpaper: Updated Flashpaper object

        Returns:
            True if updated successfully, False otherwise
        """
        flashpapers = self.load_all()
        for i, fp in enumerate(flashpapers):
            if fp.id == flashpaper.id:
                flashpapers[i] = flashpaper
                self.save_all(flashpapers)
                return True
        return False

    def delete(self, flashpaper_id: str) -> bool:
        """
        Delete a flashpaper by ID.

        Args:
            flashpaper_id: ID of the flashpaper to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        flashpapers = self.load_all()
        original_count = len(flashpapers)
        flashpapers = [fp for fp in flashpapers if fp.id != flashpaper_id]

        if len(flashpapers) < original_count:
            self.save_all(flashpapers)
            return True
        return False

    def create_backup(self, backup_dir: Optional[Path] = None) -> Path:
        """
        Create a backup of the storage file.

        Args:
            backup_dir: Directory for backups. Defaults to data/backups

        Returns:
            Path to the backup file
        """
        backup_dir = backup_dir or self.storage_path.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"flashpapers_backup_{timestamp}.json"

        shutil.copy2(self.storage_path, backup_path)
        return backup_path

    def restore_from_backup(self, backup_path: Path) -> bool:
        """
        Restore flashpapers from a backup file.

        Args:
            backup_path: Path to the backup file

        Returns:
            True if restored successfully, False otherwise
        """
        try:
            # Validate the backup file
            with open(backup_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            [Flashpaper(**item) for item in data]  # Validate structure

            # Create a backup of current state before restoring
            self.create_backup()

            # Restore from backup
            shutil.copy2(backup_path, self.storage_path)
            return True
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False

    def get_count(self) -> int:
        """
        Get total count of flashpapers.

        Returns:
            Number of flashpapers
        """
        return len(self.load_all())
