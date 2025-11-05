"""Analytics utilities for flashpapers."""

from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from flashpapers.models import AnalyticsData, Flashpaper
from flashpapers.utils.flashcard_storage import FlashcardStorage


class AnalyticsUtils:
    """Provides analytics and statistics for flashpapers."""

    def __init__(self, storage: Optional[FlashcardStorage] = None):
        """
        Initialize analytics utils.

        Args:
            storage: FlashcardStorage instance
        """
        self.storage = storage or FlashcardStorage()

    def _get_flashpapers(self, flashpapers: Optional[List[Flashpaper]] = None) -> List[Flashpaper]:
        """
        Get flashpapers from cache or storage.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of Flashpaper objects
        """
        if flashpapers is not None:
            return flashpapers
        return self.storage.load_all()

    def get_analytics(self, flashpapers: Optional[List[Flashpaper]] = None) -> Dict:
        """
        Get comprehensive analytics data.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Dictionary containing analytics metrics
        """
        flashpapers = self._get_flashpapers(flashpapers)
        now = datetime.now()

        # Calculate metrics
        total_papers = len(flashpapers)
        reviewed_papers = len([fp for fp in flashpapers if fp.review_count > 0])
        papers_due_today = len(
            [
                fp
                for fp in flashpapers
                if fp.next_review_date and fp.next_review_date.date() <= now.date()
            ]
        )
        total_reviews = sum(fp.review_count for fp in flashpapers)

        # Calculate average ease factor
        if flashpapers:
            avg_ease = sum(fp.ease_factor for fp in flashpapers) / len(flashpapers)
        else:
            avg_ease = 2.5

        # Category distribution
        category_counter = Counter()
        for fp in flashpapers:
            for cat in fp.category:
                category_counter[cat] += 1

        # Review history (last 30 days)
        review_history = []
        for fp in flashpapers:
            if fp.last_review_date:
                days_ago = (now - fp.last_review_date).days
                if days_ago <= 30:
                    review_history.append(
                        {
                            "paper_id": fp.id,
                            "paper_title": fp.paper_title,
                            "review_date": fp.last_review_date.isoformat(),
                            "days_ago": days_ago,
                        }
                    )

        analytics_data = AnalyticsData(
            total_papers=total_papers,
            reviewed_papers=reviewed_papers,
            papers_due_today=papers_due_today,
            total_reviews=total_reviews,
            average_ease_factor=round(avg_ease, 2),
            categories_distribution=dict(category_counter),
            review_history=review_history,
        )

        return analytics_data.model_dump()

    def get_category_stats(self, flashpapers: Optional[List[Flashpaper]] = None) -> Dict[str, int]:
        """
        Get paper count by category.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Dictionary mapping category to count
        """
        flashpapers = self._get_flashpapers(flashpapers)
        category_counter = Counter()

        for fp in flashpapers:
            for cat in fp.category:
                category_counter[cat] += 1

        return dict(category_counter)

    def get_review_streak(self, flashpapers: Optional[List[Flashpaper]] = None) -> int:
        """
        Get current review streak in days.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Number of consecutive days with reviews
        """
        flashpapers = self._get_flashpapers(flashpapers)
        review_dates = [fp.last_review_date for fp in flashpapers if fp.last_review_date]

        if not review_dates:
            return 0

        review_dates.sort(reverse=True)
        now = datetime.now().date()
        streak = 0

        for i in range(len(review_dates)):
            expected_date = now - timedelta(days=i)
            if any(rd.date() == expected_date for rd in review_dates):
                streak += 1
            else:
                break

        return streak

    def get_retention_rate(self, flashpapers: Optional[List[Flashpaper]] = None) -> float:
        """
        Calculate retention rate (papers reviewed vs total).

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Retention rate as percentage
        """
        flashpapers = self._get_flashpapers(flashpapers)
        if not flashpapers:
            return 0.0

        reviewed_count = len([fp for fp in flashpapers if fp.review_count > 0])
        return round((reviewed_count / len(flashpapers)) * 100, 2)

    def get_upcoming_reviews(self, days: int = 7, flashpapers: Optional[List[Flashpaper]] = None) -> List[Dict]:
        """
        Get papers due for review in the next N days.

        Args:
            days: Number of days to look ahead
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of papers with review dates
        """
        flashpapers = self._get_flashpapers(flashpapers)
        now = datetime.now()
        future_date = now + timedelta(days=days)

        upcoming = []
        for fp in flashpapers:
            if fp.next_review_date and now <= fp.next_review_date <= future_date:
                upcoming.append(
                    {
                        "paper_id": fp.id,
                        "paper_title": fp.paper_title,
                        "review_date": fp.next_review_date.isoformat(),
                        "days_until": (fp.next_review_date.date() - now.date()).days,
                    }
                )

        # Sort by review date
        upcoming.sort(key=lambda x: x["review_date"])
        return upcoming

    def get_performance_metrics(self, flashpapers: Optional[List[Flashpaper]] = None) -> Dict:
        """
        Get performance metrics.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Dictionary with performance metrics
        """
        flashpapers = self._get_flashpapers(flashpapers)

        if not flashpapers:
            return {
                "average_reviews_per_paper": 0,
                "retention_rate": 0,
                "review_streak": 0,
                "most_reviewed_paper": None,
            }

        avg_reviews = sum(fp.review_count for fp in flashpapers) / len(flashpapers)
        most_reviewed = max(flashpapers, key=lambda x: x.review_count)

        return {
            "average_reviews_per_paper": round(avg_reviews, 2),
            "retention_rate": self.get_retention_rate(flashpapers),
            "review_streak": self.get_review_streak(flashpapers),
            "most_reviewed_paper": {
                "title": most_reviewed.paper_title,
                "review_count": most_reviewed.review_count,
            },
        }
