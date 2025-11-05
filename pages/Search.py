"""Search and browse papers."""

import streamlit as st
from typing import List

from flashpapers.models import Flashpaper
from flashpapers.utils import SearchUtils, FlashcardDataHandler, FlashcardStorage

st.set_page_config(page_title="Search Papers", page_icon="🔍", layout="wide")

# Initialize session state
if "storage" not in st.session_state:
    st.session_state.storage = FlashcardStorage()

if "data_handler" not in st.session_state:
    st.session_state.data_handler = FlashcardDataHandler(storage=st.session_state.storage)


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

st.title("🔍 Search Papers")

# Get instances from session state
storage = st.session_state.storage
search_utils = SearchUtils(storage)
data_handler = st.session_state.data_handler
cached_flashpapers = get_cached_flashpapers()

# Search controls
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "Search", placeholder="Search by title, author, content, keywords...", label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True, type="primary")

# Advanced filters
with st.expander("🔧 Advanced Filters"):
    col1, col2 = st.columns(2)

    with col1:
        # Category filter
        all_categories = search_utils.get_all_categories(flashpapers=cached_flashpapers)
        selected_categories = st.multiselect("Filter by Categories", options=all_categories)

    with col2:
        # Keyword filter
        all_keywords = search_utils.get_all_tags(flashpapers=cached_flashpapers)
        selected_keywords = st.multiselect("Filter by Keywords", options=all_keywords)

# Perform search
if search_button or search_query or selected_categories or selected_keywords:
    results = search_utils.search_flashcards(
        query=search_query or "",
        categories=selected_categories or None,
        keywords=selected_keywords or None,
        flashpapers=cached_flashpapers,
    )

    st.markdown(f"### Found {len(results)} paper(s)")

    if results:
        # Sort options
        sort_by = st.selectbox(
            "Sort by", ["Recent (Added)", "Title", "Review Count", "Next Review Date"]
        )

        if sort_by == "Recent (Added)":
            results.sort(key=lambda x: x.added_date, reverse=True)
        elif sort_by == "Title":
            results.sort(key=lambda x: x.paper_title.lower())
        elif sort_by == "Review Count":
            results.sort(key=lambda x: x.review_count, reverse=True)
        elif sort_by == "Next Review Date":
            results.sort(key=lambda x: x.next_review_date or x.added_date)

        # Display results
        for paper in results:
            with st.expander(f"📄 {paper.paper_title}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Authors:** {paper.authors}")

                    if paper.category:
                        cats = ", ".join(f"`{cat}`" for cat in paper.category)
                        st.markdown(f"**Categories:** {cats}")

                    if paper.keywords:
                        kws = ", ".join(f"`{kw}`" for kw in paper.keywords)
                        st.markdown(f"**Keywords:** {kws}")

                    # Show snippets
                    if paper.background_of_the_study:
                        st.markdown("**Background:**")
                        st.write(paper.background_of_the_study[:200] + "..." if len(paper.background_of_the_study) > 200 else paper.background_of_the_study)

                    if paper.results_and_findings:
                        st.markdown("**Results:**")
                        st.write(paper.results_and_findings[:200] + "..." if len(paper.results_and_findings) > 200 else paper.results_and_findings)

                    if paper.contributions_to_the_field:
                        st.markdown("**Contributions:**")
                        st.write(paper.contributions_to_the_field[:200] + "..." if len(paper.contributions_to_the_field) > 200 else paper.contributions_to_the_field)

                with col2:
                    st.metric("Reviews", paper.review_count)
                    st.metric("Ease Factor", f"{paper.ease_factor:.2f}")

                    if paper.next_review_date:
                        st.caption(f"Next review: {paper.next_review_date.strftime('%Y-%m-%d')}")

                # Actions
                col1, col2, col3 = st.columns(3)

                with col1:
                    if paper.link:
                        st.link_button("🔗 View Paper", paper.link, use_container_width=True)

                with col2:
                    if st.button("✏️ Edit", key=f"edit_{paper.id}", use_container_width=True):
                        st.session_state.edit_paper_id = paper.id
                        st.info("Edit functionality coming soon!")

                with col3:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{paper.id}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        if data_handler.delete_flashcard(paper.id):
                            invalidate_flashpapers_cache()
                            st.success("Paper deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete paper")

                # Full details toggle
                show_full = st.checkbox("Show full details", key=f"full_{paper.id}")
                if show_full:
                    st.markdown("---")

                    if paper.research_objectives_and_hypothesis:
                        st.markdown("**Research Objectives:**")
                        st.write(paper.research_objectives_and_hypothesis)

                    if paper.methodology:
                        st.markdown("**Methodology:**")
                        st.write(paper.methodology)

                    if paper.discussion_and_interpretation:
                        st.markdown("**Discussion:**")
                        st.write(paper.discussion_and_interpretation)

                    if paper.achievements_and_significance:
                        st.markdown("**Significance:**")
                        st.write(paper.achievements_and_significance)

                    if paper.notes:
                        st.markdown("**Notes:**")
                        st.write(paper.notes)

                    if paper.pdf_path:
                        st.info(f"📄 PDF: {paper.pdf_path}")

    else:
        st.info("No papers found. Try adjusting your search criteria.")

else:
    # Show recent papers by default
    st.markdown("### 📚 Recent Papers")
    recent_papers = search_utils.get_recent_papers(limit=10, flashpapers=cached_flashpapers)

    if recent_papers:
        for paper in recent_papers:
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{paper.paper_title}**")
                    st.caption(f"by {paper.authors}")
                    if paper.category:
                        cats = ", ".join(f"`{cat}`" for cat in paper.category)
                        st.markdown(cats)

                with col2:
                    st.caption(f"Added: {paper.added_date.strftime('%Y-%m-%d')}")

                st.markdown("---")
    else:
        st.info("No papers in your collection yet. Add some papers to get started!")

# Sidebar with quick stats
with st.sidebar:
    st.header("📊 Collection Overview")

    from flashpapers.utils import AnalyticsUtils

    analytics = AnalyticsUtils(storage)
    stats = analytics.get_analytics(flashpapers=cached_flashpapers)

    st.metric("Total Papers", stats["total_papers"])
    st.metric("Reviewed Papers", stats["reviewed_papers"])

    # Category distribution
    if stats["categories_distribution"]:
        st.subheader("By Category")
        for cat, count in sorted(
            stats["categories_distribution"].items(), key=lambda x: x[1], reverse=True
        ):
            st.text(f"{cat}: {count}")

    # Keywords cloud
    st.subheader("Popular Keywords")
    all_keywords = search_utils.get_all_tags(flashpapers=cached_flashpapers)
    if all_keywords:
        st.write(", ".join(all_keywords[:10]))
    else:
        st.info("No keywords yet")
