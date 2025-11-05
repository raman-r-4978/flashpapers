"""Tests for flashcard data handler."""

from flashpapers.models import ReviewResponse


class TestFlashcardDataHandler:
    """Tests for FlashcardDataHandler class."""

    def test_add_flashcard(self, data_handler):
        """Test adding a flashcard."""
        paper_id = data_handler.add_flashcard(
            paper_title="Test Paper",
            authors="Test Author",
            tags=["test", "paper"],
            category=["Machine Learning"],
        )

        assert paper_id is not None

        # Verify it was added
        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper is not None
        assert paper.paper_title == "Test Paper"
        assert paper.keywords == ["test", "paper"]

    def test_add_flashcard_with_question_answer(self, data_handler):
        """Test adding flashcard with legacy question/answer format."""
        paper_id = data_handler.add_flashcard(
            paper_title="Test",
            authors="Author",
            question="What is the objective?",
            answer="The main finding",
        )

        paper = data_handler.get_flashcard_by_id(paper_id)
        assert "What is the objective?" in paper.research_objectives_and_hypothesis
        assert "The main finding" in paper.results_and_findings

    def test_get_flashcards_for_review(self, data_handler):
        """Test getting flashcards for review."""
        # Add some papers
        data_handler.add_flashcard(paper_title="Paper 1", authors="Author 1", tags=["test"])
        data_handler.add_flashcard(paper_title="Paper 2", authors="Author 2", tags=["test"])

        # Both should be due for review
        due_papers = data_handler.get_flashcards_for_review()
        assert len(due_papers) >= 2

    def test_get_flashcards_for_review_with_limit(self, data_handler):
        """Test getting limited number of flashcards for review."""
        # Add multiple papers
        for i in range(5):
            data_handler.add_flashcard(paper_title=f"Paper {i}", authors=f"Author {i}")

        # Get only 3 for review
        due_papers = data_handler.get_flashcards_for_review(limit=3)
        assert len(due_papers) == 3

    def test_process_review_easy(self, data_handler):
        """Test processing an easy review."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        # Get initial state
        paper = data_handler.get_flashcard_by_id(paper_id)
        initial_ease = paper.ease_factor

        # Process easy review
        response = ReviewResponse(flashpaper_id=paper_id, difficulty="easy")
        success = data_handler.process_review(response)
        assert success is True

        # Verify changes
        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper.ease_factor > initial_ease  # Ease factor should increase
        assert paper.review_count == 1
        assert paper.last_review_date is not None
        assert paper.next_review_date is not None

    def test_process_review_hard(self, data_handler):
        """Test processing a hard review."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        # Get initial state
        paper = data_handler.get_flashcard_by_id(paper_id)
        initial_ease = paper.ease_factor

        # Process hard review
        response = ReviewResponse(flashpaper_id=paper_id, difficulty="hard")
        success = data_handler.process_review(response)
        assert success is True

        # Verify changes
        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper.ease_factor < initial_ease  # Ease factor should decrease
        assert paper.review_count == 1

    def test_process_review_medium(self, data_handler):
        """Test processing a medium review."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        # Get initial state
        paper = data_handler.get_flashcard_by_id(paper_id)
        initial_ease = paper.ease_factor

        # Process medium review
        response = ReviewResponse(flashpaper_id=paper_id, difficulty="medium")
        success = data_handler.process_review(response)
        assert success is True

        # Verify changes
        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper.ease_factor == initial_ease  # Ease factor should stay same
        assert paper.review_count == 1

    def test_update_flashcard_review_legacy(self, data_handler):
        """Test legacy update_flashcard_review method."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        success = data_handler.update_flashcard_review(paper_id, success=True)
        assert success is True

        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper.review_count == 1

    def test_update_flashcard(self, data_handler):
        """Test updating a flashcard."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        paper = data_handler.get_flashcard_by_id(paper_id)
        paper.paper_title = "Updated Title"
        paper.notes = "New notes"

        success = data_handler.update_flashcard(paper)
        assert success is True

        updated = data_handler.get_flashcard_by_id(paper_id)
        assert updated.paper_title == "Updated Title"
        assert updated.notes == "New notes"

    def test_delete_flashcard(self, data_handler):
        """Test deleting a flashcard."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        success = data_handler.delete_flashcard(paper_id)
        assert success is True

        paper = data_handler.get_flashcard_by_id(paper_id)
        assert paper is None

    def test_get_all_flashcards(self, data_handler):
        """Test getting all flashcards."""
        # Add multiple papers
        for i in range(3):
            data_handler.add_flashcard(paper_title=f"Paper {i}", authors=f"Author {i}")

        all_papers = data_handler.get_all_flashcards()
        assert len(all_papers) == 3

    def test_srs_interval_calculation(self, data_handler):
        """Test SRS interval calculation over multiple reviews."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        # Review multiple times as "easy"
        for _ in range(3):
            response = ReviewResponse(flashpaper_id=paper_id, difficulty="easy")
            data_handler.process_review(response)

        paper = data_handler.get_flashcard_by_id(paper_id)

        # Interval should increase with each review
        assert paper.interval_days > 1
        assert paper.review_count == 3

    def test_ease_factor_bounds(self, data_handler):
        """Test that ease factor stays within bounds."""
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        # Review many times as "hard" to try to push ease factor below minimum
        for _ in range(10):
            response = ReviewResponse(flashpaper_id=paper_id, difficulty="hard")
            data_handler.process_review(response)

        paper = data_handler.get_flashcard_by_id(paper_id)

        # Ease factor should not go below 1.3
        assert paper.ease_factor >= 1.3
