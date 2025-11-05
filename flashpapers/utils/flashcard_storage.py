"""Storage layer for flashpapers with JSON persistence."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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
        # Cache management
        self._cache: Optional[List[Flashpaper]] = None
        self._cache_timestamp: Optional[float] = None
        self._id_index: Optional[Dict[str, Flashpaper]] = None

    def _ensure_storage_exists(self) -> None:
        """Create storage file if it doesn't exist."""
        if not self.storage_path.exists():
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _get_cache(self) -> Optional[List[Flashpaper]]:
        """
        Get cached data if valid, otherwise None.

        Returns:
            Cached flashpapers list if cache is valid, None otherwise
        """
        if self._cache is None or self._cache_timestamp is None:
            return None

        # Check if file has been modified since cache was created
        if self.storage_path.exists():
            file_mtime = self.storage_path.stat().st_mtime
            if file_mtime > self._cache_timestamp:
                # File was modified, cache is invalid
                self._cache = None
                self._cache_timestamp = None
                self._id_index = None
                return None

        return self._cache

    def invalidate_cache(self) -> None:
        """Invalidate the cache."""
        self._cache = None
        self._cache_timestamp = None
        self._id_index = None

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
        Uses cache if available and valid.

        Returns:
            List of Flashpaper objects
        """
        # Check cache first
        cached = self._get_cache()
        if cached is not None:
            return cached

        # Load from file
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            flashpapers = [Flashpaper(**item) for item in data]

            # Update cache
            self._cache = flashpapers
            self._cache_timestamp = datetime.now().timestamp()
            self._id_index = None  # Will be rebuilt when needed

            return flashpapers
        except Exception as e:
            print(f"Error loading flashpapers: {e}")
            return []

    def load_by_id(self, flashpaper_id: str) -> Optional[Flashpaper]:
        """
        Load a specific flashpaper by ID.
        Uses cached data and dictionary index for O(1) lookup.

        Args:
            flashpaper_id: ID of the flashpaper

        Returns:
            Flashpaper object or None if not found
        """
        # Get or build ID index
        if self._id_index is None:
            flashpapers = self.load_all()
            self._id_index = {fp.id: fp for fp in flashpapers}

        # Lookup in index
        return self._id_index.get(flashpaper_id)

    def save_all(self, flashpapers: List[Flashpaper]) -> None:
        """
        Save all flashpapers to storage.

        Args:
            flashpapers: List of Flashpaper objects
        """
        data = [fp.model_dump() for fp in flashpapers]
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        # Update cache after save
        self._cache = flashpapers
        self._cache_timestamp = datetime.now().timestamp()
        self._id_index = {fp.id: fp for fp in flashpapers}

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
            # Invalidate cache after restore
            self.invalidate_cache()
            return True
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False

    def get_count(self) -> int:
        """
        Get total count of flashpapers.
        Uses cache when available.

        Returns:
            Number of flashpapers
        """
        cached = self._get_cache()
        if cached is not None:
            return len(cached)
        return len(self.load_all())
