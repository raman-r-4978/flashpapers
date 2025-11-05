"""Data handler with Spaced Repetition System (SRS) logic."""

from datetime import datetime, timedelta
from typing import List, Optional

from flashpapers.config import ConfigManager
from flashpapers.models import Flashpaper, ReviewResponse
from flashpapers.utils.flashcard_storage import FlashcardStorage


class FlashcardDataHandler:
    """Handles flashcard data operations with SRS scheduling."""

    def __init__(
        self,
        storage: Optional[FlashcardStorage] = None,
        config_manager: Optional[ConfigManager] = None,
    ):
        """
        Initialize data handler.

        Args:
            storage: FlashcardStorage instance
            config_manager: ConfigManager instance
        """
        self.storage = storage or FlashcardStorage()
        self.config_manager = config_manager or ConfigManager()
        self.config = self.config_manager.get_config()

    def add_flashcard(
        self,
        paper_title: str,
        authors: str,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        tags: Optional[List[str]] = None,
        difficulty: str = "medium",
        **kwargs,
    ) -> str:
        """
        Add a new flashcard.

        Args:
            paper_title: Title of the paper
            authors: Authors of the paper
            question: Question (for compatibility)
            answer: Answer (for compatibility)
            tags: List of tags/keywords
            difficulty: Initial difficulty
            **kwargs: Additional flashpaper fields

        Returns:
            ID of the created flashcard
        """
        # Handle legacy question/answer format
        if question and not kwargs.get("research_objectives_and_hypothesis"):
            kwargs["research_objectives_and_hypothesis"] = question
        if answer and not kwargs.get("results_and_findings"):
            kwargs["results_and_findings"] = answer

        flashpaper = Flashpaper(
            paper_title=paper_title,
            authors=authors,
            keywords=tags or [],
            **kwargs,
        )

        # Set initial review date
        srs_params = self.config.srs_parameters
        flashpaper.next_review_date = datetime.now() + timedelta(
            days=srs_params["minimum_interval_days"]
        )
        flashpaper.ease_factor = srs_params["initial_ease_factor"]

        return self.storage.add(flashpaper)

    def get_flashcards_for_review(self, limit: Optional[int] = None) -> List[Flashpaper]:
        """
        Get flashcards due for review.

        Args:
            limit: Maximum number of cards to return

        Returns:
            List of Flashpaper objects due for review
        """
        flashpapers = self.storage.load_all()
        now = datetime.now()

        due_papers = [
            fp for fp in flashpapers if fp.next_review_date is None or fp.next_review_date <= now
        ]

        # Sort by next review date (earliest first)
        due_papers.sort(key=lambda x: x.next_review_date or datetime.min)

        if limit:
            return due_papers[:limit]
        return due_papers

    def update_flashcard_review(self, flashpaper_id: str, success: bool) -> bool:
        """
        Update flashcard after review (legacy compatibility).

        Args:
            flashpaper_id: ID of the flashcard
            success: Whether the review was successful

        Returns:
            True if updated successfully
        """
        difficulty = "easy" if success else "hard"
        response = ReviewResponse(flashpaper_id=flashpaper_id, difficulty=difficulty)
        return self.process_review(response)

    def process_review(self, response: ReviewResponse) -> bool:
        """
        Process a review response and update SRS schedule.

        Args:
            response: ReviewResponse object

        Returns:
            True if processed successfully
        """
        flashpaper = self.storage.load_by_id(response.flashpaper_id)
        if not flashpaper:
            return False

        srs_params = self.config.srs_parameters

        # Update ease factor based on difficulty
        if response.difficulty == "easy":
            flashpaper.ease_factor *= srs_params.get("easy_bonus", 1.3)
        elif response.difficulty == "hard":
            flashpaper.ease_factor *= srs_params.get("hard_penalty", 0.8)

        # Ensure ease factor stays within bounds
        flashpaper.ease_factor = max(1.3, flashpaper.ease_factor)

        # Calculate new interval
        if flashpaper.interval_days == 0:
            new_interval = srs_params["minimum_interval_days"]
        else:
            new_interval = int(flashpaper.interval_days * flashpaper.ease_factor)

        # Apply bounds
        new_interval = max(srs_params["minimum_interval_days"], new_interval)
        new_interval = min(srs_params["maximum_interval_days"], new_interval)

        # Update flashpaper
        flashpaper.interval_days = new_interval
        flashpaper.last_review_date = response.timestamp
        flashpaper.next_review_date = response.timestamp + timedelta(days=new_interval)
        flashpaper.review_count += 1

        return self.storage.update(flashpaper)

    def update_flashcard(self, flashpaper: Flashpaper) -> bool:
        """
        Update a flashcard.

        Args:
            flashpaper: Updated Flashpaper object

        Returns:
            True if updated successfully
        """
        return self.storage.update(flashpaper)

    def delete_flashcard(self, flashpaper_id: str) -> bool:
        """
        Delete a flashcard.

        Args:
            flashpaper_id: ID of the flashcard to delete

        Returns:
            True if deleted successfully
        """
        return self.storage.delete(flashpaper_id)

    def get_all_flashcards(self) -> List[Flashpaper]:
        """
        Get all flashcards.

        Returns:
            List of all Flashpaper objects
        """
        return self.storage.load_all()

    def get_flashcard_by_id(self, flashpaper_id: str) -> Optional[Flashpaper]:
        """
        Get a specific flashcard by ID.

        Args:
            flashpaper_id: ID of the flashcard

        Returns:
            Flashpaper object or None if not found
        """
        return self.storage.load_by_id(flashpaper_id)
