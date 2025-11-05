"""Tests for data models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from flashpapers.models import AnalyticsData, AppConfig, Flashpaper, ReviewResponse


class TestFlashpaper:
    """Tests for Flashpaper model."""

    def test_create_minimal_flashpaper(self):
        """Test creating a flashpaper with minimal required fields."""
        paper = Flashpaper(paper_title="Test Paper", authors="Test Author")
        assert paper.paper_title == "Test Paper"
        assert paper.authors == "Test Author"
        assert paper.id is not None
        assert isinstance(paper.added_date, datetime)

    def test_create_full_flashpaper(self, sample_flashpaper):
        """Test creating a flashpaper with all fields."""
        assert sample_flashpaper.paper_title == "Attention Is All You Need"
        assert sample_flashpaper.authors == "Vaswani et al."
        assert "transformers" in sample_flashpaper.keywords
        assert "Deep Learning" in sample_flashpaper.category

    def test_flashpaper_validation(self):
        """Test flashpaper validation."""
        # Empty title should fail
        with pytest.raises(ValidationError):
            Flashpaper(paper_title="", authors="Test")

        # Empty authors should fail
        with pytest.raises(ValidationError):
            Flashpaper(paper_title="Test", authors="")

    def test_keywords_as_string(self):
        """Test that keywords can be provided as string and converted to list."""
        paper = Flashpaper(paper_title="Test", authors="Author", keywords="single")
        assert paper.keywords == ["single"]

    def test_default_values(self):
        """Test default values for optional fields."""
        paper = Flashpaper(paper_title="Test", authors="Author")
        assert paper.review_count == 0
        assert paper.ease_factor == 2.5
        assert paper.interval_days == 0
        assert paper.keywords == []
        assert paper.category == []

    def test_ease_factor_bounds(self):
        """Test ease factor bounds."""
        # Ease factor below minimum should fail
        with pytest.raises(ValidationError):
            Flashpaper(paper_title="Test", authors="Author", ease_factor=1.0)


class TestAppConfig:
    """Tests for AppConfig model."""

    def test_create_default_config(self):
        """Test creating config with defaults."""
        config = AppConfig()
        assert config.backup_frequency_days == 7
        assert config.current_user == "default"
        assert "Machine Learning" in config.categories
        assert config.srs_parameters["initial_ease_factor"] == 2.5

    def test_create_custom_config(self):
        """Test creating config with custom values."""
        config = AppConfig(
            backup_frequency_days=14, current_user="test_user", categories=["Test Category"]
        )
        assert config.backup_frequency_days == 14
        assert config.current_user == "test_user"
        assert config.categories == ["Test Category"]


class TestReviewResponse:
    """Tests for ReviewResponse model."""

    def test_create_review_response(self):
        """Test creating a review response."""
        response = ReviewResponse(flashpaper_id="test-id", difficulty="easy")
        assert response.flashpaper_id == "test-id"
        assert response.difficulty == "easy"
        assert isinstance(response.timestamp, datetime)

    def test_invalid_difficulty(self):
        """Test that invalid difficulty raises error."""
        with pytest.raises(ValidationError):
            ReviewResponse(flashpaper_id="test-id", difficulty="invalid")


class TestAnalyticsData:
    """Tests for AnalyticsData model."""

    def test_create_analytics_data(self):
        """Test creating analytics data."""
        data = AnalyticsData(
            total_papers=10, reviewed_papers=5, papers_due_today=2, total_reviews=25
        )
        assert data.total_papers == 10
        assert data.reviewed_papers == 5
        assert data.average_ease_factor == 2.5

    def test_negative_values(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            AnalyticsData(total_papers=-1)
