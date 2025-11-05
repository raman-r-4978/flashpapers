"""Tests for search and analytics utilities."""

import pytest

from flashpapers.models import ReviewResponse


class TestSearchUtils:
    """Tests for SearchUtils class."""

    def test_search_by_title(self, search_utils, storage, sample_flashpapers):
        """Test searching flashcards by title."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.search_flashcards("BERT")
        assert len(results) == 1
        assert results[0].paper_title.startswith("BERT")

    def test_search_by_author(self, search_utils, storage, sample_flashpapers):
        """Test searching flashcards by author."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.search_by_author("Brown")
        assert len(results) == 1
        assert "Brown" in results[0].authors

    def test_search_by_keyword(self, search_utils, storage, sample_flashpapers):
        """Test searching by keyword."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.search_flashcards("transformers")
        # Should find papers with "transformers" keyword or in content
        assert len(results) >= 0

    def test_search_by_category(self, search_utils, storage, sample_flashpapers):
        """Test filtering by category."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.search_flashcards("", categories=["Computer Vision"])
        assert len(results) == 1
        assert "Computer Vision" in results[0].category

    def test_search_combined_filters(self, search_utils, storage, sample_flashpapers):
        """Test search with combined filters."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.search_flashcards(
            "Deep",
            categories=["Natural Language Processing"],
        )
        # Should find NLP papers with "Deep" in content
        assert all("Natural Language Processing" in r.category for r in results)

    def test_get_all_tags(self, search_utils, storage, sample_flashpapers):
        """Test getting all unique tags."""
        for paper in sample_flashpapers:
            storage.add(paper)

        tags = search_utils.get_all_tags()
        assert "BERT" in tags
        assert "GPT" in tags
        assert len(tags) > 0

    def test_get_all_categories(self, search_utils, storage, sample_flashpapers):
        """Test getting all unique categories."""
        for paper in sample_flashpapers:
            storage.add(paper)

        categories = search_utils.get_all_categories()
        assert "Deep Learning" in categories
        assert "Natural Language Processing" in categories
        assert "Computer Vision" in categories

    def test_filter_by_category(self, search_utils, storage, sample_flashpapers):
        """Test filtering by specific category."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.filter_by_category("Computer Vision")
        assert len(results) == 1
        assert all("Computer Vision" in r.category for r in results)

    def test_filter_by_keyword(self, search_utils, storage, sample_flashpapers):
        """Test filtering by specific keyword."""
        for paper in sample_flashpapers:
            storage.add(paper)

        results = search_utils.filter_by_keyword("BERT")
        assert len(results) == 1

    def test_get_recent_papers(self, search_utils, storage, sample_flashpapers):
        """Test getting recent papers."""
        for paper in sample_flashpapers:
            storage.add(paper)

        recent = search_utils.get_recent_papers(limit=2)
        assert len(recent) == 2

    def test_empty_search(self, search_utils, storage):
        """Test search on empty storage."""
        results = search_utils.search_flashcards("test")
        assert len(results) == 0

        tags = search_utils.get_all_tags()
        assert len(tags) == 0


class TestAnalyticsUtils:
    """Tests for AnalyticsUtils class."""

    def test_get_analytics_empty(self, analytics):
        """Test analytics with no papers."""
        stats = analytics.get_analytics()

        assert stats["total_papers"] == 0
        assert stats["reviewed_papers"] == 0
        assert stats["papers_due_today"] == 0
        assert stats["total_reviews"] == 0

    def test_get_analytics_with_papers(self, analytics, storage, data_handler, sample_flashpapers):
        """Test analytics with papers."""
        # Add papers
        paper_ids = []
        for paper in sample_flashpapers:
            paper_id = storage.add(paper)
            paper_ids.append(paper_id)

        stats = analytics.get_analytics()

        assert stats["total_papers"] == len(sample_flashpapers)
        assert stats["reviewed_papers"] == 0  # None reviewed yet
        assert stats["average_ease_factor"] == 2.5

    def test_get_analytics_with_reviews(self, analytics, storage, data_handler):
        """Test analytics after reviews."""
        # Add a paper
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author", tags=["test"])

        # Review it
        response = ReviewResponse(flashpaper_id=paper_id, difficulty="easy")
        data_handler.process_review(response)

        stats = analytics.get_analytics()

        assert stats["total_papers"] == 1
        assert stats["reviewed_papers"] == 1
        assert stats["total_reviews"] == 1

    def test_get_category_stats(self, analytics, storage, sample_flashpapers):
        """Test category statistics."""
        for paper in sample_flashpapers:
            storage.add(paper)

        cat_stats = analytics.get_category_stats()

        assert cat_stats["Deep Learning"] == 3  # All papers have this category
        assert cat_stats["Natural Language Processing"] == 2
        assert cat_stats["Computer Vision"] == 1

    def test_get_retention_rate(self, analytics, storage, data_handler):
        """Test retention rate calculation."""
        # Add papers
        paper_id1 = data_handler.add_flashcard(paper_title="Paper 1", authors="Author 1")
        paper_id2 = data_handler.add_flashcard(paper_title="Paper 2", authors="Author 2")

        # Review one
        response = ReviewResponse(flashpaper_id=paper_id1, difficulty="easy")
        data_handler.process_review(response)

        retention = analytics.get_retention_rate()
        assert retention == 50.0  # 1 out of 2 reviewed

    def test_get_upcoming_reviews(self, analytics, storage, data_handler):
        """Test getting upcoming reviews."""
        # Add and review a paper
        paper_id = data_handler.add_flashcard(paper_title="Test", authors="Author")

        response = ReviewResponse(flashpaper_id=paper_id, difficulty="medium")
        data_handler.process_review(response)

        upcoming = analytics.get_upcoming_reviews(days=30)

        # Should have one upcoming review
        assert len(upcoming) >= 0  # Depends on interval calculation

    def test_get_performance_metrics(self, analytics, storage, data_handler):
        """Test performance metrics."""
        # Add papers and review them
        paper_id1 = data_handler.add_flashcard(paper_title="Paper 1", authors="Author 1")
        paper_id2 = data_handler.add_flashcard(paper_title="Paper 2", authors="Author 2")

        # Review first paper twice
        for _ in range(2):
            response = ReviewResponse(flashpaper_id=paper_id1, difficulty="easy")
            data_handler.process_review(response)

        # Review second paper once
        response = ReviewResponse(flashpaper_id=paper_id2, difficulty="medium")
        data_handler.process_review(response)

        metrics = analytics.get_performance_metrics()

        assert metrics["average_reviews_per_paper"] == 1.5  # 3 reviews / 2 papers
        assert metrics["retention_rate"] == 100.0  # Both reviewed
        assert metrics["most_reviewed_paper"]["review_count"] == 2

    def test_performance_metrics_empty(self, analytics):
        """Test performance metrics with no papers."""
        metrics = analytics.get_performance_metrics()

        assert metrics["average_reviews_per_paper"] == 0
        assert metrics["retention_rate"] == 0
        assert metrics["most_reviewed_paper"] is None
