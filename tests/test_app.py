#!/usr/bin/env python3
"""
Simple test script to verify the flashcards app functionality
"""

import sys
import os
import io

# # Add the current directory to the Python path so we can import our modules
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flashpapers.utils.data_handler import FlashcardDataHandler
from flashpapers.utils.flashcard_storage import FlashcardStorage
from flashpapers.utils.analytics_utils import AnalyticsUtils
from flashpapers.utils.search_utils import SearchUtils
from flashpapers.utils.pdf_utils import save_pdf


def test_flashcard_operations():
    """Test all flashcard operations and print concise results."""
    print("🧪 Testing Flashcard Operations...\n")
    
    try:
        # Initialize components
        data_handler = FlashcardDataHandler()
        storage = FlashcardStorage()
        analytics = AnalyticsUtils(storage)
        search = SearchUtils(storage)
        
        # Test 1: Add flashcard
        card_id = data_handler.add_flashcard(
            question="What is the capital of France?",
            answer="Paris",
            tags=["geography", "europe", "capitals"],
            difficulty="easy"
        )
        
        # Test 2: Load flashcards
        df = storage.load_flashcards()
        
        # Test 3: Get analytics
        analytics_data = analytics.get_analytics()
        
        # Test 4: Search functionality
        search_results = search.search_flashcards("France")
        
        # Test 5: Review functionality
        review_cards = data_handler.get_flashcards_for_review(limit=5)
        
        # Test 6: Update review
        data_handler.update_flashcard_review(card_id, True)
        
        # Test 7: Get tags
        tags = search.get_all_tags()
        
        # Test 8: PDF utility
        fake_pdf = io.BytesIO(b"%PDF-1.4 test pdf content")
        pdf_path = save_pdf(fake_pdf, "TestPDF", card_id)
        
        # Print results
        print(f"✅ Flashcard added (ID: {card_id})")
        print(f"✅ Loaded {len(df)} flashcards")
        print(f"✅ Analytics: {analytics_data['total_cards']} total, {analytics_data['reviewed_cards']} reviewed")
        print(f"✅ Search found {len(search_results)} results for 'France'")
        print(f"✅ {len(review_cards)} cards ready for review")
        print(f"✅ Tags available: {len(tags)}")
        print(f"✅ PDF saved to: {os.path.basename(pdf_path)}")
        
        print("\n🎉 All tests passed! Run: streamlit run main_app.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_flashcard_operations()
