"""Tests for flashcard storage."""

import json

import pytest

from flashpapers.models import Flashpaper


class TestFlashcardStorage:
    """Tests for FlashcardStorage class."""

    def test_storage_initialization(self, storage):
        """Test storage initialization."""
        assert storage.storage_path.exists()

    def test_add_flashcard(self, storage, sample_flashpaper):
        """Test adding a flashcard."""
        paper_id = storage.add(sample_flashpaper)
        assert paper_id == sample_flashpaper.id

        # Verify it was saved
        loaded = storage.load_by_id(paper_id)
        assert loaded is not None
        assert loaded.paper_title == sample_flashpaper.paper_title

    def test_load_all_flashcards(self, storage, sample_flashpapers):
        """Test loading all flashcards."""
        # Add multiple papers
        for paper in sample_flashpapers:
            storage.add(paper)

        # Load all
        loaded = storage.load_all()
        assert len(loaded) == len(sample_flashpapers)

    def test_load_by_id(self, storage, sample_flashpaper):
        """Test loading a specific flashcard by ID."""
        paper_id = storage.add(sample_flashpaper)

        loaded = storage.load_by_id(paper_id)
        assert loaded is not None
        assert loaded.id == paper_id
        assert loaded.paper_title == sample_flashpaper.paper_title

    def test_load_by_id_not_found(self, storage):
        """Test loading a non-existent flashcard."""
        loaded = storage.load_by_id("non-existent-id")
        assert loaded is None

    def test_update_flashcard(self, storage, sample_flashpaper):
        """Test updating a flashcard."""
        paper_id = storage.add(sample_flashpaper)

        # Update the paper
        loaded = storage.load_by_id(paper_id)
        loaded.paper_title = "Updated Title"
        loaded.review_count = 5

        success = storage.update(loaded)
        assert success is True

        # Verify update
        updated = storage.load_by_id(paper_id)
        assert updated.paper_title == "Updated Title"
        assert updated.review_count == 5

    def test_update_nonexistent_flashcard(self, storage):
        """Test updating a non-existent flashcard."""
        paper = Flashpaper(id="fake-id", paper_title="Test", authors="Test")
        success = storage.update(paper)
        assert success is False

    def test_delete_flashcard(self, storage, sample_flashpaper):
        """Test deleting a flashcard."""
        paper_id = storage.add(sample_flashpaper)

        # Verify it exists
        assert storage.load_by_id(paper_id) is not None

        # Delete it
        success = storage.delete(paper_id)
        assert success is True

        # Verify it's gone
        assert storage.load_by_id(paper_id) is None

    def test_delete_nonexistent_flashcard(self, storage):
        """Test deleting a non-existent flashcard."""
        success = storage.delete("non-existent-id")
        assert success is False

    def test_get_count(self, storage, sample_flashpapers):
        """Test getting flashcard count."""
        assert storage.get_count() == 0

        for paper in sample_flashpapers:
            storage.add(paper)

        assert storage.get_count() == len(sample_flashpapers)

    def test_create_backup(self, storage, sample_flashpaper, temp_dir):
        """Test creating a backup."""
        storage.add(sample_flashpaper)

        backup_path = storage.create_backup(backup_dir=temp_dir / "backups")
        assert backup_path.exists()
        assert backup_path.suffix == ".json"

        # Verify backup content
        with open(backup_path, "r") as f:
            data = json.load(f)
        assert len(data) == 1

    def test_restore_from_backup(self, storage, sample_flashpapers, temp_dir):
        """Test restoring from a backup."""
        # Add papers and create backup
        for paper in sample_flashpapers:
            storage.add(paper)

        backup_path = storage.create_backup(backup_dir=temp_dir / "backups")

        # Delete all papers
        for paper in storage.load_all():
            storage.delete(paper.id)

        assert storage.get_count() == 0

        # Restore from backup
        success = storage.restore_from_backup(backup_path)
        assert success is True
        assert storage.get_count() == len(sample_flashpapers)

    def test_load_flashcards_as_dataframe(self, storage, sample_flashpapers):
        """Test loading flashcards as DataFrame."""
        for paper in sample_flashpapers:
            storage.add(paper)

        df = storage.load_flashcards()
        assert len(df) == len(sample_flashpapers)
        assert "paper_title" in df.columns
        assert "authors" in df.columns

    def test_empty_storage_dataframe(self, storage):
        """Test loading empty storage as DataFrame."""
        df = storage.load_flashcards()
        assert len(df) == 0
