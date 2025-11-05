"""Data models for Flashpapers application using Pydantic for validation."""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class Flashpaper(BaseModel):
    """Model representing a research paper flashcard."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    paper_title: str = Field(..., min_length=1, description="Title of the research paper")
    authors: str = Field(..., min_length=1, description="Authors of the paper")
    background_of_the_study: str = Field(default="", description="Background context")
    research_objectives_and_hypothesis: str = Field(
        default="", description="Research objectives and hypotheses"
    )
    methodology: str = Field(default="", description="Research methodology")
    results_and_findings: str = Field(default="", description="Key results and findings")
    discussion_and_interpretation: str = Field(
        default="", description="Discussion and interpretation"
    )
    contributions_to_the_field: str = Field(
        default="", description="Main contributions to the field"
    )
    achievements_and_significance: str = Field(
        default="", description="Achievements and significance"
    )
    link: Optional[str] = Field(default=None, description="URL link to the paper")
    notes: str = Field(default="", description="Additional notes")
    keywords: List[str] = Field(default_factory=list, description="Keywords for the paper")
    category: List[str] = Field(default_factory=list, description="Categories for organization")
    added_date: datetime = Field(default_factory=datetime.now)
    next_review_date: Optional[datetime] = Field(
        default=None, description="Next scheduled review date"
    )
    review_count: int = Field(default=0, ge=0, description="Number of times reviewed")
    ease_factor: float = Field(default=2.5, ge=1.3, description="SRS ease factor")
    interval_days: int = Field(default=0, ge=0, description="Current review interval in days")
    last_review_date: Optional[datetime] = Field(default=None, description="Last review date")
    pdf_path: Optional[str] = Field(default=None, description="Path to attached PDF")

    @field_validator("keywords", "category", mode="before")
    @classmethod
    def ensure_list(cls, v):
        """Ensure fields are lists."""
        if isinstance(v, str):
            return [v] if v else []
        return v if v else []

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class AppConfig(BaseModel):
    """Application configuration model."""

    categories: List[str] = Field(
        default_factory=lambda: [
            "Machine Learning",
            "Deep Learning",
            "Natural Language Processing",
            "Computer Vision",
            "Reinforcement Learning",
            "Optimization",
            "Other",
        ]
    )
    backup_frequency_days: int = Field(default=7, ge=1, description="Backup frequency in days")
    last_backup_timestamp: Optional[datetime] = Field(
        default=None, description="Last backup timestamp"
    )
    srs_parameters: dict = Field(
        default_factory=lambda: {
            "initial_ease_factor": 2.5,
            "minimum_interval_days": 1,
            "maximum_interval_days": 365,
            "easy_bonus": 1.3,
            "hard_penalty": 0.8,
        }
    )
    current_user: str = Field(default="default")
    data_directory: str = Field(default="data")

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class ReviewResponse(BaseModel):
    """Model for review response."""

    flashpaper_id: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    timestamp: datetime = Field(default_factory=datetime.now)


class AnalyticsData(BaseModel):
    """Model for analytics data."""

    total_papers: int = Field(default=0, ge=0)
    reviewed_papers: int = Field(default=0, ge=0)
    papers_due_today: int = Field(default=0, ge=0)
    total_reviews: int = Field(default=0, ge=0)
    average_ease_factor: float = Field(default=2.5, ge=1.3)
    categories_distribution: dict = Field(default_factory=dict)
    review_history: List[dict] = Field(default_factory=list)
