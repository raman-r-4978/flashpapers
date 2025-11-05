#!/usr/bin/env python3
"""Integration test to verify the flashcards app functionality."""

import io
import tempfile
from pathlib import Path

from flashpapers.utils import AnalyticsUtils, FlashcardDataHandler, FlashcardStorage, SearchUtils
from flashpapers.utils.pdf_utils import save_pdf


def test_flashcard_operations():
    """Integration test for all flashcard operations."""
    print("🧪 Testing Flashcard Operations...\n")

    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)

        # Initialize components with temporary storage
        storage = FlashcardStorage(storage_path=temp_path / "test_flashpapers.json")
        data_handler = FlashcardDataHandler(storage=storage)
        analytics = AnalyticsUtils(storage)
        search = SearchUtils(storage)

        # Test 1: Add flashcard
        card_id = data_handler.add_flashcard(
            paper_title="What is the capital of France?",
            authors="Test Author",
            tags=["geography", "europe", "capitals"],
        )
        print(f"✅ Flashcard added (ID: {card_id[:8]}...)")

        # Test 2: Load flashcards
        df = storage.load_flashcards()
        print(f"✅ Loaded {len(df)} flashcards")

        # Test 3: Get analytics
        analytics_data = analytics.get_analytics()
        print(
            f"✅ Analytics: {analytics_data['total_papers']} total, "
            f"{analytics_data['reviewed_papers']} reviewed"
        )

        # Test 4: Search functionality
        search_results = search.search_flashcards("France")
        print(f"✅ Search found {len(search_results)} results for 'France'")

        # Test 5: Review functionality
        review_cards = data_handler.get_flashcards_for_review(limit=5)
        print(f"✅ {len(review_cards)} cards ready for review")

        # Test 6: Update review
        data_handler.update_flashcard_review(card_id, True)
        print(f"✅ Review updated for card {card_id[:8]}...")

        # Test 7: Get tags
        tags = search.get_all_tags()
        print(f"✅ Tags available: {len(tags)}")

        # Test 8: PDF utility
        fake_pdf = io.BytesIO(b"%PDF-1.4 test pdf content")
        pdf_path = save_pdf(fake_pdf, "TestPDF", card_id, pdf_dir=temp_path / "pdfs")
        print(f"✅ PDF saved to: {Path(pdf_path).name}")

        print("\n🎉 All tests passed! Run: streamlit run main_app.py")


if __name__ == "__main__":
    test_flashcard_operations()
