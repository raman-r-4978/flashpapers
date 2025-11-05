"""Search utilities for flashpapers."""

from typing import List, Optional, Set

from flashpapers.models import Flashpaper
from flashpapers.utils.flashcard_storage import FlashcardStorage


class SearchUtils:
    """Provides search functionality for flashpapers."""

    def __init__(self, storage: Optional[FlashcardStorage] = None):
        """
        Initialize search utils.

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

    def search_flashcards(
        self,
        query: str,
        categories: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        flashpapers: Optional[List[Flashpaper]] = None,
    ) -> List[Flashpaper]:
        """
        Search flashcards by query, categories, and keywords.

        Args:
            query: Search query string
            categories: Filter by categories
            keywords: Filter by keywords
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of matching Flashpaper objects
        """
        flashpapers = self._get_flashpapers(flashpapers)
        query_lower = query.lower().strip()

        results = []
        for fp in flashpapers:
            # Category filter
            if categories:
                if not any(cat in fp.category for cat in categories):
                    continue

            # Keyword filter
            if keywords:
                if not any(kw in fp.keywords for kw in keywords):
                    continue

            # Text search
            if query_lower:
                searchable_text = " ".join(
                    [
                        fp.paper_title,
                        fp.authors,
                        fp.background_of_the_study,
                        fp.research_objectives_and_hypothesis,
                        fp.methodology,
                        fp.results_and_findings,
                        fp.discussion_and_interpretation,
                        fp.contributions_to_the_field,
                        fp.achievements_and_significance,
                        fp.notes,
                        " ".join(fp.keywords),
                        " ".join(fp.category),
                    ]
                ).lower()

                if query_lower in searchable_text:
                    results.append(fp)
            else:
                results.append(fp)

        return results

    def search_by_title(
        self, title_query: str, flashpapers: Optional[List[Flashpaper]] = None
    ) -> List[Flashpaper]:
        """
        Search flashcards by title only.

        Args:
            title_query: Title search query
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of matching Flashpaper objects
        """
        flashpapers = self._get_flashpapers(flashpapers)
        query_lower = title_query.lower().strip()

        return [fp for fp in flashpapers if query_lower in fp.paper_title.lower()]

    def search_by_author(
        self, author_query: str, flashpapers: Optional[List[Flashpaper]] = None
    ) -> List[Flashpaper]:
        """
        Search flashcards by author.

        Args:
            author_query: Author search query
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of matching Flashpaper objects
        """
        flashpapers = self._get_flashpapers(flashpapers)
        query_lower = author_query.lower().strip()

        return [fp for fp in flashpapers if query_lower in fp.authors.lower()]

    def get_all_tags(self, flashpapers: Optional[List[Flashpaper]] = None) -> List[str]:
        """
        Get all unique keywords/tags.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Sorted list of all unique tags
        """
        flashpapers = self._get_flashpapers(flashpapers)
        tags: Set[str] = set()

        for fp in flashpapers:
            tags.update(fp.keywords)

        return sorted(list(tags))

    def get_all_categories(self, flashpapers: Optional[List[Flashpaper]] = None) -> List[str]:
        """
        Get all unique categories used.

        Args:
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            Sorted list of all unique categories
        """
        flashpapers = self._get_flashpapers(flashpapers)
        categories: Set[str] = set()

        for fp in flashpapers:
            categories.update(fp.category)

        return sorted(list(categories))

    def filter_by_category(
        self, category: str, flashpapers: Optional[List[Flashpaper]] = None
    ) -> List[Flashpaper]:
        """
        Get all flashcards in a specific category.

        Args:
            category: Category name
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of Flashpaper objects in the category
        """
        flashpapers = self._get_flashpapers(flashpapers)
        return [fp for fp in flashpapers if category in fp.category]

    def filter_by_keyword(
        self, keyword: str, flashpapers: Optional[List[Flashpaper]] = None
    ) -> List[Flashpaper]:
        """
        Get all flashcards with a specific keyword.

        Args:
            keyword: Keyword to filter by
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of Flashpaper objects with the keyword
        """
        flashpapers = self._get_flashpapers(flashpapers)
        return [fp for fp in flashpapers if keyword in fp.keywords]

    def get_recent_papers(
        self, limit: int = 10, flashpapers: Optional[List[Flashpaper]] = None
    ) -> List[Flashpaper]:
        """
        Get most recently added papers.

        Args:
            limit: Maximum number of papers to return
            flashpapers: Optional pre-loaded flashpapers list

        Returns:
            List of recent Flashpaper objects
        """
        flashpapers = self._get_flashpapers(flashpapers)
        flashpapers.sort(key=lambda x: x.added_date, reverse=True)
        return flashpapers[:limit]
