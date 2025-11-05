"""Review papers using spaced repetition."""

import streamlit as st
from typing import List

from flashpapers.models import Flashpaper, ReviewResponse

st.set_page_config(page_title="Review Papers", page_icon="🔄", layout="wide")


def get_cached_flashpapers() -> List[Flashpaper]:
    """Get flashpapers from session state cache or load from storage."""
    cache_key = "_flashpapers_cache"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = st.session_state.storage.load_all()
    return st.session_state[cache_key]


def invalidate_flashpapers_cache() -> None:
    """Invalidate the flashpapers cache in session state."""
    cache_key = "_flashpapers_cache"
    if cache_key in st.session_state:
        del st.session_state[cache_key]
    st.session_state.storage.invalidate_cache()

st.title("🔄 Review Papers")

# Get instances from session state
data_handler = st.session_state.data_handler

# Initialize review session state
if "current_review_index" not in st.session_state:
    st.session_state.current_review_index = 0

if "review_papers" not in st.session_state:
    st.session_state.review_papers = data_handler.get_flashcards_for_review()

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False


def next_paper():
    """Move to next paper."""
    st.session_state.current_review_index += 1
    st.session_state.show_answer = False


def toggle_answer():
    """Toggle answer visibility."""
    st.session_state.show_answer = not st.session_state.show_answer


def submit_review(difficulty: str):
    """Submit review response."""
    current_paper = st.session_state.review_papers[st.session_state.current_review_index]
    response = ReviewResponse(flashpaper_id=current_paper.id, difficulty=difficulty)
    data_handler.process_review(response)
    # Invalidate cache after review
    invalidate_flashpapers_cache()
    next_paper()


# Get papers for review
papers = st.session_state.review_papers

if not papers:
    st.info("🎉 No papers due for review right now! Check back later.")
    if st.button("Refresh"):
        st.session_state.review_papers = data_handler.get_flashcards_for_review()
        st.rerun()
else:
    # Check if we've finished all reviews
    if st.session_state.current_review_index >= len(papers):
        st.success("🎉 Congratulations! You've completed all reviews for today!")
        st.balloons()

        if st.button("Start New Review Session"):
            st.session_state.current_review_index = 0
            st.session_state.review_papers = data_handler.get_flashcards_for_review()
            st.session_state.show_answer = False
            st.rerun()
    else:
        # Current paper
        current_paper = papers[st.session_state.current_review_index]

        # Progress
        progress = (st.session_state.current_review_index + 1) / len(papers)
        st.progress(progress)
        st.caption(f"Paper {st.session_state.current_review_index + 1} of {len(papers)}")

        # Display paper information
        st.markdown(f"### {current_paper.paper_title}")
        st.markdown(f"**Authors:** {current_paper.authors}")

        if current_paper.category:
            st.markdown(f"**Categories:** {', '.join(current_paper.category)}")

        if current_paper.keywords:
            st.markdown(f"**Keywords:** {', '.join(current_paper.keywords)}")

        st.markdown("---")

        # Show/Hide answer button
        if not st.session_state.show_answer:
            if st.button("🔍 Show Details", use_container_width=True, type="primary"):
                toggle_answer()
                st.rerun()
        else:
            # Display all details
            if current_paper.background_of_the_study:
                with st.expander("📖 Background", expanded=True):
                    st.write(current_paper.background_of_the_study)

            if current_paper.research_objectives_and_hypothesis:
                with st.expander("🎯 Research Objectives", expanded=True):
                    st.write(current_paper.research_objectives_and_hypothesis)

            if current_paper.methodology:
                with st.expander("🔬 Methodology", expanded=True):
                    st.write(current_paper.methodology)

            if current_paper.results_and_findings:
                with st.expander("📊 Results and Findings", expanded=True):
                    st.write(current_paper.results_and_findings)

            if current_paper.discussion_and_interpretation:
                with st.expander("💬 Discussion", expanded=True):
                    st.write(current_paper.discussion_and_interpretation)

            if current_paper.contributions_to_the_field:
                with st.expander("🌟 Contributions", expanded=True):
                    st.write(current_paper.contributions_to_the_field)

            if current_paper.achievements_and_significance:
                with st.expander("🏆 Significance", expanded=True):
                    st.write(current_paper.achievements_and_significance)

            if current_paper.notes:
                with st.expander("📝 Notes"):
                    st.write(current_paper.notes)

            if current_paper.link:
                st.markdown(f"🔗 [View Paper]({current_paper.link})")

            if current_paper.pdf_path:
                st.info(f"📄 PDF attached: {current_paper.pdf_path}")

            # Review metadata
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Review Count", current_paper.review_count)
            with col2:
                st.metric("Ease Factor", f"{current_paper.ease_factor:.2f}")
            with col3:
                st.metric("Interval (days)", current_paper.interval_days)

            # Rating buttons
            st.markdown("### How well did you remember this paper?")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("😰 Hard", use_container_width=True):
                    submit_review("hard")
                    st.rerun()

            with col2:
                if st.button("😐 Medium", use_container_width=True):
                    submit_review("medium")
                    st.rerun()

            with col3:
                if st.button("😊 Easy", use_container_width=True):
                    submit_review("easy")
                    st.rerun()

            with col4:
                if st.button("⏭️ Skip", use_container_width=True):
                    next_paper()
                    st.rerun()

# Sidebar with review statistics
with st.sidebar:
    st.header("📊 Review Statistics")

    from flashpapers.utils import AnalyticsUtils

    cached_flashpapers = get_cached_flashpapers()
    analytics = AnalyticsUtils(st.session_state.storage)
    stats = analytics.get_analytics(flashpapers=cached_flashpapers)

    st.metric("Total Papers", stats["total_papers"])
    st.metric("Reviewed", stats["reviewed_papers"])
    st.metric("Due Today", stats["papers_due_today"])
    st.metric("Total Reviews", stats["total_reviews"])
    st.metric("Avg Ease Factor", f"{stats['average_ease_factor']:.2f}")

    # Upcoming reviews
    st.subheader("📅 Upcoming Reviews")
    upcoming = analytics.get_upcoming_reviews(days=7, flashpapers=cached_flashpapers)
    if upcoming:
        for item in upcoming[:5]:
            st.text(f"• {item['paper_title'][:30]}...")
            st.caption(f"  in {item['days_until']} days")
    else:
        st.info("No reviews scheduled")
